from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/blueprintqa"

    # LLM provider: NVIDIA NIM, which exposes an OpenAI-compatible API.
    nvidia_api_key: str = ""
    llm_base_url: str = "https://integrate.api.nvidia.com/v1"
    # Must be vision-capable: pages are sent as images.
    llm_vision_model: str = "meta/llama-3.2-11b-vision-instruct"
    llm_max_tokens: int = 2048
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 50
    max_pages_per_document: int = 10
    storage_backend: str = "local"
    azure_connection_string: str = ""
    azure_container_name: str = "blueprintqa"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
