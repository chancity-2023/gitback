"""
Configuration management using Pydantic Settings.
Environment variables are loaded from .env file or system environment.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""
    
    # Appwrite Configuration
    appwrite_endpoint: str = "https://nyc.cloud.appwrite.io/v1"
    appwrite_project_id: str
    appwrite_api_key: str
    appwrite_database_id: str
    appwrite_collection_id: str
    
    # CORS Configuration
    cors_origins: str = "https://rahulj-crypto.github.io"
    
    # Application Configuration
    environment: str = "production"
    debug: bool = False
    app_name: str = "Tournament Registration API"
    app_version: str = "1.0.0"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 10
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


# Global settings instance
settings = Settings()
