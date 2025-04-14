from abc import ABC, abstractmethod

from app.schemas.rag import DocumentCreate, DocumentResponse


class VectorStore(ABC):
    @abstractmethod
    async def add_documents(self, documents: list[DocumentCreate]) -> None:
        pass

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 3) -> list[DocumentResponse]:
        pass
