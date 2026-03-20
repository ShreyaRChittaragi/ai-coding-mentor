from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Coding Mentor"
    DEBUG: bool = True
    GROQ_API_KEY: str = ""
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_URL: str = "https://ui.hindsight.vectorize.io"

    class Config:
        env_file = ".env"

settings = Settings()