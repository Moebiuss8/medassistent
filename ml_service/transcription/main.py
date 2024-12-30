from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import whisper_timestamped
import numpy as np
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = whisper_timestamped.load_model("large-v3")

class TranscriptionSegment(BaseModel):
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
        audio_array = whisper_timestamped.load_audio(audio_data)
        
        result = whisper_timestamped.transcribe(
            whisper_model,
            audio_array,
            language="en",
            vad=True,
            compute_word_confidence=True,
            beam_size=5
        )

        segments = [
            TranscriptionSegment(
                start=segment["start"],
                end=segment["end"],
                text=segment["text"],
                confidence=segment["confidence"]
            ) for segment in result["segments"]
        ]

        full_text = " ".join(segment.text for segment in segments)

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
    MAX_BUFFER_DURATION = 30
    
    try:
        while True:
            data = await websocket.receive_bytes()
            buffer.append(data)
            buffer_duration += len(data) / (16000 * 2)
            
            if buffer_duration >= MAX_BUFFER_DURATION:
                combined_audio = b"".join(buffer)
                result = await process_audio(combined_audio)
                await websocket.send_json(result.dict())
                buffer = []
                buffer_duration = 0
                
    except Exception as e:
        await websocket.close()
        raise e
