from openai import AsyncOpenAI

from app.core.config import settings


class EmbeddingsService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = (
            "text-embedding-3-small"  # or "text-embedding-3-large" for better quality
        )

    async def get_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model, input=text, encoding_format="float"
        )
        return response.data[0].embedding
