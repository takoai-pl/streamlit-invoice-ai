.PHONY: all locales licences lint test start

all: locales licences lint test start

locales:
	@echo "Building locales..."
	./scripts/generate_locales.sh

licences:
	@echo "Building licences..."
	./scripts/generate_licences.sh

start: locales
	@echo "Starting the app..."
	poetry run streamlit run src/app.py


# Define a variable for the test file path.
TEST_FILE ?= tests/

test:
	@echo "Running tests..."
	poetry run pytest $(TEST_FILE)

# Define a variable for Python and notebook files.
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
	#poetry run ruff --select I --fix $(PYTHON_FILES)


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