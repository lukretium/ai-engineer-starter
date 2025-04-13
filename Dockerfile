# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create true \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Create scripts directory
RUN mkdir -p scripts

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run migrations and start the application
CMD poetry run python scripts/run_migrations.py && \
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
