from typing import Dict, Any
from openai import AsyncOpenAI
from ..config import settings

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"

    async def process_transcription(self, transcription: str) -> Dict[str, Any]:
        system_prompt = ("""
You are a medical transcription assistant. Analyze the conversation and extract:
1. Chief complaints
2. Symptoms and their duration
3. Medical history
4. Current medications
5. Allergies
6. Vital signs mentioned
7. Physical examination findings
8. Assessment
9. Plan

Format as a structured SOAP note. Maintain medical accuracy and terminology.
        """)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcription}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            return {
                "soap_note": response.choices[0].message.content,
                "model_used": self.model
            }
        except Exception as e:
            raise Exception(f"GPT processing failed: {str(e)}")

    async def enhance_diagnosis(self, soap_note: str) -> Dict[str, Any]:
        system_prompt = ("""
You are a medical diagnosis assistant. Based on the SOAP note:
1. Suggest potential differential diagnoses
2. Recommend additional tests if needed
3. Suggest evidence-based treatment options
4. Identify any red flags or urgent concerns
5. Provide relevant ICD-10 codes
        """)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": soap_note}
                ],
                temperature=0.1
            )
            return {
                "analysis": response.choices[0].message.content,
                "model_used": self.model
            }
        except Exception as e:
            raise Exception(f"Diagnosis enhancement failed: {str(e)}")

gpt_service = GPTService()
