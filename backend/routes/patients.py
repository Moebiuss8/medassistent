from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from utils.security import get_current_user
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
async def get_patients(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Patient).all()

@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
