FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==2.1.3

RUN poetry config virtualenvs.create false

RUN poetry lock || true

RUN poetry install --no-root --only main

COPY . .

RUN useradd -m -u 1000 appuser

RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

USER appuser

ENV PYTHONPATH=/app
ENV SERVE_FRONTEND=false

EXPOSE 3000

CMD ["uvicorn", "openhands.app_server.app:app", "--host", "0.0.0.0", "--port", "3000"]
