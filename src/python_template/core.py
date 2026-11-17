"""Núcleo do pacote: funções puras e tipos de domínio.

Este módulo não deve importar nada de I/O (rede, disco, stdin/stdout).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Final

DEFAULT_NAME: Final[str] = "Mundo"


def greeting(name: str = DEFAULT_NAME, *, excited: bool = False) -> str:
    """Retorna uma saudação formatada.

    Args:
        name: Nome a ser saudado. Espaços em branco são removidos das pontas.
        excited: Se verdadeiro, adiciona um ponto de exclamação.

    Returns:
        A saudação formatada.

    Raises:
        ValueError: Se ``name`` estiver vazio após o corte de espaços.

    Example:
        >>> greeting("Ana")
        'Olá, Ana!'
        >>> greeting("Ana", excited=True)
        'Olá, Ana!!'
    """
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name não pode ser vazio")

    suffix = "!!" if excited else "!"
    return f"Olá, {cleaned}{suffix}"


@dataclass(frozen=True, slots=True)
class Config:
    """Configuração imutável do projeto.

    Os valores podem ser sobrescritos por variáveis de ambiente
    prefixadas com ``PYTHON_TEMPLATE_``.
    """

    name: str = DEFAULT_NAME
    verbose: bool = False
    max_retries: int = 3
    tags: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> Config:
        """Constrói a configuração a partir de variáveis de ambiente.

        Args:
            env: Mapeamento a usar. Se ``None``, usa ``os.environ``.

        Returns:
            Uma instância de :class:`Config` com os valores resolvidos.
        """
        source = os.environ if env is None else env

        raw_retries = source.get("PYTHON_TEMPLATE_MAX_RETRIES")
        try:
            max_retries = int(raw_retries) if raw_retries else 3
        except ValueError:
            max_retries = 3

        raw_tags = source.get("PYTHON_TEMPLATE_TAGS", "")
        tags = tuple(t.strip() for t in raw_tags.split(",") if t.strip())

        return cls(
            name=source.get("PYTHON_TEMPLATE_NAME", DEFAULT_NAME),
            verbose=source.get("PYTHON_TEMPLATE_VERBOSE", "").lower()
            in {"1", "true", "yes"},
            max_retries=max_retries,
            tags=tags,
        )
