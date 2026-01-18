from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # -----------------------------
    # Application
    # -----------------------------
    app_name: str = Field(..., env="APP_NAME")
    app_env: str = Field(..., env="APP_ENV")
    app_log_level: str = Field("INFO", env="APP_LOG_LEVEL")

    # -----------------------------
    # Backend
    # -----------------------------
    backend_host: str = Field(..., env="BACKEND_HOST")
    backend_port: int = Field(..., env="BACKEND_PORT")

    # -----------------------------
    # Database
    # -----------------------------
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")

    # -----------------------------
    # Redis
    # -----------------------------
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")

    # -----------------------------
    # Inference
    # -----------------------------
    inference_provider: str = Field(..., env="INFERENCE_PROVIDER")
    inference_base_url: str = Field(..., env="INFERENCE_BASE_URL")
    inference_model: str = Field(..., env="INFERENCE_MODEL")
    inference_timeout_seconds: int = Field(..., env="INFERENCE_TIMEOUT_SECONDS")

    # -----------------------------
    # Retrieval
    # -----------------------------
    embedding_model: str = Field(..., env="EMBEDDING_MODEL")
    faiss_index_path: str = Field(..., env="FAISS_INDEX_PATH")

    # -----------------------------
    # Security
    # -----------------------------
    enable_pii_detection: bool = Field(True, env="ENABLE_PII_DETECTION")
    enable_prompt_injection_guard: bool = Field(True, env="ENABLE_PROMPT_INJECTION_GUARD")
    max_input_tokens: int = Field(..., env="MAX_INPUT_TOKENS")

    # -----------------------------
    # Memory
    # -----------------------------
    short_term_memory_ttl_seconds: int = Field(..., env="SHORT_TERM_MEMORY_TTL_SECONDS")
    long_term_memory_enabled: bool = Field(True, env="LONG_TERM_MEMORY_ENABLED")
    summary_memory_enabled: bool = Field(True, env="SUMMARY_MEMORY_ENABLED")

    # -----------------------------
    # Audit
    # -----------------------------
    enable_audit_logs: bool = Field(True, env="ENABLE_AUDIT_LOGS")
    audit_log_path: str = Field(..., env="AUDIT_LOG_PATH")


settings = Settings()
