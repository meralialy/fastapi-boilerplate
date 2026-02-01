# Variables
CONTAINER_NAME = fastapi
DOCKER_COMPOSE = docker compose
ENV_FILENAME ?= .env
IMAGE_NAME = fastapi-boilerplate
PYTEST = $(UV) run pytest
PYTHON = $(UV) run python
PYTHON_VERSION = 3.14
RUFF = $(UV) run ruff
MYPY = $(UV) run mypy
UV = uv
VENV = .venv

## --- Help System ---

.PHONY: help create-env delete-env ensure-venv

help: ## Show this help message
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

create-env: # Create a temporary .env file from .env.example
	@cat .env.example > $(ENV_FILENAME)

delete-env: # Remove the temporary .env file
	@rm -f $(ENV_FILENAME)

ensure-venv: # Check for a virtual environment and create one if it doesn't exist
	@test -d $(VENV) || $(MAKE) setup

## --- Setup & Installation & Clean---

.PHONY: setup install install-hooks clean

setup: ## Set up the development environment (virtualenv, dependencies, pre-commit hooks)
	@command -v uv >/dev/null 2>&1 || pip install uv
	$(UV) venv --clear --python $(PYTHON_VERSION)
	$(MAKE) install
	$(MAKE) install-hooks

install: # Install/sync dependencies from uv.lock into the virtual environment
	$(UV) sync

install-hooks: # Install pre-commit hooks into the local .git config
	$(MAKE) ensure-venv
	$(UV) run pre-commit install

clean: ## Remove caches, artifacts, and virtualenv, then re-initialize the environment
	-$(UV) run pre-commit clean
	rm -rf $(VENV) $(ENV_FILENAME) .coverage .mypy_cache .pytest_cache .ruff_cache htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "py.typed" -exec rm -rf {} +

## --- Testing ---

.PHONY: test code-coverage

test: ## Run tests with Pytest. Pass extra arguments via ARG, e.g., 'make test ARG="-k test_name"'
	$(MAKE) ensure-venv
	$(PYTEST) $(ARG)

code-coverage: ## Run tests and generate a code coverage report in the terminal
	$(MAKE) ensure-venv
	$(PYTEST)

## --- Linting & Formatting ---

.PHONY: lint lint-fix format format-fix

lint: ## Lint the codebase using Ruff without making changes
	$(MAKE) ensure-venv
	$(RUFF) check .

lint-fix: ## Automatically fix linting issues with Ruff
	$(MAKE) ensure-venv
	$(RUFF) check . --fix

format: ## Check for code formatting issues with Ruff without making changes
	$(MAKE) ensure-venv
	$(RUFF) format . --check

format-fix: ## Automatically format the codebase using Ruff
	$(MAKE) ensure-venv
	$(RUFF) format .

## --- Hygiene & Analysis ---

.PHONY: precommit ruff mypy ci

precommit: ## Manually run all pre-commit hooks on all files
	$(MAKE) ensure-venv
	$(UV) run pre-commit run --all-files

ruff: ## Show detailed statistics for Ruff linting rules
	$(MAKE) ensure-venv
	$(RUFF) check . --statistics

mypy: ## Run static type analysis on the codebase with MyPy
	$(MAKE) ensure-venv
	$(MYPY) .

ci: ## Run all local CI checks (lint, format, types, tests)
	$(MAKE) precommit
	$(MAKE) test
	$(MAKE) code-coverage

## --- Docker Management ---

.PHONY: docker-start docker-rebuild docker-stop docker-reset docker-hard-reset docker-status docker-logs

docker-start: ## Start the Docker containers, building images if necessary
	@if [ ! -f $(ENV_FILENAME) ]; then $(MAKE) create-env; fi
	$(DOCKER_COMPOSE) up --build -d

docker-rebuild: ## Rebuild and restart the Docker containers from scratch
	@if [ ! -f $(ENV_FILENAME) ]; then $(MAKE) create-env; fi
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d --force-recreate --no-deps

docker-stop: ## Stop the Docker containers
	@if [ -z "$$($(DOCKER_COMPOSE) ps --services --filter "status=running" 2>/dev/null)" ]; then \
		printf "\033[33m⚠️  App is already stopped.\033[0m\n"; \
	else \
		$(DOCKER_COMPOSE) stop; \
	fi

docker-reset: ## Stop and remove all Docker containers, images, volumes, and networks
	$(DOCKER_COMPOSE) down --rmi all --remove-orphans
	docker system prune -f

docker-hard-reset: ## Stop and remove all Docker containers, images, volumes, and networks, and prune unused volumes
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	docker system prune -f
	docker volume prune -f

docker-status: ## Show the status of Docker containers
	@if [ -z "$$($(DOCKER_COMPOSE) ps --services --filter "status=running" 2>/dev/null)" ]; then \
		printf "\033[33m⚠️  No containers are running. Use 'make docker-start' to start them.\033[0m\n"; \
	else \
		$(DOCKER_COMPOSE) ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"; \
	fi

docker-logs: ## Tail the logs of the Docker containers
	@if [ -z "$$($(DOCKER_COMPOSE) ps --services --filter "status=running" 2>/dev/null)" ]; then \
		printf "\033[33m⚠️  App is not running. Use 'make docker-start' to start it.\033[0m\n"; \
	else \
		$(DOCKER_COMPOSE) logs -f; \
	fi
