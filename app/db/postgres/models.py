from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    document_metadata = Column(Text, nullable=True)
    embedding = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_pydantic(self) -> "Document":
        from app.models.document import Document as PydanticDocument

        return PydanticDocument(
            id=self.id,
            content=self.content,
            metadata=self.document_metadata,
            embedding=self.embedding,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
