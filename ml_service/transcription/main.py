import whisper
import numpy as np
import torch
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import asyncio
import json
from typing import Dict
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import soundfile as sf
import io

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model
model = whisper.load_model("base")

# Store active connections
connections: Dict[str, WebSocket] = {}

async def process_audio(audio_data: bytes, session_id: str):
    try:
        # Convert audio bytes to numpy array
        audio_np, _ = sf.read(io.BytesIO(audio_data))
        
        # Ensure audio is mono
        if len(audio_np.shape) > 1:
            audio_np = np.mean(audio_np, axis=1)
        
        # Normalize audio
        audio_np = audio_np / np.max(np.abs(audio_np))
        
        # Transcribe with Whisper
        result = model.transcribe(audio_np)
        
        # Send transcription back to client
        if session_id in connections:
            await connections[session_id].send_json({
                "type": "transcript",
                "text": result["text"],
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        print(f"Error processing audio: {e}")
        if session_id in connections:
            await connections[session_id].send_json({
                "type": "error",
                "message": str(e)
            })

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Generate unique session ID
    session_id = str(datetime.now().timestamp())
    connections[session_id] = websocket
    
    try:
        while True:
            # Receive audio chunk
            audio_data = await websocket.receive_bytes()
            
            # Process audio asynchronously
            asyncio.create_task(process_audio(audio_data, session_id))
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if session_id in connections:
            del connections[session_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)