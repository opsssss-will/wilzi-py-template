.PHONY: help install lint format type test coverage all build clean check release-test release-pypi version

help:  ## Mostra esta ajuda
	@echo "install   - Instala dependências (uv sync --all-extras)"
	@echo "lint      - Ruff check + verificação de formatação"
	@echo "format    - Ruff --fix + ruff format"
	@echo "type      - mypy (tipagem estrita)"
	@echo "test      - pytest"
	@echo "coverage  - pytest com relatório de cobertura"
	@echo "all       - lint + type + test"
	@echo "build     - Constrói wheel e sdist"
	@echo "check     - twine check nos artefatos"
	@echo "clean     - Remove caches e artefatos"
	@echo "release-test - Sobe para o TestPyPI (requer token)"
	@echo "release-pypi - Publica no PyPI (via GitHub Actions / Trusted Publishing)"

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

check: build  ## Valida os metadados dos artefatos
	uv run twine check dist/*

release-test: check  ## Sobe para o TestPyPI (requer TESTPYPI_API_TOKEN no ambiente)
	uvx twine upload dist/* \
		--repository-url https://test.pypi.org/legacy/ \
		--non-interactive

release-pypi: check  ## Mostra os comandos para publicar no PyPI
	@echo "Publique pelo GitHub Actions (Trusted Publishing):"
	@echo "  git tag -a v<versao> -m 'v<versao>' && git push origin main --follow-tags"
	@echo "  gh release create v<versao> --generate-notes"
	@echo ""
	@echo "Ou manualmente (requer PYPI_API_TOKEN no ambiente):"
	@echo "  uvx twine upload dist/* --non-interactive"

clean:  ## Limpa caches
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
