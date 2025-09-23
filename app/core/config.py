from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'.env.{Literal["dev", "prod"]}',
        env_file_encoding='utf-8'
    )

    ENV: str = "dev"
    CORS_ORIGINS: List[str] = []

settings = Settings()
