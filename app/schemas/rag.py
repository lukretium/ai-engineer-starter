from pydantic import BaseModel


class DocumentCreate(BaseModel):
    content: str
    metadata: dict | None = None


class DocumentResponse(BaseModel):
    content: str
    metadata: dict | None = None


class QueryResponse(BaseModel):
    answer: str
    documents: list[DocumentResponse]
