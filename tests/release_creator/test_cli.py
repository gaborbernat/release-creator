"""Command line behavior tests."""

from __future__ import annotations

import sys
from runpy import run_module
from typing import TYPE_CHECKING

import pytest

from release_creator.cli import main

if TYPE_CHECKING:
    from pathlib import Path


def test_notes_cli_renders_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("## 1.2.3 (2026-10-18)\n\n### Fixed\n\n- Correct a bug.\n")
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
    main()
    assert "### Bug fixes\n\n- Correct a bug." in capsys.readouterr().out


def test_notes_cli_renders_rst(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    changelog = tmp_path / "changelog.rst"
    changelog.write_text("1.2.3 (today)\n==============\n\nFixed\n-----\n\n- Correct a bug (:issue:`4`).\n")
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
            "--issue-role",
            "pull",
        ],
    )
    main()
    assert "- Correct a bug ([#4](https://github.com/tox-dev/example/pull/4))." in capsys.readouterr().out


def test_notes_cli_reports_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "release-creator",
            "notes",
            "--changelog",
            str(tmp_path / "missing.md"),
            "--tag",
            "1.2.3",
            "--repository",
            "tox-dev/example",
        ],
    )
    with pytest.raises(SystemExit) as error:
        main()
    expected_usage_error = 2
    assert error.value.code == expected_usage_error
    assert "missing.md" in capsys.readouterr().err


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


def test_fragments_cli_links_squash_pull_request(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / "changelog.d"
    directory.mkdir()
    fragment = directory / "+topic.feature.md"
    fragment.write_text("Add a feature.\n")
    commits = tmp_path / "commits.tsv"
    commits.write_text("+topic.feature.md\tAdd a feature (#3)\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        ["release-creator", "fragments", "--repository", "tox-dev/example", "--commit-map", str(commits)],
    )

    main()

    assert fragment.read_text() == "Add a feature ([#3](https://github.com/tox-dev/example/pull/3)).\n"


def test_fragments_cli_reports_missing_commit_map(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = tmp_path / "changelog.d"
    directory.mkdir()
    (directory / "+topic.feature.md").write_text("Add a feature.\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        ["release-creator", "fragments", "--repository", "tox-dev/example", "--commit-map", "missing.tsv"],
    )

    with pytest.raises(SystemExit) as error:
        main()

    expected_usage_error = 2
    assert error.value.code == expected_usage_error
    assert "missing.tsv" in capsys.readouterr().err
