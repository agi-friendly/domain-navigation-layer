#!/usr/bin/env python3
"""Optional, read-only DNL document size hints for human review."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dnl_config import DnlConfigError, is_dnl_search_target, load_dnl_config
from qa import should_skip_dir
from yaml_header import parse_dnl_header


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def collect_files(root: Path, targets: list[str], exclude: set[str]) -> list[Path]:
    files: set[Path] = set()

    def eligible(path: Path) -> bool:
        relative = path.relative_to(root).as_posix()
        return (
            not path.is_symlink()
            and not (path.is_dir() and path.name.startswith(".") and path != root)
            and not should_skip_dir(relative, exclude)
            and is_dnl_search_target(relative)
        )

    def walk_error(error: OSError) -> None:
        raise error

    for target in targets:
        path = (root / target).absolute()
        # Keep this inspection within the chosen repository, including symlinks.
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError(f"target is outside root: {target}")
        if not path.exists():
            raise ValueError(f"target does not exist: {target}")
        if path.is_symlink():
            continue
        path = resolved
        if not eligible(path):
            continue
        if path.is_file():
            if path.suffix != ".md":
                raise ValueError(f"target must be a Markdown file or directory: {target}")
            files.add(path)
            continue
        for directory, dirs, names in os.walk(path, onerror=walk_error):
            base = Path(directory)
            dirs[:] = [
                name for name in dirs
                if not name.startswith(".") and eligible(base / name)
            ]
            for name in names:
                candidate = base / name
                if candidate.suffix == ".md" and eligible(candidate):
                    files.add(candidate)
    return sorted(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets", nargs="*", help="Markdown files or directories relative to --root"
    )
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2],
        help="repository root (default: this script's repository)",
    )
    parser.add_argument(
        "--paths-threshold", type=positive_int, default=15,
        help="warn when paths count is at least this number (default: 15)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise ValueError(f"root is not a directory: {root}")
        config = load_dnl_config(root)
        files = collect_files(
            root, args.targets or list(config.scan_include), set(config.scan_exclude)
        )
    except (OSError, ValueError, DnlConfigError) as exc:
        parser.error(str(exc))

    warnings: list[tuple[int, str]] = []
    errors = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            header = parse_dnl_header(path.read_text(encoding="utf-8"))
            # A partial parse can undercount paths and give a false clean result.
            if header.errors:
                raise ValueError("; ".join(header.errors))
        except (OSError, UnicodeError, ValueError) as exc:
            print(f"ERROR {relative}: {exc}", file=sys.stderr)
            errors += 1
            continue
        count = len(header.paths)
        if count >= args.paths_threshold:
            warnings.append((count, relative))

    for count, relative in sorted(warnings, key=lambda item: (-item[0], item[1])):
        print(f"WARNING paths={count} (>= {args.paths_threshold}) {relative}")
    print(
        f"Scanned {len(files)} Markdown files: {len(warnings)} warnings, {errors} errors. "
        "Warnings are review hints, not mandatory splits."
    )
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
