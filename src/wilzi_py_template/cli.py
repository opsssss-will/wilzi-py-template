"""Interface de linha de comando do pacote.

Este módulo contém toda a interação com o sistema (argumentos, stdout).
A lógica de negócio vive em :mod:`wilzi_py_template.core`.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from wilzi_py_template import __version__
from wilzi_py_template.core import Config, greeting


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da CLI.

    Returns:
        Um :class:`argparse.ArgumentParser` configurado.
    """
    parser = argparse.ArgumentParser(
        prog="wilzi-py-template",
        description="Ferramenta de linha de comando do template Python.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Nome a ser saudado (padrão: valor da config ou 'Mundo').",
    )
    parser.add_argument(
        "--excited",
        action="store_true",
        help="Adiciona um ponto de exclamação extra à saudação.",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Exibe a configuração resolvida e sai.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada da CLI.

    Args:
        argv: Argumentos a processar. Se ``None``, usa ``sys.argv[1:]``.

    Returns:
        O código de saída do processo (``0`` para sucesso).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    config = Config.from_env()

    if args.show_config:
        print(f"name={config.name}")
        print(f"verbose={config.verbose}")
        print(f"max_retries={config.max_retries}")
        print(f"tags={','.join(config.tags)}")
        return 0

    name = args.name or config.name
    try:
        print(greeting(name, excited=args.excited))
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
