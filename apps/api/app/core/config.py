from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str

    postgres_host: str = "localhost"
    postgres_port: int = 5432

    s3_endpoint_url: str
    s3_bucket_name: str
    s3_access_key: str
    s3_secret_key: SecretStr
    s3_region: str = "us-east-1"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_to_file: bool = True
    log_dir: Path = Path("logs/api")
    log_max_bytes: int = Field(default=10 * 1024 * 1024, gt=0)
    log_max_files: int = Field(default=5, ge=2, le=5)

    api_service_token: SecretStr = Field(min_length=32)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


settings = Settings()
