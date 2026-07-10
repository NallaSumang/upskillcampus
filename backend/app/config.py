"""
Application configuration via environment variables.

Uses Pydantic BaseSettings for type-safe config with .env file support.
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    # Application
    APP_NAME: str = "Smart Factory Dashboard API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./factory.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

