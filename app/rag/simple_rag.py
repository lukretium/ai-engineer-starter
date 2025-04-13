import logging

import numpy as np

from app.rag.base import RAG
from app.schemas.rag import DocumentCreate, QueryResponse

logger = logging.getLogger(__name__)


class SimpleRAG(RAG):
    def __init__(self, vector_store, llm, embedding_provider):
        super().__init__(vector_store, llm, embedding_provider)
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
        # Get embeddings for all documents
        for doc in documents:
            embedding = await self.embedding_provider.get_embedding(doc.content)
            doc.metadata = doc.metadata or {}
            doc.metadata["embedding"] = embedding
        await self.vector_store.add_documents(documents)

    def _calculate_similarity(
        self, query_embedding: list[float], doc_embedding: list[float]
    ) -> float:
        """Calculate cosine similarity between query and document embeddings."""
        # Pad both embeddings to target dimension
        query_embedding = self._pad_embedding(query_embedding)
        doc_embedding = self._pad_embedding(doc_embedding)

        query_norm = np.linalg.norm(query_embedding)
        doc_norm = np.linalg.norm(doc_embedding)
        if query_norm == 0 or doc_norm == 0:
            return 0
        return np.dot(query_embedding, doc_embedding) / (query_norm * doc_norm)

    async def query(self, query: str, top_k: int = 3) -> QueryResponse:
        logger.info(f"Processing query: {query}")

        # Get embedding for query
        query_embedding = await self.embedding_provider.get_embedding(query)
        logger.info("Generated query embedding")

        # Get relevant documents
        documents = await self.vector_store.similarity_search(query, k=top_k)
        logger.info(f"Retrieved {len(documents)} documents from vector store")

        if not documents:
            logger.warning("No documents found for query")
            return QueryResponse(
                answer=(
                    "I don't have enough information to answer your question "
                    "based on the provided documents."
                ),
                documents=[],
                confidence_score=0.0,
            )

        # Calculate confidence scores for each document
        confidence_scores = []
        for doc in documents:
            doc_embedding = doc.metadata.get("embedding", [])
            if doc_embedding:
                score = self._calculate_similarity(query_embedding, doc_embedding)
                confidence_scores.append(score)
                doc.metadata["confidence_score"] = score
                logger.info(f"Document confidence score: {score}")

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.0
        )
        logger.info(f"Average confidence score: {avg_confidence}")

        # Prepare context for LLM
        context = [doc.content for doc in documents]
        logger.info("Prepared context for LLM")

        # Generate answer using LLM
        answer = await self.llm.generate(query, context)
        logger.info("Generated answer from LLM")

        return QueryResponse(
            answer=answer, documents=documents, confidence_score=avg_confidence
        )
