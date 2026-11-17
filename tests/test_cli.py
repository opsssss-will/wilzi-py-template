"""Testes da interface de linha de comando."""

from __future__ import annotations

import pytest

from wilzi_py_template.cli import main


class TestCLI:
    """Testes para :func:`wilzi_py_template.cli.main`."""

    def test_default_greeting(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main([]) == 0
        assert "Olá, Mundo!" in capsys.readouterr().out

    def test_named_greeting(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["Ana"]) == 0
        assert "Olá, Ana!" in capsys.readouterr().out

    def test_excited_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["Ana", "--excited"]) == 0
        assert "Olá, Ana!!" in capsys.readouterr().out

    def test_show_config(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["--show-config"]) == 0
        out = capsys.readouterr().out
        assert "name=" in out
        assert "max_retries=" in out

    def test_version_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        assert "0.1.0" in capsys.readouterr().out

    def test_empty_name_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["   "]) == 1
        assert "erro:" in capsys.readouterr().err
