from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class TranscriptionSegment(BaseModel):
    speaker: str
    start: float
    end: float
    text: str
    confidence: float

class TranscriptionResponse(BaseModel):
    segments: List[TranscriptionSegment]
    full_text: str
    metadata: Dict[str, Any]
