from typing import Any

import gradio as gr
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.postgres.session import get_db, init_db
from app.db.vector_store.factory import VectorStoreFactory
from app.embeddings.factory import EmbeddingFactory
from app.llm.factory import LLMFactory
from app.models.document import Document
from app.rag.simple_rag import SimpleRAG
from app.schemas.rag import DocumentCreate, QueryResponse
from app.ui.gradio_ui import create_gradio_ui

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Gradio UI
gradio_app = gr.mount_gradio_app(app, create_gradio_ui(), path="/ui")


def get_rag_service(db: AsyncSession) -> SimpleRAG:
    vector_store = VectorStoreFactory.create_vector_store(session=db)
    llm = LLMFactory.create_llm()
    embedding_provider = EmbeddingFactory.create_embedding_provider()
    return SimpleRAG(vector_store, llm, embedding_provider)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to AI Engineer API"}


@app.post("/documents", response_model=None)
async def add_documents(
    documents: list[DocumentCreate], db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    rag_service = get_rag_service(db)
    await rag_service.add_documents(documents)
    return {"message": "Documents added successfully"}


@app.post("/query", response_model=QueryResponse)
async def query(
    query: str, top_k: int = 3, db: AsyncSession = Depends(get_db)
) -> QueryResponse:
    rag_service = get_rag_service(db)
    return await rag_service.query(query, top_k)


class ImportRequest(BaseModel):
    documents: list[dict[str, Any]]


class QueryRequest(BaseModel):
    query: str
    top_k: int | None = 5


@app.post("/import")
async def import_documents(
    request: ImportRequest, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    try:
        vector_store = VectorStoreFactory.create_vector_store(session=db)
        documents = [Document(**doc) for doc in request.documents]
        await vector_store.add_documents(documents)
        return {"message": f"Successfully imported {len(documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/query")
async def query_documents(
    query: str, top_k: int = 5, db: AsyncSession = Depends(get_db)
) -> dict[str, list[dict[str, Any]]]:
    try:
        vector_store = VectorStoreFactory.create_vector_store(session=db)
        results = await vector_store.similarity_search(query, k=top_k)
        return {"results": [doc.dict() for doc in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup.

    This function is called once when the application starts.
    It ensures all necessary components are properly initialized.
    """
    # Initialize database connection pool
    await init_db()
