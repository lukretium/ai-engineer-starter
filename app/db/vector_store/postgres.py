from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config_manager import ConfigManager
from app.db.postgres.models import Document
from app.db.vector_store.base import VectorStore
from app.embeddings.factory import EmbeddingFactory
from app.schemas.rag import DocumentCreate, DocumentResponse


class PostgresVectorStore(VectorStore):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_provider = EmbeddingFactory.create_embedding_provider()
        self.target_dimension = 1536  # OpenAI's dimension

    def _pad_embedding(self, embedding: list[float]) -> list[float]:
        """Pad the embedding to match the target dimension."""
        current_dim = len(embedding)
        if current_dim < self.target_dimension:
            # Pad with zeros
            padding = [0.0] * (self.target_dimension - current_dim)
            return embedding + padding
        elif current_dim > self.target_dimension:
            # Truncate if larger (shouldn't happen with current models)
            return embedding[: self.target_dimension]
        return embedding

    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        for doc in documents:
            embedding = await self.embedding_provider.get_embedding(doc.content)
            # Pad the embedding to match target dimension
            padded_embedding = self._pad_embedding(embedding)

            db_doc = Document(
                content=doc.content,
                metadata=doc.metadata,
                embedding=padded_embedding,
                embedding_type=ConfigManager.get_config().embedding_type.value,
            )
            self.session.add(db_doc)
        await self.session.commit()

    async def similarity_search(self, query: str, k: int = 3) -> list[DocumentResponse]:
        query_embedding = await self.embedding_provider.get_embedding(query)
        # Pad the query embedding to match target dimension
        padded_query_embedding = self._pad_embedding(query_embedding)

        similar_docs = await self.session.execute(
            select(Document)
            .order_by(Document.embedding.cosine_distance(padded_query_embedding))
            .limit(k)
        )
        documents = similar_docs.scalars().all()

        return [
            DocumentResponse(
                content=doc.content,
                metadata={
                    **(
                        doc.metadata._asdict()
                        if hasattr(doc.metadata, "_asdict")
                        else {}
                    ),
                    "embedding": (
                        doc.embedding.tolist()
                        if hasattr(doc.embedding, "tolist")
                        else doc.embedding
                    ),
                },
            )
            for doc in documents
        ]
