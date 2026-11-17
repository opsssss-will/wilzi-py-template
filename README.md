# python-template

Template de projeto Python profissional — estrutura pronta com lint, tipagem,
testes, cobertura, CI e empacotamento.

## Stack

| Ferramenta | Papel |
|---|---|
| [uv](https://docs.astral.sh/uv/) | Gerenciador de pacotes e ambientes (rápido) |
| [ruff](https://docs.astral.sh/ruff/) | Lint + formatação |
| [pytest](https://docs.pytest.org/) | Testes |
| [pytest-cov](https://pytest-cov.readthedocs.io/) | Cobertura |
| [mypy](https://mypy-lang.org/) | Tipagem estática (modo strict) |
| [hatchling](https://hatch.pypa.io/) | Build backend |
| GitHub Actions | CI |

## Começando

```bash
# Instalar uv (se ainda não tiver)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Criar ambiente e instalar dependências
uv sync --all-extras

# Rodar tudo
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest --cov
```

Sem uv? Use pip:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
ruff check . && ruff format --check . && mypy . && pytest --cov
```

## Estrutura

```
python-template/
├── src/
│   └── python_template/
│       ├── __init__.py      # API pública do pacote
│       ├── __main__.py      # python -m python_template
│       ├── cli.py           # interface de linha de comando
│       ├── core.py          # lógica pura (sem I/O)
│       └── py.typed         # marcador PEP 561
├── tests/
│   ├── conftest.py          # fixtures
│   ├── test_core.py
│   └── test_cli.py
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

**Convenção:** `core.py` não faz I/O. `cli.py` faz I/O e delega para `core.py`.
Isso mantém a lógica testável e o CLI薄 fino.

## Comandos

```bash
make install    # uv sync --all-extras
make lint       # ruff check + ruff format --check
make format     # ruff check --fix + ruff format
make type       # mypy
make test       # pytest
make coverage   # pytest --cov (com relatório de cobertura)
make all        # lint + type + test
make clean      # remove caches
```

Sem `make` (Windows): use os comandos do `uv run` listados acima.

## Uso da CLI

```bash
uv run python-template                 # Olá, Mundo!
uv run python-template Ana             # Olá, Ana!
uv run python-template Ana --excited   # Olá, Ana!!
uv run python-template --show-config
uv run python-template --version
```

## Configuração por ambiente

A CLI lê variáveis com prefixo `PYTHON_TEMPLATE_`:

| Variável | Padrão | Exemplo |
|---|---|---|
| `PYTHON_TEMPLATE_NAME` | `Mundo` | `Projeto` |
| `PYTHON_TEMPLATE_VERBOSE` | `false` | `true` |
| `PYTHON_TEMPLATE_MAX_RETRIES` | `3` | `7` |
| `PYTHON_TEMPLATE_TAGS` | (vazio) | `a,b,c` |

## CI

`.github/workflows/ci.yml` roda em cada push/PR:
lint → formatação → mypy → pytest com cobertura → build.

## Publicando

O projeto usa **Trusted Publishing** (OIDC) — sem token de API no repositório.

```bash
# Build + validação dos metadados
uv build
uv run twine check dist/*

# Teste no TestPyPI
uvx twine upload dist/* --repository-url https://test.pypi.org/legacy/

# Release real (dispara o workflow de publish)
git tag -a v0.1.0 -m "v0.1.0" && git push origin main --follow-tags
gh release create v0.1.0 --generate-notes
```

Guia completo (setup do PyPI, Trusted Publishing, checklist):
**[RELEASING.md](RELEASING.md)**

## Licença

MIT — veja [LICENSE](LICENSE).
