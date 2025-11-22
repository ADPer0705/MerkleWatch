.PHONY: help install dev clean snapshot verify test lint format

PYTHON := python3
PIP := pip

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in editable mode
	$(PIP) install -e .

dev: ## Install development dependencies
	$(PIP) install -e ".[dev]"

clean: ## Remove build artifacts and cache
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

snapshot: ## Create a snapshot (Usage: make snapshot DIR=./path OUT=manifest.json)
	@if [ -z "$(DIR)" ]; then echo "Error: DIR argument is required. Usage: make snapshot DIR=./path OUT=manifest.json"; exit 1; fi
	@if [ -z "$(OUT)" ]; then echo "Error: OUT argument is required. Usage: make snapshot DIR=./path OUT=manifest.json"; exit 1; fi
	$(PYTHON) -m merklewatch snapshot "$(DIR)" --out "$(OUT)"

verify: ## Verify a snapshot (Usage: make verify MANIFEST=manifest.json DIR=./path)
	@if [ -z "$(MANIFEST)" ]; then echo "Error: MANIFEST argument is required. Usage: make verify MANIFEST=manifest.json DIR=./path"; exit 1; fi
	@if [ -z "$(DIR)" ]; then echo "Error: DIR argument is required. Usage: make verify MANIFEST=manifest.json DIR=./path"; exit 1; fi
	$(PYTHON) -m merklewatch verify "$(MANIFEST)" "$(DIR)"

test: ## Run tests (if any)
	pytest

lint: ## Run linting
	ruff check .

format: ## Format code
	black .
