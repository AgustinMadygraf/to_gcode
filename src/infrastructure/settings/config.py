"""
Path: src/infrastructure/settings/config.py
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_TITLE: str = "to_gcode API"
    APP_DESCRIPTION: str = "Conversor de SVG a G-code para Plotters"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    GCODE_TRUNCATE_LIMIT: int = 0
    ARC_TOLERANCE: float = 2.0

    DATABASE_URL: str = "sqlite:///./to_gcode.db"

    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
