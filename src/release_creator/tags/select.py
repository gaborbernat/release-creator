"""Validate numeric tags and find their predecessors."""


def parse_tag(tag: str) -> tuple[int, int, int]:
    """Parse a major.minor.patch release tag.

    Returns:
        The numeric major, minor, and patch components.

    Raises:
        ValueError: The tag is not a numeric release version.

    """
    match tag.split("."):
        case [major, minor, patch] if all(part.isascii() and part.isdecimal() for part in (major, minor, patch)):
            return int(major), int(minor), int(patch)
        case _:
            msg = f"expected a major.minor.patch version: {tag}"
            raise ValueError(msg)


def previous_tag(tag: str, tags: list[str]) -> str | None:
    """Select the greatest numeric release tag before ``tag``.

    Returns:
        The preceding tag, or ``None`` when this is the first release.

    """
    target = parse_tag(tag)
    candidates: list[tuple[tuple[int, int, int], str]] = []
    for candidate in tags:
        try:
            version = parse_tag(candidate)
        except ValueError:
            continue
        if version < target:
            candidates.append((version, candidate))
    return max(candidates, default=((), ""))[1] or None


def require_newer_tag(tag: str, tags: list[str]) -> None:
    """Require ``tag`` to follow every existing numeric release tag.

    Raises:
        ValueError: A matching or newer release tag already exists.

    """
    target = parse_tag(tag)
    versions: list[tuple[int, int, int]] = []
    for candidate in tags:
        try:
            versions.append(parse_tag(candidate))
        except ValueError:
            continue
    if versions and target <= max(versions):
        msg = f"{tag} must be newer than the latest release tag"
        raise ValueError(msg)


__all__ = [
    "parse_tag",
    "previous_tag",
    "require_newer_tag",
]
