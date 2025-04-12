from abc import ABC, abstractmethod
from typing import List

from app.schemas.rag import DocumentCreate, DocumentResponse


class VectorStore(ABC):
    @abstractmethod
    async def add_documents(self, documents: List[DocumentCreate]) -> None:
        pass

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 3) -> List[DocumentResponse]:
        pass
