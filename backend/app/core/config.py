from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

# FORCE asyncpg (NO psycopg2 allowed)
settings.database_url = settings.database_url.replace(
    "postgresql+psycopg2", "postgresql+asyncpg"
)
