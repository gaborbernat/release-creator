"""Associate named Towncrier fragments with merged pull requests."""

from __future__ import annotations

import re
lazy from pathlib import Path


def add_pull_request_links(directory: Path, repository: str, commit_subjects: dict[str, str]) -> None:
    """Add pull request links to named fragments using squash commit subjects.

    Raises:
        ValueError: A fragment has no unambiguous squash commit or already names a pull request.

    """
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        msg = f"invalid repository: {repository}"
        raise ValueError(msg)
    for fragment in sorted(directory.glob("+*.*")):
        subject = commit_subjects.get(fragment.name, "")
        if (match := re.search(r"\(#(?P<number>\d+)\)$", subject)) is None:
            msg = f"no squash pull request number for {fragment}: {subject}"
            raise ValueError(msg)
        content = fragment.read_text(encoding="utf-8").rstrip()
        if re.search(rf"https://github\.com/{re.escape(repository)}/pull/\d+", content):
            msg = f"pull request already linked in {fragment}"
            raise ValueError(msg)
        link = f"([#{match['number']}](https://github.com/{repository}/pull/{match['number']}))"
        if re.search(r"\s+by\s+(?=\[@|:user:)", content):
            content = re.sub(r"\s+by\s+(?=\[@|:user:)", f" {link} by ", content, count=1)
        else:
            content = f"{content.removesuffix('.')} {link}."
        fragment.write_text(f"{content}\n", encoding="utf-8")


__all__ = [
    "add_pull_request_links",
]
