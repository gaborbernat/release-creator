"""Selectable lock export behavior."""

import subprocess  # ruff: ignore[suspicious-subprocess-import]  # Process results are uv's test boundary.
import sys
import tomllib
from typing import TYPE_CHECKING

import pytest
lazy from pytest_mock import MockerFixture

lazy from release_creator.cli import main
lazy from release_creator.locks.export import export_lock

if TYPE_CHECKING:
    from pathlib import Path


def test_export_lock_keeps_group_and_extra_membership(
    tmp_path: Path, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "demo"\nversion = "1.0"\nrequires-python = ">=3.11"\n'
        '[project.optional-dependencies]\ncli = ["shared"]\n'
        '[dependency-groups]\ntest = ["shared"]\nrelease = ["release-tool"]\n'
    )
    mocker.patch("shutil.which", return_value="/usr/bin/uv")
    mocker.patch(
        "subprocess.run",
        side_effect=[
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, '[[packages]]\nname = "runtime"\nversion = "1.0"\n', ""),
            subprocess.CompletedProcess([], 0, '[[packages]]\nname = "shared"\nversion = "2.0"\n', ""),
            subprocess.CompletedProcess(
                [],
                0,
                '[[packages]]\nname = "release-tool"\nversion = "3.0"\nmarker = "python_version >= \'3.15\'"\n',
                "",
            ),
            subprocess.CompletedProcess([], 0, '[[packages]]\nname = "shared"\nversion = "2.0"\n', ""),
        ],
    )

    monkeypatch.setattr(
        sys, "argv", ["release-creator", "locks", "--project", str(project), "--output", str(tmp_path / "pylock.toml")]
    )
    main()

    lock = tomllib.loads((tmp_path / "pylock.toml").read_text())
    assert {key: lock[key] for key in ("requires-python", "dependency-groups", "default-groups", "extras")} == {
        "requires-python": ">=3.11",
        "dependency-groups": ["project-runtime", "test", "release"],
        "default-groups": [],
        "extras": ["cli"],
    }
    assert [(package["name"], package["marker"]) for package in lock["packages"]] == [
        ("release-tool", "(\"release\" in dependency_groups and (python_version >= '3.15'))"),
        ("runtime", '"project-runtime" in dependency_groups'),
        ("shared", '"cli" in extras or "test" in dependency_groups'),
    ]


def test_export_lock_removes_generated_uv_lock(tmp_path: Path) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text("[project]\nname = 'demo'\nversion = '1.0'\nrequires-python = '>=3.15'\n")

    export_lock(project, tmp_path / "pylock.toml")

    assert (tmp_path / "pylock.toml").exists()
    assert not (tmp_path / "uv.lock").exists()


@pytest.mark.parametrize(
    ("project_text", "message"),
    [
        pytest.param("[project]\nname = 'demo'\n", "requires-python", id="missing-python-range"),
        pytest.param(
            "[project]\nname = 'demo'\nrequires-python = '>=3.11'\n[dependency-groups]\nproject-runtime = []\n",
            "project-runtime is reserved",
            id="reserved-group",
        ),
    ],
)
def test_export_lock_rejects_invalid_project(
    project_text: str, message: str, tmp_path: Path, mocker: MockerFixture
) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text(project_text)
    process = mocker.patch("subprocess.run")

    with pytest.raises(ValueError, match=message):
        export_lock(project, tmp_path / "pylock.toml")

    process.assert_not_called()


def test_export_lock_requires_uv(tmp_path: Path, mocker: MockerFixture) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text("[project]\nname = 'demo'\nrequires-python = '>=3.11'\n")
    mocker.patch("shutil.which", return_value=None)

    with pytest.raises(FileNotFoundError, match="uv is required"):
        export_lock(project, tmp_path / "pylock.toml")


def test_export_lock_keeps_existing_uv_lock(tmp_path: Path, mocker: MockerFixture) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text("[project]\nname = 'demo'\nrequires-python = '>=3.11'\n")
    (tmp_path / "uv.lock").write_text("existing")
    mocker.patch("shutil.which", return_value="/usr/bin/uv")
    mocker.patch(
        "subprocess.run",
        side_effect=[
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, "packages = []\n", ""),
        ],
    )

    export_lock(project, tmp_path / "pylock.toml")

    assert (tmp_path / "uv.lock").read_text() == "existing"


def test_export_lock_reports_uv_failure(tmp_path: Path, mocker: MockerFixture) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text("[project]\nname = 'demo'\nrequires-python = '>=3.11'\n")
    mocker.patch("shutil.which", return_value="/usr/bin/uv")
    mocker.patch("subprocess.run", return_value=subprocess.CompletedProcess([], 1, "", "invalid project"))

    with pytest.raises(ValueError, match="invalid project"):
        export_lock(project, tmp_path / "pylock.toml")

    assert not (tmp_path / "uv.lock").exists()
