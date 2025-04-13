from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        pass
