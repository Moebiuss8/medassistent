from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicalRecordBase(BaseModel):
    visit_date: datetime
    chief_complaint: Optional[str] = None
    history: Optional[str] = None
    examination: Optional[str] = None
    diagnosis: Optional[str] = None
    plan: Optional[str] = None
    transcription: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    patient_id: int

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True