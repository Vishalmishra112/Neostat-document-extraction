import os

class Settings:
    PROJECT_NAME: str = "Intelligent Document Extraction Platform"
    API_V1_STR: str = "/api/v1"
    #YOUR API KEY HERE
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./documents.db")
    MAX_PAGE_LIMIT: int = 3

settings = Settings()