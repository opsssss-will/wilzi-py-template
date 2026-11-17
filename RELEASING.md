# Guia de Publicação no PyPI

Este projeto usa **Trusted Publishing** (OIDC) — sem token de API no repositório.

## Setup único (uma vez)

### 1. Criar conta no PyPI

- Acesse <https://pypi.org/account/register/>
- Verifique o e-mail
- Habilite 2FA (obrigatório para Trusted Publishing)

### 2. Criar o repositório no GitHub

```bash
gh auth login          # login interativo
gh repo create python-template --public --source=. --remote=origin --push
```

### 3. Configurar Trusted Publishing

No PyPI, vá em **Manage → Publishing → Add a new publisher**:

| Campo | Valor |
|---|---|
| PyPI project name | `python-template` |
| Owner | `wilzi` (seu usuário do GitHub) |
| Repository name | `python-template` |
| Workflow name | `release.yml` |
| Environment name | `pypi` |

Repita o processo escolhendo o repositório `testpypi` para o ambiente `testpypi`.

> **Importante:** o environment `pypi` precisa existir no GitHub
> (Settings → Environments → New environment).

### 4. (Opcional) Token para TestPyPI

Se preferir token em vez de Trusted Publishing no TestPyPI:

- PyPI → Manage → API tokens → Create token (escopo `testpypi` project)
- GitHub → Settings → Secrets → New repository secret → `TESTPYPI_API_TOKEN`

---

## Fluxo de release

### Teste primeiro (recomendado)

```bash
# 1. Build local
uv build

# 2. Conferir os metadados
uv run twine check dist/*

# 3. Subir para o TestPyPI (token)
uvx twine upload dist/* \
  --repository-url https://test.pypi.org/legacy/ \
  --non-interactive

# 4. Testar a instalação
uv venv /tmp/teste && uv pip install --index-url https://test.pypi.org/legacy/ \
  --extra-index-url https://pypi.org/simple python-template
```

Ou via GitHub Actions (após configurar o secret):

```bash
gh workflow run release.yml -f environment=testpypi
```

### Release real

```bash
# 1. Atualizar a versão em pyproject.toml
#    (use `uv version patch` / `minor` / `major`)

# 2. Commitar e marcar
git add pyproject.toml uv.lock
git commit -m "chore: release v0.1.0"
git tag -a v0.1.0 -m "v0.1.0"
git push origin main --follow-tags

# 3. Criar a release no GitHub (dispara o workflow)
gh release create v0.1.0 --generate-notes --title "v0.1.0"
```

O workflow `release.yml` roda automaticamente: lint → tipos → testes → build → publish.

---

## Verificação pós-publicação

```bash
# O pacote aparece em:
# https://pypi.org/project/python-template/

# Testar instalação real
pip install python-template
python -c "import python_template; print(python_template.__version__)"
```

> O PyPI leva ~1-5 minutos para propagar o pacote.

---

## Regras do PyPI

- O **nome do pacote é global e permanente** — `python-template` não pode ser
  reutilizado depois, mesmo em conta nova.
- Versões são imutáveis: para corrigir algo, publique `0.1.1`.
- Não é possível reenviar o mesmo arquivo para a mesma versão.

---

## Checklist

- [ ] `uv run ruff check .` sem erros
- [ ] `uv run ruff format --check .` ok
- [ ] `uv run mypy .` ok
- [ ] `uv run pytest --cov` passa
- [ ] `uv run twine check dist/*` → PASSED
- [ ] Testado no TestPyPI
- [ ] Versão no `pyproject.toml` incrementada
- [ ] Tag `vX.Y.Z` criada e enviada
- [ ] Release criada no GitHub
- [ ] Pacote visível em pypi.org/project/python-template/
