from typing import Any, Dict, List

import pinecone
from sentence_transformers import SentenceTransformer

from app.db.vector_store.base import VectorStore
from app.schemas.rag import DocumentCreate, DocumentResponse


class PineconeVectorStore(VectorStore):
    def __init__(self, api_key: str, environment: str, index_name: str):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384  # all-MiniLM-L6-v2 dimension

    async def add_documents(self, documents: List[DocumentCreate]) -> None:
        vectors = []
        for i, doc in enumerate(documents):
            embedding = self.model.encode(doc.content)
            metadata: Dict[str, Any] = {"content": doc.content}
            if doc.metadata:
                metadata.update(doc.metadata)
            vectors.append(
                {"id": str(i), "values": embedding.tolist(), "metadata": metadata}
            )

        self.index.upsert(vectors=vectors)

    async def similarity_search(self, query: str, k: int = 3) -> List[DocumentResponse]:
        query_embedding = self.model.encode(query)

        results = self.index.query(
            vector=query_embedding.tolist(), top_k=k, include_metadata=True
        )

        return [
            DocumentResponse(
                content=result.metadata["content"], metadata=result.metadata
            )
            for result in results.matches
        ]
