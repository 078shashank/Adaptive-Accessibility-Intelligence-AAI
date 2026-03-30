"""Backend Configuration"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App Configuration
    APP_NAME: str = "Adaptive Accessibility Intelligence (AAI)"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "chrome-extension://*",  # Allow Chrome extension
        "moz-extension://*"     # Allow Firefox extension (future)
    ]
    
    # AI Models
    HF_MODEL_NAME: str = "facebook/bart-large-cnn"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
