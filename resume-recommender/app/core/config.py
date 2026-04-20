from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # -----------------------------
    # Database
    # -----------------------------
    MONGO_URI: str = "mongodb://localhost:27017/"
    DB_NAME: str = "resume_db"

    # -----------------------------
    # LLM Configuration
    # -----------------------------
    LLM_PROVIDER: str = "openai"   # openai | local

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Local (Ollama)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    # -----------------------------
    # App Settings
    # -----------------------------
    APP_NAME: str = "AI Resume Recommender"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignore unknown env variables


# -----------------------------
# Cached Settings Instance
# -----------------------------
@lru_cache
def get_settings():
    return Settings()


# Singleton-like access
settings = get_settings()