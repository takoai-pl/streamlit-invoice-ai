FROM python:3.10-slim

RUN apt-get update && apt-get install -y make gettext && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY Makefile ./
COPY locales/ locales/
COPY scripts/ scripts/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD ["make", "start"]