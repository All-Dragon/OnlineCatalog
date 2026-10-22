from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_bot_token: SecretStr = Field(min_length=1)
    telegram_admin_id: int = Field(gt=0)
    telegram_webhook_secret: SecretStr = Field(min_length=32)

    api_base_url: AnyHttpUrl = "http://127.0.0.1:8000"
    api_service_token: SecretStr = Field(min_length=32)

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_to_file: bool = True
    log_dir: Path = Field(
        default=Path("logs/bot"),
        validation_alias="BOT_LOG_DIR",
    )
    log_max_bytes: int = Field(default=10 * 1024 * 1024, gt=0)
    log_max_files: int = Field(default=5, ge=2, le=5)

    mini_app_url: HttpUrl

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
