"""Read introducing squash subjects from Git history."""

import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]  # Fragment provenance comes from the local Git checkout.
lazy from pathlib import Path

lazy from release_creator.fragments.names import pending_fragments


def commit_subjects_from_git(directory: Path) -> dict[str, str]:
    """Read the commit subject that first added each fragment.

    Returns:
        Fragment filenames mapped to their introducing subjects.

    Raises:
        FileNotFoundError: Git is not installed.
        ValueError: Git cannot read the checkout history.

    """
    if (git := shutil.which("git")) is None:
        msg = "Git is required to read fragment history"
        raise FileNotFoundError(msg)
    subjects: dict[str, str] = {}
    for fragment in pending_fragments(directory):
        result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]  # Fixed Git command; the fragment path is a separate argument.
            [git, "log", "-1", "--format=%s", "--diff-filter=A", "HEAD", "--", str(fragment)],
            capture_output=True,
            check=False,
            text=True,
        )
        if result.returncode:
            msg = result.stderr.strip() or f"could not read Git history for {fragment}"
            raise ValueError(msg)
        subjects[fragment.name] = result.stdout.strip()
    return subjects


__all__ = [
    "commit_subjects_from_git",
]
