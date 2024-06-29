.PHONY: all locales licences lint test start

all: locales format_diff licences lint test

locales:
	@echo "Building locales..."
	./scripts/generate_locales.sh

licences:
	@echo "Building licences..."
	./scripts/generate_licences.sh

start_frontend: locales
	@echo "Starting the front-end..."
	poetry run streamlit frontend/app.py --server.port 8501

start_backend: locales
	@echo "Starting the back-end..."
	poetry run uvicorn backend.server:app --reload

docker_dev:
	@echo "Building the development Docker image..."
	docker-compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml up --build

TEST_FILE ?= tests/

test:
	@echo "Running tests..."
	poetry run pytest $(TEST_FILE)

PYTHON_FILES=.
lint format: PYTHON_FILES=.
lint_diff format_diff: PYTHON_FILES=$(shell git diff --name-only --diff-filter=d main | grep -E '\.py$$|\.ipynb$$')

lint lint_diff:
	@echo "Running linters..."
	poetry run mypy $(PYTHON_FILES)
	poetry run black $(PYTHON_FILES) --check
	poetry run ruff .

format format_diff:
	@echo "Running formatters..."
	poetry run black $(PYTHON_FILES)
	poetry run ruff --select I --fix $(PYTHON_FILES)
	poetry run ruff --select F --fix $(PYTHON_FILES) --ignore F821

docker_prod:
	@echo "Building the production Docker image..."
	docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up --build -d

######################
# HELP
######################
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all         to build locales, lint, test and start the app"
	@echo "  locales     to build locales"
	@echo "  lint        to run linters"
	@echo "  test        to run tests"
	@echo "  start       to start the app"
	@echo "  format      to run formatters"
	@echo "  help        to display this help message"