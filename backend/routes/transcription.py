from fastapi import APIRouter, File, UploadFile, WebSocket
from services.transcription import transcription_service

router = APIRouter()

@router.post("/audio")
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    return await transcription_service.transcribe_audio(contents)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await transcription_service.handle_stream(websocket)