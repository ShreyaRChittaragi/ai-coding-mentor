from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Coding Mentor"
    DEBUG: bool = True
    GROQ_API_KEY: str = ""
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_URL: str = "https://api.hindsight.vectorize.io"
    HINDSIGHT_LLM_PROVIDER: str = "groq"
    HINDSIGHT_LLM_MODEL: str = "openai/gpt-oss-20b"
    HINDSIGHT_BASE_URL: str = "http://localhost:8888"  # ← add this

    class Config:
        env_file = ".env"
        extra = "ignore"   # ← also add this so unknown .env vars never crash the app again

settings = Settings()