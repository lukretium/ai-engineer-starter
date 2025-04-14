from sentence_transformers import SentenceTransformer

from .base import EmbeddingProvider


class HuggingFaceEmbedding(EmbeddingProvider):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    async def get_embedding(self, text: str) -> list[float]:
        # Note: SentenceTransformer is synchronous, but we wrap it in async
        embedding = self.model.encode(text)
        return embedding.tolist()
