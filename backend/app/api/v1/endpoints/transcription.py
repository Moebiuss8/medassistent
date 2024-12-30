from typing import Any
from fastapi import APIRouter, File, UploadFile, WebSocket, Depends
from ....services.transcription import transcription_service
from ....api import deps
from ....db.models.user import User
from ....schemas.transcription import TranscriptionResponse

router = APIRouter()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Transcribe an audio file."""
    contents = await file.read()
    result = await transcription_service.transcribe_file(contents)
    return result

@router.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    """Handle live audio transcription through WebSocket."""
    await websocket.accept()
    
    try:
        async for result in transcription_service.process_live_audio(websocket):
            await websocket.send_json(result)
    except Exception as e:
        await websocket.close(code=1001, reason=str(e))
