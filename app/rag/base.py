from abc import ABC, abstractmethod

from app.db.vector_store.base import VectorStore
from app.embeddings.base import EmbeddingProvider
from app.llm.base import LLM
from app.schemas.rag import DocumentCreate, QueryResponse


class RAG(ABC):
    def __init__(
        self, vector_store: VectorStore, llm: LLM, embedding_provider: EmbeddingProvider
    ) -> None:
        self.vector_store = vector_store
        self.llm = llm
        self.embedding_provider = embedding_provider

    @abstractmethod
    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        pass

    @abstractmethod
    async def query(self, query: str, top_k: int = 3) -> QueryResponse:
        pass
