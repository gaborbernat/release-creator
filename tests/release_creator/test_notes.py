"""Release note rendering tests."""

from __future__ import annotations

import sys
from dataclasses import replace
from runpy import run_module
from typing import TYPE_CHECKING

import pytest

from release_creator import ReleaseContext, main, render_markdown

if TYPE_CHECKING:
    from pathlib import Path


def test_render_markdown_maps_categories_and_credits() -> None:
    changelog = """\
<a name="release-1-2-3"></a>

## 1.2.3 (2026-10-18)

<a name="release-1-2-3-added"></a>

### Added

- New option ([#42](https://github.com/tox-dev/example/pull/42)) by [@alice](https://github.com/alice),
  [@bob](https://github.com/bob) and [@carol](https://github.com/carol).

<a name="release-1-2-2"></a>

## 1.2.2 (2026-10-17)

### Fixed

- Old change.
"""
    context = ReleaseContext(
        tag="1.2.3",
        repository="tox-dev/example",
        previous="1.2.2",
        artifact_url="https://pypi.org/project/example/1.2.3/",
    )
    result = render_markdown(changelog, context)
    assert (
        result
        == """\
<a name="release-1-2-3-added"></a>

### Features

- New option ([#42](https://github.com/tox-dev/example/pull/42)) by @alice, @bob and @carol.

[PyPI release](https://pypi.org/project/example/1.2.3/)

**Full Changelog**: https://github.com/tox-dev/example/compare/1.2.2...1.2.3
"""
    )


def test_render_markdown_first_release_without_artifact() -> None:
    result = render_markdown("## 0.1.0 (2026-02-13)\n", ReleaseContext(tag="0.1.0", repository="tox-dev/example"))
    assert result == "**Full Changelog**: https://github.com/tox-dev/example/commits/0.1.0\n"


@pytest.mark.parametrize(
    ("changelog", "overrides", "message"),
    [
        ("## 1.2.3 (today)\n", {"tag": "bad/tag"}, "invalid release tag"),
        ("## 1.2.3 (today)\n", {"previous": "bad/tag"}, "invalid previous tag"),
        ("## 1.2.3 (today)\n", {"repository": "bad"}, "invalid repository"),
        ("## 1.2.3 (today)\n", {"artifact_url": "http://bad"}, "artifact URL"),
        ("", {}, "found 0"),
        ("## 1.2.3 (today)\n## 1.2.3 (today)\n", {}, "found 2"),
        ("## 1.2.3 (today)\n### Maintenance\n", {}, "unknown changelog category"),
    ],
    ids=["tag", "previous", "repository", "artifact", "absent", "duplicate", "category"],
)
def test_render_markdown_rejects_invalid_input(
    changelog: str,
    overrides: dict[str, str],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        render_markdown(changelog, replace(ReleaseContext(tag="1.2.3", repository="tox-dev/example"), **overrides))


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
