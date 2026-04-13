from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv

# Load .env file explicitly if needed, but pydantic-settings handles it
load_dotenv()

class Settings(BaseSettings):
    """
    Settings class for the FLL Lesson Builder Agent.
    Values are loaded from environment variables or a .env file.
    """
    POE_API_KEY: str
    TAVILY_API_KEY: Optional[str] = None
    LLM_MODEL: str = "Claude-Sonnet-4-6"
    LLM_MAX_TOKENS: int = 4096
    LLM_MAX_RETRIES: int = 3
    OUTPUT_BASE_PATH: str = "~/Documents/FLL_Lessons"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Export a single settings instance
settings = Settings()
