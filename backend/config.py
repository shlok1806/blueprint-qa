from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/blueprintqa"
    anthropic_api_key: str = ""
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 50
    max_pages_per_document: int = 10
    storage_backend: str = "local"  # "local" | "azure"
    azure_connection_string: str = ""
    azure_container_name: str = "blueprintqa"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
