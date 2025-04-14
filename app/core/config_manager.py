from enum import Enum
from typing import Literal

from pydantic import BaseModel

from app.embeddings.types import EmbeddingType


class VectorStoreType(str, Enum):
    POSTGRES = "postgres"
    PINECONE = "pinecone"


class LLMType(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class Config(BaseModel):
    vector_store_type: VectorStoreType
    llm_type: LLMType
    embedding_type: EmbeddingType
    source: Literal["env", "ui"] = "env"


class ConfigManager:
    _instance = None
    _config: Config | None = None

    # Singleton pattern
    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_config(cls) -> Config:
        if cls._config is None:
            from app.core.config import settings

            cls._config = Config(
                vector_store_type=VectorStoreType(settings.VECTOR_STORE_TYPE),
                llm_type=LLMType(settings.LLM_TYPE),
                embedding_type=EmbeddingType(settings.EMBEDDING_TYPE),
                source="env",
            )
        return cls._config

    @classmethod
    def update_from_ui(
        cls, vector_store_type: str, llm_type: str, embedding_type: str
    ) -> None:
        from app.core.config import settings

        # Update the config
        cls._config = Config(
            vector_store_type=VectorStoreType(vector_store_type),
            llm_type=LLMType(llm_type),
            embedding_type=EmbeddingType(embedding_type),
            source="ui",
        )

        # Update the actual settings object
        settings.VECTOR_STORE_TYPE = vector_store_type
        settings.LLM_TYPE = llm_type
        settings.EMBEDDING_TYPE = EmbeddingType(embedding_type)
