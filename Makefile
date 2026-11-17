.PHONY: help install lint format type test coverage all build clean

help:  ## Mostra esta ajuda
	@echo "install   - Instala dependências (uv sync --all-extras)"
	@echo "lint      - Ruff check + verificação de formatação"
	@echo "format    - Ruff --fix + ruff format"
	@echo "type      - mypy (tipagem estrita)"
	@echo "test      - pytest"
	@echo "coverage  - pytest com relatório de cobertura"
	@echo "all       - lint + type + test"
	@echo "build     - Constrói wheel e sdist"
	@echo "clean     - Remove caches e artefatos"

install:  ## Instala dependências
	uv sync --all-extras --dev

lint:  ## Ruff check + formatação
	uv run ruff check .
	uv run ruff format --check .

format:  ## Corrige lint e formata
	uv run ruff check --fix .
	uv run ruff format .

type:  ## Tipagem estática
	uv run mypy .

test:  ## Roda os testes
	uv run pytest

coverage:  ## Testes com cobertura
	uv run pytest --cov --cov-report=term-missing --cov-report=html

all: lint type test  ## Tudo

build:  ## Build
	uv build

clean:  ## Limpa caches
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
