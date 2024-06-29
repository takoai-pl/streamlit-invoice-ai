FROM python:3.10-slim

RUN apt-get update && apt-get install -y make gettext && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /invoice-ai

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]