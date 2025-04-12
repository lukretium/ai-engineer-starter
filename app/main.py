from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.postgres.session import get_db
from app.db.vector_store.factory import VectorStoreFactory
from app.llm.factory import LLMFactory
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

# Initialize Gradio UI
create_gradio_ui(app)


def get_rag_service(db: AsyncSession) -> SimpleRAG:
    vector_store = VectorStoreFactory.create_vector_store(session=db)
    llm = LLMFactory.create_llm()
    return SimpleRAG(vector_store, llm)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to AI Engineer API"}


@app.post("/documents/", response_model=None)
async def add_documents(
    documents: list[DocumentCreate], db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    rag_service = get_rag_service(db)
    await rag_service.add_documents(documents)
    return {"message": "Documents added successfully"}


@app.post("/query/", response_model=QueryResponse)
async def query(
    query: str, top_k: int = 3, db: AsyncSession = Depends(get_db)
) -> QueryResponse:
    rag_service = get_rag_service(db)
    return await rag_service.query(query, top_k)
