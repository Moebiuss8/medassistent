from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, schemas
from app.models.medical_record import MedicalRecord

router = APIRouter()

@router.get("/patient/{patient_id}/records", response_model=List[schemas.MedicalRecord])
def get_patient_records(patient_id: int, db: Session = Depends(deps.get_db)):
    return crud.medical_record.get_by_patient(db, patient_id=patient_id)

@router.post("/patient/{patient_id}/records", response_model=schemas.MedicalRecord)
def create_record(patient_id: int, record: schemas.MedicalRecordCreate, db: Session = Depends(deps.get_db)):
    return crud.medical_record.create_with_patient(db, obj_in=record, patient_id=patient_id)

@router.get("/records/{record_id}", response_model=schemas.MedicalRecord)
def get_record(record_id: int, db: Session = Depends(deps.get_db)):
    record = crud.medical_record.get(db, id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/records/{record_id}", response_model=schemas.MedicalRecord)
def update_record(record_id: int, record: schemas.MedicalRecordUpdate, db: Session = Depends(deps.get_db)):
    db_record = crud.medical_record.get(db, id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return crud.medical_record.update(db, db_obj=db_record, obj_in=record)