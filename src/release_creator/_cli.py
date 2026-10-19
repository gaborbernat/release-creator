"""Command line entry point for release-creator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from release_creator._notes import ReleaseContext, render_markdown

__all__ = ["main"]


def main() -> None:
    """Dispatch release preparation commands."""
    parser = argparse.ArgumentParser(description="Release preparation tools")
    commands = parser.add_subparsers(dest="command", required=True)
    notes = commands.add_parser("notes", help="render notes from a tagged changelog")
    notes.add_argument("--changelog", type=Path, required=True)
    notes.add_argument("--tag", required=True)
    notes.add_argument("--repository", required=True)
    notes.add_argument("--previous")
    notes.add_argument("--artifact-url")
    notes.add_argument("--artifact-label", default="PyPI release")
    args = parser.parse_args()
    try:
        sys.stdout.write(
            render_markdown(
                args.changelog.read_text(encoding="utf-8"),
                ReleaseContext(
                    tag=args.tag,
                    repository=args.repository,
                    previous=args.previous,
                    artifact_url=args.artifact_url,
                    artifact_label=args.artifact_label,
                ),
            )
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))
