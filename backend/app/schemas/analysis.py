from pydantic import BaseModel

class SOAPNoteResponse(BaseModel):
    soap_note: str
    model_used: str

class DiagnosisResponse(BaseModel):
    analysis: str
    model_used: str