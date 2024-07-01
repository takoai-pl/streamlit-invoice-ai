FROM python:3.10-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY backend/server.py ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

