"""Fragment command tests."""

import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]  # Test the fragment command against real Git history.
import sys
from typing import TYPE_CHECKING

import pytest

from release_creator.cli import main

if TYPE_CHECKING:
    from pathlib import Path


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


def test_fragments_cli_reads_git(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / "changelog.d"
    directory.mkdir()
    fragment = directory / "+topic.feature.md"
    fragment.write_text("Add a feature.\n")
    git = shutil.which("git")
    assert git is not None
    subprocess.run([git, "init", "-q", str(tmp_path)], check=True)  # ruff: ignore[subprocess-without-shell-equals-true]  # Fixed Git setup in a temp repo.
    subprocess.run([git, "-C", str(tmp_path), "add", "changelog.d"], check=True)  # ruff: ignore[subprocess-without-shell-equals-true]  # Git test setup.
    subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]  # Git test setup with fixed flags and temp path.
        [
            git,
            "-C",
            str(tmp_path),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-qm",
            "Add a feature (#3)",
        ],
        check=True,
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["release-creator", "fragments", "--repository", "tox-dev/example", "--git"])

    main()

    assert fragment.read_text() == "Add a feature ([#3](https://github.com/tox-dev/example/pull/3)).\n"


def test_fragments_cli_reports_git_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = tmp_path / "changelog.d"
    directory.mkdir()
    (directory / "+topic.feature.md").write_text("Add a feature.\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["release-creator", "fragments", "--repository", "tox-dev/example", "--git"])

    with pytest.raises(SystemExit) as error:
        main()

    expected_usage_error = 2
    assert error.value.code == expected_usage_error
    assert "not a git repository" in capsys.readouterr().err


def test_fragments_cli_reports_missing_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = tmp_path / "changelog.d"
    directory.mkdir()
    (directory / "+topic.feature.md").write_text("Add a feature.\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["release-creator", "fragments", "--repository", "tox-dev/example", "--git"])

    with pytest.raises(SystemExit) as error:
        main()

    expected_usage_error = 2
    assert error.value.code == expected_usage_error
    assert "Git is required" in capsys.readouterr().err
