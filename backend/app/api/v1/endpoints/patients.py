from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....api import deps
from ....schemas.patient import (
    Patient,
    PatientCreate,
    PatientUpdate,
    PatientWithRecords,
    MedicalRecord,
    MedicalRecordCreate,
    MedicalRecordUpdate
)
from ....db.models.patient import Patient as PatientModel
from ....db.models.patient import MedicalRecord as MedicalRecordModel

router = APIRouter()

@router.get("/", response_model=List[Patient])
def get_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Retrieve patients."""
    patients = db.query(PatientModel).offset(skip).limit(limit).all()
    return patients

@router.post("/", response_model=Patient)
def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: PatientCreate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Create new patient."""
    patient = PatientModel(**patient_in.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/{patient_id}", response_model=PatientWithRecords)
def get_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Get patient by ID."""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    patient_in: PatientUpdate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Update patient."""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for field, value in patient_in.dict(exclude_unset=True).items():
        setattr(patient, field, value)
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Delete patient."""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

# Medical Records endpoints
@router.get("/{patient_id}/records", response_model=List[MedicalRecord])
def get_patient_records(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Get patient's medical records."""
    records = db.query(MedicalRecordModel).filter(MedicalRecordModel.patient_id == patient_id).all()
    return records

@router.post("/{patient_id}/records", response_model=MedicalRecord)
def create_medical_record(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    record_in: MedicalRecordCreate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Create new medical record for patient."""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    record = MedicalRecordModel(
        **record_in.dict(),
        patient_id=patient_id,
        doctor_id=current_user.id
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/{patient_id}/records/{record_id}", response_model=MedicalRecord)
def get_medical_record(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    record_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Get specific medical record."""
    record = db.query(MedicalRecordModel).filter(
        MedicalRecordModel.patient_id == patient_id,
        MedicalRecordModel.id == record_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@router.put("/{patient_id}/records/{record_id}", response_model=MedicalRecord)
def update_medical_record(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    record_id: int,
    record_in: MedicalRecordUpdate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """Update medical record."""
    record = db.query(MedicalRecordModel).filter(
        MedicalRecordModel.patient_id == patient_id,
        MedicalRecordModel.id == record_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    for field, value in record_in.dict(exclude_unset=True).items():
        setattr(record, field, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
