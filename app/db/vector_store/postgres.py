from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Document
from app.db.vector_store.base import VectorStore
from app.schemas.rag import DocumentCreate, DocumentResponse


class PostgresVectorStore(VectorStore):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        for doc in documents:
            embedding = self.model.encode(doc.content)
            db_doc = Document(
                content=doc.content, metadata=doc.metadata, embedding=embedding
            )
            self.session.add(db_doc)
        await self.session.commit()

    async def similarity_search(self, query: str, k: int = 3) -> list[DocumentResponse]:
        query_embedding = self.model.encode(query)

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
