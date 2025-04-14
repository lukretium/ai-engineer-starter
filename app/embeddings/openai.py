from openai import AsyncOpenAI

from .base import EmbeddingProvider


class OpenAIEmbedding(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def get_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model, input=text, encoding_format="float"
        )
        return response.data[0].embedding
