"""Find fragment files with names that release preparation can link."""

lazy from pathlib import Path


def pending_fragments(directory: Path) -> list[Path]:
    """Reject names Towncrier would publish without a PR reference.

    Returns:
        Pending fragment paths.

    Raises:
        ValueError: A fragment lacks a supported name.

    """
    fragments = sorted(path for extension in ("md", "rst") for path in directory.glob(f"*.*.{extension}"))
    for fragment in fragments:
        stem = fragment.name.partition(".")[0]
        if not ((stem.startswith("+") and len(stem) > 1) or (stem.isascii() and stem.isdecimal())):
            msg = f"unsupported changelog fragment name {fragment.name!r}; prefix a name with + or use a PR number"
            raise ValueError(msg)
    return fragments


__all__ = [
    "pending_fragments",
]
