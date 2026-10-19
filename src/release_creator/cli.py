"""Keep command registration separate from release work."""

import argparse

lazy from release_creator.fragments.cli import register as register_fragments
lazy from release_creator.notes.cli import register as register_notes


def main() -> None:
    """Report command input errors through argparse's exit path."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.handler(args)
    except (OSError, ValueError) as error:
        parser.error(str(error))


def build_parser() -> argparse.ArgumentParser:
    """Expose the same parser to Sphinx and the executable.

    Returns:
        Parser shared by the documentation and command line.

    """
    parser = argparse.ArgumentParser(description="Release preparation tools")
    commands = parser.add_subparsers(dest="command", required=True)
    register_notes(commands)
    register_fragments(commands)
    return parser


__all__ = [
    "build_parser",
    "main",
]
