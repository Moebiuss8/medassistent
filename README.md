# MedAssistent

A comprehensive medical assistant application that supports doctors during patient visits with real-time analysis, documentation, and clinical decision support.

## Core Features

- 🎙️ Real-time voice transcription of doctor-patient conversations
- 📝 Automated clinical note generation
- 🤖 AI-powered symptom analysis and diagnosis suggestions
- 📊 Interactive visualization of patient data
- 📱 Mobile-first responsive design
- 🔒 HIPAA-compliant data handling

## Project Structure

```
medassistent/
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/             # Core functionality
│   │   ├── db/               # Database models and migrations
│   │   ├── ml/               # Machine learning models
│   │   └── services/         # Business logic
│   └── tests/                # Backend tests
├── frontend/                 # Next.js application
│   ├── components/           # React components
│   ├── hooks/               # Custom React hooks
│   ├── pages/               # Next.js pages
│   └── public/              # Static assets
├── ml_service/              # Separate ML microservice
│   ├── models/              # Trained models
│   └── training/            # Model training scripts
└── docs/                    # Documentation
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 16+
- Python 3.9+
- PostgreSQL 13+

### Installation

Coming soon...

## License

MIT