from abc import ABC, abstractmethod


class LLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str, context: list[str]) -> str:
        pass
