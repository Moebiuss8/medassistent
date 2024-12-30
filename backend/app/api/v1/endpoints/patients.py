from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, schemas
from app.models.patient import Patient

router = APIRouter()

@router.get("/", response_model=List[schemas.Patient])
def get_patients(db: Session = Depends(deps.get_db)):
    return crud.patient.get_multi(db)

@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(deps.get_db)):
    return crud.patient.create(db, obj_in=patient)

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(deps.get_db)):
    patient = crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(deps.get_db)):
    db_patient = crud.patient.get(db, id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.patient.update(db, db_obj=db_patient, obj_in=patient)

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(deps.get_db)):
    patient = crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    crud.patient.remove(db, id=patient_id)
    return {"success": True}