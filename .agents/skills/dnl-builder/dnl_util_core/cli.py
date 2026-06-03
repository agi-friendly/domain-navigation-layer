from __future__ import annotations

import argparse

from dnl_util_core.commands import link, tag


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dnl_util.py",
        description="DNL maintenance utilities.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the current git worktree root.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    link.register(subparsers)
    tag.register(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
