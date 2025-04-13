from app.core.settings import settings

from .base import EmbeddingProvider
from .huggingface import HuggingFaceEmbedding
from .ollama import OllamaEmbedding
from .openai import OpenAIEmbedding
from .types import EmbeddingType


class EmbeddingFactory:
    @staticmethod
    def create_embedding_provider() -> EmbeddingProvider:
        embedding_type = settings.EMBEDDING_TYPE.lower()

        if embedding_type == EmbeddingType.OPENAI:
            return OpenAIEmbedding(
                api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_EMBEDDING_MODEL
            )
        elif embedding_type == EmbeddingType.HUGGINGFACE:
            return HuggingFaceEmbedding(model_name=settings.HUGGINGFACE_EMBEDDING_MODEL)
        elif embedding_type == EmbeddingType.OLLAMA:
            return OllamaEmbedding(
                model=settings.OLLAMA_EMBEDDING_MODEL, base_url=settings.OLLAMA_BASE_URL
            )
        else:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")
