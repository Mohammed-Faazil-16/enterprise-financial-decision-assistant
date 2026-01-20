from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "enterprise-financial-decision-assistant"
    app_env: str = "local"
    app_log_level: str = "INFO"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    redis_host: str
    redis_port: int
    redis_db: int

    inference_provider: str
    inference_base_url: str
    inference_model: str
    inference_timeout_seconds: int = 120

    embedding_model: str
    faiss_index_path: str

    enable_audit_logs: bool = True

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
