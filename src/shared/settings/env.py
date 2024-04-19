from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Environment variables settings."""

    DEBUG: bool = True
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    AUTH_SERVICE_URL: str = "http://auth:8001"
    STORAGE_SERVICE_URL: str = "http://storage:8002"

    # PostgreSQL
    POSTGRES_DRIVER: str = "postgresql+psycopg"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5555
    POSTGRES_USER: str = "postgres_user"
    POSTGRES_PASSWORD: str = "postgres_pass"
    POSTGRES_DB: str = "postgres_db"

    @property
    def POSTGRES_URI(self):
        return f"{self.POSTGRES_DRIVER}://\
            {self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/\
            {self.POSTGRES_DB}".replace(" ", "")  # fmt: skip

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )
