FROM python:3.10-slim

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 8080

ENTRYPOINT ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8080"]

