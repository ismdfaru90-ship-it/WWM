FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install "poetry>=2.0,<3.0"

# Copy poetry files
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install Python dependencies
RUN poetry install --no-root --without dev

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV SERVE_FRONTEND=false

# Expose port
EXPOSE 3000

# Start command
CMD ["uvicorn", "openhands.app_server.app:app", "--host", "0.0.0.0", "--port", "3000"]
