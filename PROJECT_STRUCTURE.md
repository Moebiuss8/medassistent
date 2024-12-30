# MedAssistent Project Structure

## Overview
API-driven medical assistant application with real-time transcription and GPT-4 analysis.

## Architecture
```
medassistent/
├── backend/                   # Main FastAPI application
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py       # Authentication
│   │   │       │   ├── users.py      # User management
│   │   │       │   ├── patients.py   # Patient records
│   │   │       │   ├── transcription.py  # Audio processing
│   │   │       │   └── analysis.py   # GPT-4 analysis
│   │   │       └── api.py
│   │   ├── core/             # Core functionality
│   │   │   └── security.py   # JWT handling
│   │   ├── db/               # Database
│   │   │   ├── models/
│   │   │   │   ├── user.py
│   │   │   │   └── patient.py
│   │   │   └── base.py
│   │   ├── schemas/          # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── token.py
│   │   │   └── analysis.py
│   │   └── services/         # Business logic
│   │       ├── transcription.py
│   │       └── gpt.py
│   ├── alembic/              # Database migrations
│   └── tests/                # Backend tests
├── ml_service/              # ML microservices
│   └── transcription/       # Whisper service
│       ├── main.py
│       └── Dockerfile
└── docs/                    # Documentation

## Key Components

### Backend Services
1. Authentication (JWT)
2. User Management
3. Patient Records
4. Medical Records
5. Real-time Transcription
6. GPT-4 Analysis

### ML Service
1. Whisper ASR Large-v3
2. Real-time Audio Processing
3. Structured Output Generation

### Data Models
1. Users
   - Authentication
   - Role-based access
2. Patients
   - Demographics
   - Medical history
3. Medical Records
   - Visit records
   - SOAP notes
   - Transcriptions

## API Endpoints

### Authentication
- POST /api/v1/token

### Users
- GET /api/v1/users/
- POST /api/v1/users/
- GET /api/v1/users/me
- PUT /api/v1/users/me

### Patients
- GET /api/v1/patients/
- POST /api/v1/patients/
- GET /api/v1/patients/{id}
- PUT /api/v1/patients/{id}
- DELETE /api/v1/patients/{id}

### Medical Records
- GET /api/v1/patients/{id}/records
- POST /api/v1/patients/{id}/records
- GET /api/v1/patients/{id}/records/{record_id}
- PUT /api/v1/patients/{id}/records/{record_id}

### Transcription
- POST /api/v1/transcribe
- WS /api/v1/ws/transcribe

### Analysis
- POST /api/v1/analyze-transcription
- POST /api/v1/enhance-diagnosis

## Environment Variables
```env
# Backend
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/medassistent
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key

# ML Service
HUGGING_FACE_TOKEN=your-token  # Optional
```

## Development Setup
1. Backend: docker-compose up in backend/
2. ML Service: docker-compose up in ml_service/transcription/
3. Database migrations: alembic upgrade head
