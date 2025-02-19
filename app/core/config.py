# /Users/tef/Projects/cta/back/app/core/config.py
from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized configuration management for the CTA backend.
    
    Design Principles:
    - Type-safe configuration via Pydantic
    - Environment variable overrides
    - Sensible defaults
    - Support for multiple deployment environments
    """
    
    # AI Model Configuration
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str | None = None
    
    # Preferred AI Model Selection
    MODEL_NAME: Literal[
        'claude-3-sonnet-20240229', 
        'claude-3-opus-20240229', 
        'gpt-4-turbo', 
        'gpt-4o'
    ] = 'claude-3-sonnet-20240229'
    
    # Application Settings
    APP_NAME: str = "CTA Travel Companion"
    ENV: Literal['development', 'production', 'testing'] = 'development'
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    POSTGRES_USER: str = "cta"
    POSTGRES_PASSWORD: str = "development_only"
    POSTGRES_DB: str = "cta"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Security Settings
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Image Processing Configuration
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg", 
        "image/png", 
        "image/webp"
    ]
    
    # Logging Configuration
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    
    # Feature Flags
    ENABLE_IMAGE_ANALYSIS: bool = True
    ENABLE_VECTOR_SEARCH: bool = True
    ENABLE_CHAT_HISTORY: bool = True
    
    # Model configuration for Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'  # Ignore extra environment variables
    )

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# Create a singleton settings instance
settings = Settings()