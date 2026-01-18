from abc import ABC, abstractmethod


class InferenceClient(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        context: list[str] | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        pass
