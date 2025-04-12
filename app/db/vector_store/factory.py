from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config_manager import ConfigManager
from app.db.vector_store.base import VectorStore
from app.db.vector_store.pinecone import PineconeVectorStore
from app.db.vector_store.postgres import PostgresVectorStore


class VectorStoreFactory:
    @staticmethod
    def create_vector_store(session: AsyncSession | None = None) -> VectorStore:
        config = ConfigManager.get_config()

        if config.vector_store_type == "postgres":
            if not session:
                raise ValueError("PostgresVectorStore requires a database session")
            return PostgresVectorStore(session)
        elif config.vector_store_type == "pinecone":
            from app.core.config import settings

            return PineconeVectorStore(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT,
                index_name=settings.PINECONE_INDEX_NAME,
            )
        else:
            raise ValueError(
                f"Unsupported vector store type: {config.vector_store_type}"
            )
