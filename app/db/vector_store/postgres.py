from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Document
from app.db.vector_store.base import VectorStore
from app.schemas.rag import DocumentCreate, DocumentResponse
from app.services.embeddings import EmbeddingsService


class PostgresVectorStore(VectorStore):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embeddings_service = EmbeddingsService()

    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        for doc in documents:
            embedding = await self.embeddings_service.get_embedding(doc.content)
            db_doc = Document(
                content=doc.content, metadata=doc.metadata, embedding=embedding
            )
            self.session.add(db_doc)
        await self.session.commit()

    async def similarity_search(self, query: str, k: int = 3) -> list[DocumentResponse]:
        query_embedding = await self.embeddings_service.get_embedding(query)

        similar_docs = await self.session.execute(
            select(Document)
            .order_by(Document.embedding.cosine_distance(query_embedding))
            .limit(k)
        )
        documents = similar_docs.scalars().all()

        return [
            DocumentResponse(content=doc.content, metadata=doc.metadata)
            for doc in documents
        ]
