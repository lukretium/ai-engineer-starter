from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.vector_store.base import VectorStore
from app.db.vector_store.pinecone import PineconeVectorStore
from app.db.vector_store.postgres import PostgresVectorStore


class VectorStoreFactory:
    @staticmethod
    def create_vector_store(session: AsyncSession | None = None) -> VectorStore:
        vector_store_type = settings.VECTOR_STORE_TYPE.lower()

        if vector_store_type == "postgres":
            if not session:
                raise ValueError("PostgresVectorStore requires a database session")
            return PostgresVectorStore(session)
        elif vector_store_type == "pinecone":
            return PineconeVectorStore(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT,
                index_name=settings.PINECONE_INDEX_NAME,
            )
        else:
            raise ValueError(f"Unsupported vector store type: {vector_store_type}")
