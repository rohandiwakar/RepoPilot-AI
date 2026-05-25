from pydantic import field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LLM_MAX_RETRIES: int = 2
    LLM_RETRY_BASE_SECONDS: float = 2.0
    LLM_RETRY_MAX_SECONDS: float = 30.0
    GITHUB_TOKEN: str = ""
    APP_NAME: str = "RepoPilot AI"
    DEBUG: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str) and value.lower() in {"release", "prod", "production"}:
            return False
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
