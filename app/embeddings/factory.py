from app.core.config_manager import ConfigManager

from .base import EmbeddingProvider
from .huggingface import HuggingFaceEmbedding
from .ollama import OllamaEmbedding
from .openai import OpenAIEmbedding
from .types import EmbeddingType


class EmbeddingFactory:
    @staticmethod
    def create_embedding_provider() -> EmbeddingProvider:
        config = ConfigManager.get_config()
        embedding_type = config.embedding_type.value.lower()

        if embedding_type == EmbeddingType.OPENAI:
            from app.core.config import settings

            return OpenAIEmbedding(
                api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_EMBEDDING_MODEL
            )
        elif embedding_type == EmbeddingType.HUGGINGFACE:
            from app.core.config import settings

            return HuggingFaceEmbedding(model_name=settings.HUGGINGFACE_EMBEDDING_MODEL)
        elif embedding_type == EmbeddingType.OLLAMA:
            from app.core.config import settings

            return OllamaEmbedding(
                model=settings.OLLAMA_EMBEDDING_MODEL, base_url=settings.OLLAMA_BASE_URL
            )
        else:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")
