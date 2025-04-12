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
- Pre-commit hooks for code quality
- GitHub Actions for CI/CD

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

4. Set up pre-commit hooks:

   ```bash
   poetry run pre-commit install
   ```

5. Create a `.env` file with the following variables:
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

## Code Quality

The project uses pre-commit hooks to ensure code quality. These hooks run automatically before each commit and include:

- Code formatting with black and isort
- Linting with ruff
- Type checking with mypy
- Various file checks (YAML, JSON, TOML, etc.)
- Security checks

To run all hooks manually:

```bash
poetry run pre-commit run --all-files
```

## Testing

Run tests with coverage:

```bash
poetry run pytest --cov=app tests/
```

## Continuous Integration

The project uses GitHub Actions for CI/CD. The workflow:

1. Runs pre-commit hooks
2. Runs tests with coverage
3. Uploads coverage reports to Codecov

## License

MIT
