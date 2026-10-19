"""Command line entry point for release-creator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

lazy from release_creator.notes.fragments import add_pull_request_links
lazy from release_creator.notes.render import ReleaseContext, render_markdown, render_rst


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
    notes.add_argument("--issue-role", choices=("issue", "pull"), default="issue")
    notes.add_argument("--generated-notes", type=Path)
    fragments = commands.add_parser("fragments", help="link named fragments to their squash pull requests")
    fragments.add_argument("--directory", type=Path, default=Path("changelog.d"))
    fragments.add_argument("--repository", required=True)
    fragments.add_argument("--commit-map", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "fragments":
            _prepare_fragments(args)
        else:
            _render_notes(args)
    except (OSError, ValueError) as error:
        parser.error(str(error))


def _prepare_fragments(args: argparse.Namespace) -> None:
    commit_subjects = dict(line.split("\t", 1) for line in args.commit_map.read_text(encoding="utf-8").splitlines())
    add_pull_request_links(args.directory, args.repository, commit_subjects)


def _render_notes(args: argparse.Namespace) -> None:
    renderer = render_rst if args.changelog.suffix == ".rst" else render_markdown
    context = ReleaseContext(
        tag=args.tag,
        repository=args.repository,
        previous=args.previous,
        artifact_url=args.artifact_url,
        artifact_label=args.artifact_label,
    )
    changelog = args.changelog.read_text(encoding="utf-8")
    generated_notes = args.generated_notes.read_text(encoding="utf-8") if args.generated_notes else None
    sys.stdout.write(
        renderer(changelog, context, args.issue_role, generated_notes)
        if renderer is render_rst
        else renderer(changelog, context, generated_notes)
    )


__all__ = [
    "main",
]
