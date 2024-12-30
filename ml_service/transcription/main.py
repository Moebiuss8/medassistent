from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import asyncio
import os
from datetime import datetime
from typing import Dict
import io

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connections: Dict[str, WebSocket] = {}

async def transcribe_audio(audio_data: bytes, session_id: str):
    try:
        # Save audio chunk temporarily
        temp_file = io.BytesIO(audio_data)
        temp_file.name = "audio.wav"
        
        # Transcribe using OpenAI Whisper API
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=temp_file,
            response_format="text"
        )
        
        # Send transcription to client
        if session_id in connections:
            await connections[session_id].send_json({
                "type": "transcript",
                "text": transcript,
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        if session_id in connections:
            await connections[session_id].send_json({
                "type": "error",
                "message": str(e)
            })

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(datetime.now().timestamp())
    connections[session_id] = websocket
    
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            asyncio.create_task(transcribe_audio(audio_data, session_id))
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if session_id in connections:
            del connections[session_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)