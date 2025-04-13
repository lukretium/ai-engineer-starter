from pydantic_settings import BaseSettings

from app.embeddings.types import EmbeddingType


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Engineer API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Professional Python backend with LLM integration"

    DATABASE_URL: str
    DB_ECHO_LOG: bool = False

    VECTOR_STORE_TYPE: str = "postgres"  # or "pinecone"

    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = ""

    LLM_TYPE: str = "openai"  # or "anthropic" or "ollama"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    # Ollama configuration
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"

    # Embedding configuration
    EMBEDDING_TYPE: EmbeddingType = EmbeddingType.OLLAMA
    HUGGINGFACE_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
