from transformers import pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class TranscriptAnalysis(BaseModel):
    text: str

@app.post('/analyze')
async def analyze_transcript(data: TranscriptAnalysis):
    # Initialize model
    model = pipeline('text-classification', model='ybelkada/medical-ner')
    
    # Analyze text
    result = model(data.text)
    
    return {"analysis": result}
