"""Testes do módulo :mod:`wilzi_py_template.core`."""

from __future__ import annotations

import pytest

from wilzi_py_template.core import DEFAULT_NAME, Config, greeting


class TestGreeting:
    """Testes para :func:`greeting`."""

    def test_default_name(self) -> None:
        assert greeting() == f"Olá, {DEFAULT_NAME}!"

    def test_custom_name(self) -> None:
        assert greeting("Ana") == "Olá, Ana!"

    def test_strips_whitespace(self) -> None:
        assert greeting("  Ana  ") == "Olá, Ana!"

    def test_excited(self) -> None:
        assert greeting("Ana", excited=True) == "Olá, Ana!!"

    @pytest.mark.parametrize("invalid", ["", "   ", "\t\n"])
    def test_empty_name_raises(self, invalid: str) -> None:
        with pytest.raises(ValueError, match="não pode ser vazio"):
            greeting(invalid)


class TestConfig:
    """Testes para :class:`Config`."""

    def test_defaults(self, config: Config) -> None:
        assert config.name == DEFAULT_NAME
        assert config.verbose is False
        assert config.max_retries == 3
        assert config.tags == ()

    def test_is_immutable(self, config: Config) -> None:
        with pytest.raises(AttributeError):
            config.name = "outro"  # type: ignore[misc]

    def test_from_env_empty(self, env: dict[str, str]) -> None:
        config = Config.from_env(env)
        assert config.name == DEFAULT_NAME
        assert config.max_retries == 3

    def test_from_env_overrides(self, env: dict[str, str]) -> None:
        env.update(
            {
                "WILZI_PY_TEMPLATE_NAME": "Projeto",
                "WILZI_PY_TEMPLATE_VERBOSE": "true",
                "WILZI_PY_TEMPLATE_MAX_RETRIES": "7",
                "WILZI_PY_TEMPLATE_TAGS": "a, b ,c",
            }
        )
        config = Config.from_env(env)
        assert config.name == "Projeto"
        assert config.verbose is True
        assert config.max_retries == 7
        assert config.tags == ("a", "b", "c")

    @pytest.mark.parametrize("raw", ["abc", "", "3.5"])
    def test_invalid_retries_falls_back(self, env: dict[str, str], raw: str) -> None:
        env["WILZI_PY_TEMPLATE_MAX_RETRIES"] = raw
        config = Config.from_env(env)
        if raw == "":
            assert config.max_retries == 3
        else:
            assert config.max_retries == 3
