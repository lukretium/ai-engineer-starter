from pydantic_settings import BaseSettings


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

    LLM_TYPE: str = "openai"  # or "anthropic"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
