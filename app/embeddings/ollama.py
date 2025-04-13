import aiohttp

from .base import EmbeddingProvider

HTTP_OK = 200


class OllamaEmbedding(EmbeddingProvider):
    def __init__(
        self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_embedding(self, text: str) -> list[float]:
        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.session.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model, "prompt": text},
        ) as response:
            if response.status != HTTP_OK:
                raise Exception(f"Ollama API error: {await response.text()}")
            result = await response.json()
            return result["embedding"]
