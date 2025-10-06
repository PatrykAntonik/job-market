# Makefile for Docker Compose

# Variables
COMPOSE = docker compose
API_SERVICE = api

# Commands
.PHONY: help up down build-start logs test shell lint format makemigrations migrate createsuperuser collectstatic populate_db clear_data
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

start: ## Start Docker containers in detached mode
	@echo "Starting Docker containers..."
	$(COMPOSE) up -d

stop: ## Stop and remove Docker containers
	@echo "Stopping Docker containers..."
	$(COMPOSE) down

restart: ## Restart Docker containers
	@echo "Restarting Docker containers..."
	$(COMPOSE) restart

build-start: ## Build images and start containers
	@echo "Building and starting Docker containers..."
	$(COMPOSE) up --build -d

logs: ## Follow logs for all services
	@echo "Showing logs for all services..."
	$(COMPOSE) logs -f

test: ## Run tests in parallel
	@echo "Running tests..."
	$(COMPOSE) exec $(API_SERVICE) python -m pytest -n auto

lint: ## Run lint check
	@echo "Running pylint..."
	$(COMPOSE) exec $(API_SERVICE) pylint --fail-under=8.0 JobApp JobMarket2

sort: ## Run sorting check
	@echo "Running Sort..."
	$(COMPOSE) exec $(API_SERVICE) isort -c JobApp JobMarket2

format: ## Run formatter check
	@echo "Running formatter..."
	$(COMPOSE) exec $(API_SERVICE) black JobMarket2 JobApp --check

makemigrations: ## Create new database migrations
	@echo "Creating new migrations..."
	$(COMPOSE) exec $(API_SERVICE) python manage.py makemigrations

migrate: ## Apply database migrations
	@echo "Applying database migrations..."
	$(COMPOSE) exec $(API_SERVICE) python manage.py migrate

createsuperuser: ## Create a new superuser
	@echo "Creating superuser..."
	$(COMPOSE) exec $(API_SERVICE) python manage.py createsuperuser

populate_db: ## Populate the database with initial data
	@echo "Populating the database..."
	$(COMPOSE) exec $(API_SERVICE) python manage.py populate_db

clear_data: ## Clear all data from the database
	@echo "Clearing all data..."
	$(COMPOSE) exec $(API_SERVICE) python manage.py clear_all_data
