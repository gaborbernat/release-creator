"""Render release notes from tagged changelogs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

import mdformat

__all__ = ["ReleaseContext", "render_markdown"]

_VERSION: Final = re.compile(r"^## (?P<tag>[^\s(]+)(?: \([^)]*\))?$")
_VERSION_ANCHOR: Final = re.compile(r'^<a name="release-v?\d+(?:-\d+){2}"></a>$')
_AUTHOR: Final = re.compile(r"\[@(?P<handle>[A-Za-z0-9-]+)\]\(https://github\.com/(?P=handle)\)")
_CATEGORIES: Final = {
    "Added": "Features",
    "Changes": "Changes",
    "Fixed": "Bug fixes",
    "Documentation": "Documentation",
    "Breaking changes": "Breaking changes",
    "Security": "Security",
    "Performance": "Performance",
    "Deprecated": "Deprecations",
    "Removed": "Removals",
    "Packaging": "Packaging",
}


@dataclass(frozen=True, kw_only=True)
class ReleaseContext:
    """Links and identity for one GitHub Release."""

    tag: str
    repository: str
    previous: str | None = None
    artifact_url: str | None = None
    artifact_label: str = "PyPI release"


def render_markdown(changelog: str, context: ReleaseContext) -> str:
    """Render one Markdown release section for GitHub without wrapped list items.

    Returns:
        The complete GitHub Release body.


    """
    _validate_context(context)
    notes = mdformat.text(_extract_body(changelog, context.tag), options={"wrap": "no"}, extensions={"gfm"}).strip()
    if context.artifact_url is not None:
        link = f"[{context.artifact_label}]({context.artifact_url})"
        notes = f"{notes}\n\n{link}" if notes else link
    comparison = (
        f"compare/{context.previous}...{context.tag}" if context.previous is not None else f"commits/{context.tag}"
    )
    if notes:
        notes += "\n\n"
    return f"{notes}**Full Changelog**: https://github.com/{context.repository}/{comparison}\n"


def _validate_context(context: ReleaseContext) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", context.tag):
        msg = f"invalid release tag: {context.tag}"
        raise ValueError(msg)
    if context.previous is not None and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", context.previous):
        msg = f"invalid previous tag: {context.previous}"
        raise ValueError(msg)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", context.repository):
        msg = f"invalid repository: {context.repository}"
        raise ValueError(msg)
    if context.artifact_url is not None and not context.artifact_url.startswith("https://"):
        msg = "artifact URL must use HTTPS"
        raise ValueError(msg)


def _extract_body(changelog: str, tag: str) -> str:
    lines = changelog.splitlines()
    headings = [
        index for index, line in enumerate(lines) if (match := _VERSION.fullmatch(line)) and match["tag"] == tag
    ]
    if len(headings) != 1:
        msg = f"expected one changelog section for {tag}, found {len(headings)}"
        raise ValueError(msg)

    body: list[str] = []
    for source_line in lines[headings[0] + 1 :]:
        if _VERSION.fullmatch(source_line) or _VERSION_ANCHOR.fullmatch(source_line):
            break
        line = source_line
        if source_line.startswith("### "):
            category = source_line[4:]
            if category not in _CATEGORIES:
                msg = f"unknown changelog category: {category}"
                raise ValueError(msg)
            line = f"### {_CATEGORIES[category]}"
        body.append(_AUTHOR.sub(lambda match: f"@{match['handle']}", line))

    return "\n".join(body).strip()
