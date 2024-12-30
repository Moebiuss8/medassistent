from .base import Base, get_db
from .models.user import User
from .models.patient import Patient, MedicalRecord

# Import all models here for Alembic autogenerate feature