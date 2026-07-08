FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.8.5

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --only main

COPY . .

EXPOSE 3000

CMD ["python", "-m", "uvicorn", "openhands.app_server.app:app", "--host", "0.0.0.0", "--port", "3000"]
