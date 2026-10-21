"""Validate changed Towncrier fragments in a pull request."""

import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]  # Git checks the PR diff without a shell.
lazy import tomllib
lazy from pathlib import Path


def changed_fragments(config: Path, base: str) -> int:
    """Count valid added or modified fragments relative to the PR base.

    Returns:
        Number of changed fragments.

    Raises:
        FileNotFoundError: Git is unavailable.
        ValueError: The configuration or a changed fragment is invalid.

    """
    towncrier = tomllib.loads(config.read_text(encoding="utf-8"))["tool"]["towncrier"]
    directory = Path(towncrier["directory"])
    suffix = Path(towncrier["filename"]).suffix
    categories = {item["directory"] for item in towncrier["type"]}
    if not base or suffix not in {".md", ".rst"}:
        msg = "news validation needs a PR base and a Markdown or reStructuredText changelog"
        raise ValueError(msg)
    if (git := shutil.which("git")) is None:
        msg = "Git is required to validate changelog fragments"
        raise FileNotFoundError(msg)
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]  # Git argument list has no shell.
        [git, "diff", "--diff-filter=AM", "--name-only", "-z", f"origin/{base}...HEAD", "--", str(directory)],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        msg = result.stderr.decode().strip() or f"could not compare changelog fragments with origin/{base}"
        raise ValueError(msg)
    count = 0
    for filename in result.stdout.decode().strip("\0").split("\0"):
        path = Path(filename)
        if not filename or path.parent != directory or path.suffix != suffix:
            continue
        match path.stem.rsplit(".", 2):
            case [stem, category, number] if number.isdecimal():
                pass
            case [*stem_parts, category] if stem_parts:
                stem = ".".join(stem_parts)
            case _:
                continue
        if not ((stem.startswith("+") and len(stem) > 1) or stem.isdigit()) or category not in categories:
            msg = f"unsupported changelog fragment: {path}"
            raise ValueError(msg)
        if not path.read_text(encoding="utf-8").strip():
            msg = f"empty changelog fragment: {path}"
            raise ValueError(msg)
        count += 1
    return count


__all__ = [
    "changed_fragments",
]
