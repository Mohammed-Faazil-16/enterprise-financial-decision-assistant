from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Enterprise Financial Decision Assistant"
    app_env: str = Field(default="local")
    debug: bool = False

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "efda"
    postgres_user: str = "efda_user"
    postgres_password: str = "efda_password"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
