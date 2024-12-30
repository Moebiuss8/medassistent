import whisper_timestamped
from fastapi import WebSocket
from typing import List, Dict, Any

class TranscriptionService:
    def __init__(self):
        self.model = whisper_timestamped.load_model("large-v3")

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        audio_array = whisper_timestamped.load_audio(audio_data)
        result = whisper_timestamped.transcribe(
            self.model,
            audio_array,
            language="en",
            vad=True,
            compute_word_confidence=True,
            beam_size=5
        )
        return self._format_result(result)

    async def handle_stream(self, websocket: WebSocket):
        buffer = []
        buffer_duration = 0
        MAX_BUFFER_DURATION = 30

        while True:
            data = await websocket.receive_bytes()
            buffer.append(data)
            buffer_duration += len(data) / (16000 * 2)

            if buffer_duration >= MAX_BUFFER_DURATION:
                combined_audio = b"".join(buffer)
                result = await self.transcribe_audio(combined_audio)
                await websocket.send_json(result)
                buffer = []
                buffer_duration = 0

    def _format_result(self, result: Dict) -> Dict[str, Any]:
        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }

transcription_service = TranscriptionService()