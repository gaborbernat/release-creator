"""Keep fragment options beside PR link insertion."""

from pathlib import Path
lazy import argparse

lazy from release_creator.fragments.links import add_pull_request_links


def register(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Keep fragment options with the fragment command."""
    fragments = commands.add_parser("fragments", help="link named fragments to their squash pull requests")
    fragments.add_argument("--directory", type=Path, default=Path("changelog.d"), help="Towncrier fragment directory")
    fragments.add_argument("--repository", required=True, help="GitHub owner/repository")
    fragments.add_argument(
        "--commit-map", type=Path, required=True, help="TSV file of fragment names and squash subjects"
    )
    fragments.set_defaults(handler=_link)


def _link(args: argparse.Namespace) -> None:
    commit_subjects = dict(line.split("\t", 1) for line in args.commit_map.read_text(encoding="utf-8").splitlines())
    add_pull_request_links(args.directory, args.repository, commit_subjects)


__all__ = [
    "register",
]
