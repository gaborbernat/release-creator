"""Render release notes from tagged changelogs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

lazy import mdformat

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


def render_markdown(changelog: str, context: ReleaseContext, generated_notes: str | None = None) -> str:
    """Render one Markdown release section for GitHub without wrapped list items.

    Returns:
        The complete GitHub Release body.


    """
    _validate_context(context)
    notes = mdformat.text(_extract_body(changelog, context.tag), options={"wrap": "no"}, extensions={"gfm"}).strip()
    return _finish(notes, context, generated_notes)


def render_rst(
    changelog: str, context: ReleaseContext, issue_role: str = "issue", generated_notes: str | None = None
) -> str:
    """Render one reStructuredText release section for GitHub.

    Returns:
        The complete GitHub Release body.

    Raises:
        ValueError: The issue role must name a GitHub issue or pull request.

    """
    _validate_context(context)
    if issue_role not in {"issue", "pull"}:
        msg = f"invalid issue role: {issue_role}"
        raise ValueError(msg)
    notes = mdformat.text(
        _extract_rst_body(changelog, context, issue_role), options={"wrap": "no"}, extensions={"gfm"}
    ).strip()
    return _finish(notes, context, generated_notes)


def _finish(notes: str, context: ReleaseContext, generated_notes: str | None) -> str:
    if generated_notes is not None and (contributors := _new_contributors(notes, generated_notes, context.tag)):
        notes = f"{notes}\n\n{contributors}" if notes else contributors
    if context.artifact_url is not None:
        link = f"[{context.artifact_label}]({context.artifact_url})"
        notes = f"{notes}\n\n{link}" if notes else link
    comparison = (
        f"compare/{context.previous}...{context.tag}" if context.previous is not None else f"commits/{context.tag}"
    )
    if notes:
        notes += "\n\n"
    return f"{notes}**Full Changelog**: https://github.com/{context.repository}/{comparison}\n"


def _new_contributors(notes: str, generated_notes: str, tag: str) -> str:
    if (section := re.search(r"(?ms)^## New Contributors\s*\n(?P<entries>.*?)(?=^## |\Z)", generated_notes)) is None:
        return ""
    credited = set(re.findall(r"@([A-Za-z0-9-]+)", notes))
    entries = [
        f"- @{match['handle']} made their first contribution in #{match['number']}"
        for line in section["entries"].splitlines()
        if (
            match := re.fullmatch(
                r"[-*] @(?P<handle>[A-Za-z0-9-]+) made their first contribution in #(?P<number>\d+)",
                line.strip(),
            )
        )
        and match["handle"] in credited
    ]
    if not entries:
        return ""
    anchor = f"release-{tag.replace('.', '-')}-new-contributors"
    return f'<a name="{anchor}"></a>\n\n### New Contributors\n\n' + "\n".join(entries)


def _extract_rst_body(changelog: str, context: ReleaseContext, issue_role: str) -> str:
    lines = changelog.splitlines()
    version = re.compile(r"^v?(?P<tag>\d+\.\d+\.\d+) \([^)]+\)$")
    headings = [
        index
        for index, line in enumerate(lines)
        if (match := version.fullmatch(line.strip())) and match["tag"] == context.tag.removeprefix("v")
    ]
    if len(headings) != 1:
        msg = f"expected one changelog section for {context.tag}, found {len(headings)}"
        raise ValueError(msg)
    end = next(
        (index for index in range(headings[0] + 1, len(lines)) if version.fullmatch(lines[index].strip())),
        len(lines),
    )
    sections: dict[str, list[str]] = {}
    category: str | None = None
    index = headings[0] + 1
    while index < end:
        line = lines[index].strip()
        if index + 1 < end and re.fullmatch(r"[-=~^]{3,}", lines[index + 1].strip()):
            category = _require_category(line)
            sections.setdefault(category, [])
            index += 2
            continue
        if line.startswith("- "):
            if category is None:
                msg = f"release item outside a category: {line}"
                raise ValueError(msg)
            sections[category].append(_convert_rst(line, context.repository, issue_role))
        elif line and line[0] not in "*=~^" and not line.startswith(".. _"):
            if category is None or not sections[category]:
                msg = f"unexpected release text: {line}"
                raise ValueError(msg)
            sections[category][-1] += f" {_convert_rst(line, context.repository, issue_role)}"
        index += 1
    body: list[str] = []
    for name, entries in sections.items():
        if entries:
            anchor = f"release-{context.tag.replace('.', '-')}-{name.lower().replace(' ', '-')}"
            body.extend((f'<a name="{anchor}"></a>', "", f"### {_CATEGORIES[name]}", "", *entries, ""))
    return "\n".join(body).strip()


def _require_category(name: str) -> str:
    if name not in _CATEGORIES:
        msg = f"unknown changelog category: {name}"
        raise ValueError(msg)
    return name


def _convert_rst(line: str, repository: str, issue_role: str) -> str:
    issue_target = "pull" if issue_role == "pull" else "issues"
    line = re.sub(
        r":(?:pr|pull):`(?P<number>\d+)`",
        lambda match: f"[#{match['number']}](https://github.com/{repository}/pull/{match['number']})",
        line,
    )
    line = re.sub(
        r":issue:`(?P<number>\d+)`",
        lambda match: f"[#{match['number']}](https://github.com/{repository}/{issue_target}/{match['number']})",
        line,
    )
    line = re.sub(r":user:`(?P<handle>[A-Za-z0-9-]+)`", lambda match: f"@{match['handle']}", line)
    line = re.sub(
        r"`@(?P<handle>[A-Za-z0-9-]+) <https://github\.com/(?P=handle)>`_", lambda match: f"@{match['handle']}", line
    )
    line = re.sub(r"``([^`]+)``", r"`\1`", line)
    line = re.sub(r":(?:[a-z]+:)?[a-z]+:`~?([^`]+)`", lambda match: f"`{match[1].split('.')[-1]}`", line)
    return line.replace(" - by ", " by ")


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
    version = re.compile(r"^## (?P<tag>[^\s(]+)(?: \([^)]*\))?$")
    lines = changelog.splitlines()
    headings = [index for index, line in enumerate(lines) if (match := version.fullmatch(line)) and match["tag"] == tag]
    if len(headings) != 1:
        msg = f"expected one changelog section for {tag}, found {len(headings)}"
        raise ValueError(msg)

    body: list[str] = []
    version_anchor = re.compile(r'^<a name="release-v?\d+(?:-\d+){2}"></a>$')
    author = re.compile(r"\[@(?P<handle>[A-Za-z0-9-]+)\]\(https://github\.com/(?P=handle)\)")
    for source_line in lines[headings[0] + 1 :]:
        if version.fullmatch(source_line) or version_anchor.fullmatch(source_line):
            break
        line = source_line
        if source_line.startswith("### "):
            category = source_line[4:]
            if category not in _CATEGORIES:
                msg = f"unknown changelog category: {category}"
                raise ValueError(msg)
            line = f"### {_CATEGORIES[category]}"
        body.append(author.sub(lambda match: f"@{match['handle']}", line))

    return "\n".join(body).strip()


__all__ = [
    "ReleaseContext",
    "render_markdown",
    "render_rst",
]
