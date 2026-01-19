from pydantic import BaseSettings


class Settings(BaseSettings):
    # --------------------
    # App
    # --------------------
    APP_NAME: str = "Enterprise Financial Decision Assistant"
    ENV: str = "local"

    # --------------------
    # Postgres
    # --------------------
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    # --------------------
    # Derived
    # --------------------
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
