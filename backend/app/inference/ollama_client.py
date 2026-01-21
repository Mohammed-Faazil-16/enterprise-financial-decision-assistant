import httpx
import os

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = "llama3.2-vision:11b-instruct-q4_K_M"

    async def generate(self, prompt: str, images: list[str] | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if images:
            payload["images"] = images  # base64 images later

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json()["response"]
