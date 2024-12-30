from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MedAssistent"
    VERSION: str = "0.1.0"
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
