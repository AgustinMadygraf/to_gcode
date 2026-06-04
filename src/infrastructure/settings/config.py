"""
Path: src/infrastructure/settings/config.py
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    APP_TITLE: str = "to_gcode API"
    APP_DESCRIPTION: str = "Conversor de SVG a G-code para Plotters (Clean Architecture)"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database Settings
    DATABASE_URL: str = "sqlite:///./to_gcode.db"

    # API Settings
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
