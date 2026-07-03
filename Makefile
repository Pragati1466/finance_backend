.PHONY: help install run test lint format clean docker-build docker-run

# Default target
help:
	@echo "Finance Analytics Backend - Available commands:"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the development server"
	@echo "  make test         - Run all tests"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make lint         - Run code linting"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make setup        - Initial setup (install + create dirs)"

# Install dependencies
install:
	pip install -r requirements.txt

# Run development server
run:
	python main.py

# Run all tests
test:
	pytest tests/ -v

# Run unit tests
test-unit:
	pytest tests/unit/ -v

# Run integration tests
test-integration:
	pytest tests/integration/ -v

# Run tests with coverage
test-coverage:
	pytest tests/ --cov=. --cov-report=html --cov-report=term

# Lint code
lint:
	flake8 . --max-line-length=100 --exclude=.git,__pycache__,venv,.venv
	mypy . --ignore-missing-imports

# Format code
format:
	black .
	isort .

# Clean temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Build Docker image
docker-build:
	docker build -t finance-analytics-backend .

# Run Docker container
docker-run:
	docker run -p 8000:8000 --env-file .env finance-analytics-backend

# Initial setup
setup:
	pip install -r requirements.txt
	mkdir -p uploads data
	cp .env.example .env
	@echo "Setup complete. Please configure .env file with your settings."
