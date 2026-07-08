FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==2.1.3

RUN poetry config virtualenvs.create false

# Update lock file if needed
RUN poetry lock || true

RUN poetry install --no-root --only main

COPY . .

EXPOSE 3000

CMD ["python", "-m", "uvicorn", "openhands.app_server.app:app", "--host", "0.0.0.0", "--port", "3000"]
