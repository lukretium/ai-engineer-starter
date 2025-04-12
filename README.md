# AI Engineer Backend

A professional Python backend with LLM integration using FastAPI, SQLAlchemy, and modern tooling.

## Features

- FastAPI for modern async API endpoints
- SQLAlchemy with async support for database operations
- PostgreSQL database
- Docker and docker-compose for development and production
- Poetry for dependency management
- Comprehensive testing setup with pytest
- Modern linting and formatting with ruff, black, and mypy

## Prerequisites

- Python 3.11+
- Docker and docker-compose
- Poetry

## Setup

1. Clone the repository
2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app
   ENVIRONMENT=development
   OPENAI_API_KEY=your_openai_api_key
   ```

## Development

1. Start the development environment:
   ```bash
   docker-compose up -d
   ```

2. The API will be available at http://localhost:8000

3. API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

Run tests with coverage:
```bash
poetry run pytest --cov=app tests/
```

## Code Quality

- Format code:
  ```bash
  poetry run black .
  poetry run isort .
  ```

- Lint code:
  ```bash
  poetry run ruff check .
  ```

- Type checking:
  ```bash
  poetry run mypy .
  ```

## License

MIT 