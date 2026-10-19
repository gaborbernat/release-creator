"""Root command tests."""

import sys
from runpy import run_module
from typing import TYPE_CHECKING

lazy import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_module_entrypoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("## 1.2.3 (2026-10-18)\n")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "release-creator",
            "notes",
            "--changelog",
            str(changelog),
            "--tag",
            "1.2.3",
            "--repository",
            "tox-dev/example",
        ],
    )
    run_module("release_creator", run_name="__main__")
    assert "https://github.com/tox-dev/example/commits/1.2.3" in capsys.readouterr().out
