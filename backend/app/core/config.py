import os

class Settings:
    PROJECT_NAME: str = "Intelligent Document Extraction Platform"
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
settings = Settings()