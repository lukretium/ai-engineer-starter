from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    document_metadata = Column(JSONB, nullable=True)
    embedding = Column(
        Vector(1536), nullable=True
    )  # Fixed dimension for all embeddings
    embedding_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_pydantic(self) -> "Document":
        from app.models.document import Document as PydanticDocument

        return PydanticDocument(
            id=self.id,
            content=self.content,
            metadata=self.document_metadata,
            embedding=self.embedding,
            embedding_type=self.embedding_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
