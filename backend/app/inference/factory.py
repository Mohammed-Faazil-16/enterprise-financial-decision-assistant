from app.core.config import settings
from app.inference.base import InferenceClient
from app.inference.ollama_client import OllamaClient


def get_inference_client() -> InferenceClient:
    if settings.inference_provider == "ollama":
        return OllamaClient()

    raise ValueError(
        f"Unsupported inference provider: {settings.inference_provider}"
    )
