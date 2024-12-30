from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(DateTime, default=datetime.utcnow)
    chief_complaint = Column(Text)
    history = Column(Text)
    examination = Column(Text)
    diagnosis = Column(Text)
    plan = Column(Text)
    transcription = Column(Text)
    
    patient = relationship("Patient", back_populates="records")