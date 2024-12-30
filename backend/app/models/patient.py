from sqlalchemy import Column, Integer, String, Date, Boolean
from app.db.base_class import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, index=True)
    phone = Column(String)
    is_active = Column(Boolean, default=True)