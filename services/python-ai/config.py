from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    nestjs_callback_url: str = "http://localhost:3001/ai-callback/decision"
    python_ai_url: str = "http://localhost:8000"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    default_llm_provider: str = "groq"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
