from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, patients, transcription, analysis
from utils.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
