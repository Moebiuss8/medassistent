from fastapi import APIRouter, Depends, HTTPException
from ....schemas.analysis import SOAPNoteResponse, DiagnosisResponse
from ....services.gpt import gpt_service
from ....api import deps

router = APIRouter()

@router.post("/analyze-transcription", response_model=SOAPNoteResponse)
async def analyze_transcription(
    transcription: str,
    current_user = Depends(deps.get_current_active_user)
):
    try:
        result = await gpt_service.process_transcription(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance-diagnosis", response_model=DiagnosisResponse)
async def enhance_diagnosis(
    soap_note: str,
    current_user = Depends(deps.get_current_active_user)
):
    try:
        result = await gpt_service.enhance_diagnosis(soap_note)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))