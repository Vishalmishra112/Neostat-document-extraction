import os

class Settings:
    PROJECT_NAME: str = "Intelligent Document Extraction Platform"
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()