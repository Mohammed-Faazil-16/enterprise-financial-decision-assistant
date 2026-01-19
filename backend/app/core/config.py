from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://redis:6379/0"
    ollama_base_url: str = "http://ollama:11434"

    class Config:
        env_file = ".env"

settings = Settings()
