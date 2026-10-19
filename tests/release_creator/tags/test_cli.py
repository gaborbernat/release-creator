"""Numeric tag command tests."""

import sys
from io import StringIO

lazy import pytest

lazy from release_creator.cli import main


def test_tags_validate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["release-creator", "tags", "1.2.3"])
    main()


def test_tags_previous(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["release-creator", "tags", "1.2.3", "--previous"])
    monkeypatch.setattr(sys, "stdin", StringIO("1.0.0\n1.2.2\n1.2.3\n"))
    main()
    assert capsys.readouterr().out == "1.2.2\n"


def test_tags_previous_missing(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["release-creator", "tags", "1.2.3", "--previous"])
    monkeypatch.setattr(sys, "stdin", StringIO("1.2.3\n"))
    main()
    assert not capsys.readouterr().out


def test_tags_require_newer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["release-creator", "tags", "1.2.3", "--require-newer"])
    monkeypatch.setattr(sys, "stdin", StringIO("1.2.2\n"))
    main()


def test_tags_require_newer_rejects_existing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["release-creator", "tags", "1.2.3", "--require-newer"])
    monkeypatch.setattr(sys, "stdin", StringIO("1.2.3\n"))
    with pytest.raises(SystemExit, match="2"):
        main()
    assert "must be newer" in capsys.readouterr().err
