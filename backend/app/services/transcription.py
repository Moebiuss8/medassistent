from typing import Optional, Dict, Any
from httpx import AsyncClient
from fastapi import WebSocket
import json
from ..config import settings

class TranscriptionService:
    def __init__(self):
        self.base_url = settings.TRANSCRIPTION_SERVICE_URL
        self.client = AsyncClient(base_url=self.base_url)
    
    async def transcribe_file(self, file_content: bytes) -> Dict[str, Any]:
        """Transcribe an audio file using the transcription service."""
        try:
            files = {"file": file_content}
            response = await self.client.post("/transcribe", files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    async def process_live_audio(self, websocket: WebSocket) -> AsyncGenerator[Dict[str, Any], None]:
        """Process live audio stream using the transcription service."""
        async with AsyncClient() as client:
            async with client.websocket_connect(f"{self.base_url}/ws/transcribe") as ws:
                try:
                    while True:
                        # Forward audio data from client to transcription service
                        data = await websocket.receive_bytes()
                        await ws.send_bytes(data)
                        
                        # Forward transcription results back to client
                        result = await ws.receive_json()
                        yield result
                except Exception as e:
                    raise Exception(f"Live transcription failed: {str(e)}")

transcription_service = TranscriptionService()
