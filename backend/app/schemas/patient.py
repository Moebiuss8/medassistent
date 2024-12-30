from pydantic import BaseModel
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: Optional[str] = None
    phone: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True