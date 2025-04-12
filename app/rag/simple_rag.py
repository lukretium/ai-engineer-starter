from app.rag.base import RAG
from app.schemas.rag import DocumentCreate, QueryResponse


class SimpleRAG(RAG):
    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        await self.vector_store.add_documents(documents)

    async def query(self, query: str, top_k: int = 3) -> QueryResponse:
        # Get relevant documents
        documents = await self.vector_store.similarity_search(query, k=top_k)

        if not documents:
            return QueryResponse(
                answer=(
                    "I don't have enough information to answer your question "
                    "based on the provided documents."
                ),
                documents=[],
            )

        # Prepare context for LLM
        context = [doc.content for doc in documents]

        # Generate answer using LLM
        answer = await self.llm.generate(query, context)

        return QueryResponse(answer=answer, documents=documents)
