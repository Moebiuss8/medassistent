from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    
    # Medical specific fields
    medical_license = Column(String, unique=True)
    specialty = Column(String)
    
    # Relationships
    patients = relationship("Patient", back_populates="doctor")
    visits = relationship("Visit", back_populates="doctor")