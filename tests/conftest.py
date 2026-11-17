"""Fixtures compartilhadas entre os testes."""

from __future__ import annotations

import pytest

from wilzi_py_template.core import Config


@pytest.fixture
def config() -> Config:
    """Configuração padrão para os testes."""
    return Config()


@pytest.fixture
def env() -> dict[str, str]:
    """Mapeamento de variáveis de ambiente limpo."""
    return {}
