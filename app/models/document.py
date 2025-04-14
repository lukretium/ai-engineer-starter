from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base

# Register Vector type with SQLAlchemy
Vector.cache_ok = True


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    document_metadata = Column(JSONB)
    embedding = Column(Vector(1536))
    embedding_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (Index("ix_documents_id", "id"),)

    def to_sqlalchemy(self) -> "Document":
        from app.db.postgres.models import Document as SQLAlchemyDocument

        return SQLAlchemyDocument(
            id=self.id,
            content=self.content,
            document_metadata=self.metadata,
            embedding=self.embedding,
            embedding_type=self.embedding_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
