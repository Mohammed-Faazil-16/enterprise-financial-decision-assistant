import httpx
from app.core.config import settings


class OllamaClient:
    """
    Ollama inference client using the correct Docker API endpoint: /api/generate
    """

    def __init__(self) -> None:
        self.base_url = settings.inference_base_url.rstrip("/")
        self.model = settings.inference_model
        self.timeout = settings.inference_timeout_seconds

    async def generate(self, prompt: str) -> dict:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return {
            "response": data.get("response", "")
        }
