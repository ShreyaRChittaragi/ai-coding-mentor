from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Coding Mentor"
    DEBUG: bool = True

    # Groq - for LLM feedback (Person 3)
    GROQ_API_KEY: str = ""

    # Hindsight Cloud - for memory (Person 1)
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_BASE_URL: str = "https://api.hindsight.vectorize.io"  # cloud default

    # Hindsight needs to know which LLM to use internally
    HINDSIGHT_LLM_PROVIDER: str = "groq"
    HINDSIGHT_LLM_MODEL: str = "openai/gpt-oss-20b"  # recommended for Groq

    class Config:
        env_file = ".env"

settings = Settings()