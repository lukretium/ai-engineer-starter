from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vector_store import Document
from app.schemas.rag import DocumentCreate, QueryResponse


class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        for doc in documents:
            embedding = self.model.encode(doc.content)
            db_doc = Document(
                content=doc.content, metadata=doc.metadata, embedding=embedding
            )
            self.db.add(db_doc)
        await self.db.commit()

    async def query(self, query: str, top_k: int = 3) -> QueryResponse:
        query_embedding = self.model.encode(query)

        # Find similar documents
        similar_docs = await self.db.execute(
            select(Document)
            .order_by(Document.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )
        documents = similar_docs.scalars().all()

        if not documents:
            return QueryResponse(
                answer=(
                    "I don't have enough information to answer your question "
                    "based on the provided documents."
                ),
                documents=[],
            )

        # Combine document contents for context
        context = "\n\n".join(doc.content for doc in documents)

        # Here you would typically use an LLM to generate the answer
        # For now, we'll return a simple response
        answer = f"Based on the provided documents, here's what I found:\n\n{context}"

        return QueryResponse(
            answer=answer,
            documents=[
                {"content": doc.content, "metadata": doc.metadata} for doc in documents
            ],
        )
