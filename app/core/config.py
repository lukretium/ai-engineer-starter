from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Engineer"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Professional Python backend with LLM integration"

    DATABASE_URL: str
    ENVIRONMENT: str = "development"

    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
