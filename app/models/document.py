from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Base document model that can be used across different storage implementations."""

    id: int | None = None
    content: str
    metadata: dict[str, Any] | None = None
    embedding: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

    def to_sqlalchemy(self) -> "Document":
        from app.db.postgres.models import Document as SQLAlchemyDocument

        return SQLAlchemyDocument(
            id=self.id,
            content=self.content,
            document_metadata=self.metadata,
            embedding=self.embedding,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
