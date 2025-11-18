"""
Configuration settings for the Carbon Footprint Tracker application.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # APIs
    openai_api_key: str = ""
    climatiq_api_key: str = ""

    # Database
    database_url: str = "sqlite:///./carbon_tracker.db"

    # Application
    app_env: str = "development"
    secret_key: str = "dev-secret-key-change-in-production"

    # API Settings
    climatiq_base_url: str = "https://api.climatiq.io"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
