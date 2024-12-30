# MedAssistent Project Structure

```
├── backend/                   # Backend logic
│   ├── app.py               # FastAPI main entry point
│   ├── routes/              # API routes
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── patients.py       # Patient management
│   │   ├── transcription.py   # Whisper transcription
│   │   └── analysis.py       # GPT-4 analysis
│   ├── utils/               # Utility functions
│   │   ├── security.py       # JWT and auth utils
│   │   ├── database.py       # Database utilities
│   │   └── config.py         # Configuration
│   ├── models/              # Database models
│   │   ├── user.py
│   │   └── patient.py
│   ├── schemas/             # Data validation
│   │   ├── auth.py
│   │   ├── patient.py
│   │   └── analysis.py
│   ├── services/            # Business logic
│   │   ├── transcription.py
│   │   └── gpt.py
│   ├── requirements.txt     # Python dependencies
│   └── tests/               # Test cases
│
├── frontend/                  # Frontend logic (Next.js)
│   ├── public/              # Static files
│   ├── src/                 # React source code
│   │   ├── components/       # UI components
│   │   ├── hooks/            # Custom React hooks
│   │   └── utils/            # Frontend utilities
│   ├── package.json
│   └── README.md
│
├── docker-compose.yml          # Docker configuration
└── README.md                   # Project documentation
```

## Key Components

### Backend
- FastAPI application with route handlers
- Database models and migrations
- Authentication with JWT
- Whisper transcription integration
- GPT-4 analysis service

### Frontend
- Next.js with React
- Real-time transcription display
- Patient management interface
- Medical record viewer/editor

### Environment Setup
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/medassistent
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```

### Development
1. Start backend: `cd backend && uvicorn app:app --reload`
2. Start frontend: `cd frontend && npm run dev`
