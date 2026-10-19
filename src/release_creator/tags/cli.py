"""Keep tag selection options beside the command."""

import sys
lazy import argparse

lazy from release_creator.tags.select import parse_tag, previous_tag, require_newer_tag


def register(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Register numeric tag validation and predecessor selection."""
    tags = commands.add_parser("tags", help="validate numeric release tags or find the previous one")
    tags.add_argument("tag", help="major.minor.patch release tag")
    choice = tags.add_mutually_exclusive_group()
    choice.add_argument("--previous", action="store_true", help="print the preceding tag from standard input")
    choice.add_argument("--require-newer", action="store_true", help="require a tag newer than those on standard input")
    tags.set_defaults(handler=_select)


def _select(args: argparse.Namespace) -> None:
    parse_tag(args.tag)
    if not args.previous and not args.require_newer:
        return
    tags = sys.stdin.read().splitlines()
    if args.require_newer:
        require_newer_tag(args.tag, tags)
    elif (previous := previous_tag(args.tag, tags)) is not None:
        sys.stdout.write(f"{previous}\n")


__all__ = [
    "register",
]
