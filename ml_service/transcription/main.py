from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import whisper_timestamped
import torch
import numpy as np
from pyannote.audio import Pipeline
from datetime import datetime
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
whisper_model = whisper_timestamped.load_model("large-v3")
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token=os.getenv("HUGGING_FACE_TOKEN")
)

class TranscriptionSegment(BaseModel):
    speaker: str
    start: float
    end: float
    text: str
    confidence: float

class TranscriptionResponse(BaseModel):
    segments: List[TranscriptionSegment]
    full_text: str
    metadata: dict

async def process_audio(audio_data: bytes) -> TranscriptionResponse:
    try:
        # Convert audio to proper format
        audio_array = whisper_timestamped.load_audio(audio_data)
        
        # Perform speaker diarization
        diarization = diarization_pipeline(audio_array)
        speaker_segments = [(segment.start, segment.end, speaker)
                           for segment, _, speaker in diarization.itertracks(yield_label=True)]
        
        # Transcribe with timestamps
        result = whisper_timestamped.transcribe(
            whisper_model,
            audio_array,
            language="en",
            vad=True,  # Voice activity detection
            compute_word_confidence=True,
            beam_size=5  # Increase beam size for better accuracy
        )

        # Match transcription segments with speakers
        segments = []
        for segment in result["segments"]:
            # Find matching speaker from diarization
            speaker = "Unknown"
            for start, end, spk in speaker_segments:
                if segment["start"] >= start and segment["end"] <= end:
                    speaker = f"Speaker {spk}"
                    break

            segments.append(TranscriptionSegment(
                speaker=speaker,
                start=segment["start"],
                end=segment["end"],
                text=segment["text"],
                confidence=segment["confidence"]
            ))

        # Combine all text with speaker attribution
        full_text = ""
        current_speaker = ""
        for segment in segments:
            if segment.speaker != current_speaker:
                full_text += f"\n{segment.speaker}: "
                current_speaker = segment.speaker
            full_text += segment.text + " "

        return TranscriptionResponse(
            segments=segments,
            full_text=full_text.strip(),
            metadata={
                "model": "whisper-large-v3",
                "timestamp": datetime.utcnow().isoformat(),
                "audio_duration": result["duration"],
                "language": result["language"]
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    return await process_audio(contents)

@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    await websocket.accept()
    
    buffer = []
    buffer_duration = 0
    MAX_BUFFER_DURATION = 30  # Process in 30-second chunks
    
    try:
        while True:
            data = await websocket.receive_bytes()
            
            # Add to buffer
            buffer.append(data)
            # Estimate duration (assuming 16kHz mono audio)
            buffer_duration += len(data) / (16000 * 2)
            
            if buffer_duration >= MAX_BUFFER_DURATION:
                # Concatenate buffer and process
                combined_audio = b"".join(buffer)
                result = await process_audio(combined_audio)
                
                # Send result to client
                await websocket.send_json(result.dict())
                
                # Clear buffer
                buffer = []
                buffer_duration = 0
                
    except Exception as e:
        await websocket.close()
        raise e
