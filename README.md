# AI Engineer Python Starter

A professional Python backend template with LLM integration, vector store support, and a Gradio UI for configuration.

## Features

- FastAPI backend with async support
- PostgreSQL with vector extension support
- Pinecone vector store integration
- OpenAI and Anthropic LLM support
- Gradio UI for runtime configuration
- Type hints and strict mypy configuration
- Pre-commit hooks for code quality
- Docker support

## Getting Started

1. Clone the repository
2. Copy `.env.sample` to `.env` and fill in your configuration
3. Install dependencies:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   poetry install
   ```

4. Start the development server:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Configuration

### Environment Variables

See `.env.sample` for all available configuration options:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
DB_ECHO_LOG=false

# Vector Store Configuration
VECTOR_STORE_TYPE=postgres  # or "pinecone"

# Pinecone Configuration (required if VECTOR_STORE_TYPE=pinecone)
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=your-index-name

# LLM Configuration
LLM_TYPE=openai  # or "anthropic"

# OpenAI Configuration (required if LLM_TYPE=openai)
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Configuration (required if LLM_TYPE=anthropic)
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### Gradio UI

Access the Gradio UI at `http://localhost:8000/ui` to:

- Switch between vector stores (PostgreSQL/Pinecone)
- Switch between LLMs (OpenAI/Anthropic)
- Apply changes at runtime

The UI configuration persists until the server is restarted, at which point it reverts to environment variable settings.

## API Endpoints

- `GET /`: Welcome message
- `POST /documents/`: Add documents to the vector store
- `POST /query/`: Query the RAG system

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
# Run all checks
poetry run pre-commit run --all-files

# Run specific checks
poetry run ruff check .
poetry run mypy .
poetry run black .
```

### Docker

Build and run with Docker:

```bash
docker-compose up --build
```

## License

MIT
