#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
from typing import Iterable


DEFAULT_IGNORES = [
    ".git", 
    ".idea", 
    ".vscode",
    "node_modules", 
    "dist", 
    "build", 
    ".svelte-kit",
    "__pycache__", 
    ".pytest_cache", ".mypy_cache",
    "*.log", 
    "*.tmp",
]


def should_ignore(name: str, patterns: Iterable[str]) -> bool:
    for p in patterns:
        if fnmatch.fnmatch(name, p):
            return True
    return False


def tree_lines(
    root: Path,
    *,
    include_files: bool,
    max_depth: int,
    ignore: list[str],
    show_hidden: bool,
) -> list[str]:
    root = root.resolve()
    lines: list[str] = [str(root)]

    def walk(dir_path: Path, prefix: str, depth: int) -> None:
        if max_depth >= 0 and depth > max_depth:
            return

        try:
            entries = list(dir_path.iterdir())
        except PermissionError:
            lines.append(prefix + "└── [PermissionError]")
            return

        # hidden 처리
        if not show_hidden:
            entries = [e for e in entries if not e.name.startswith(".")]

        # ignore 처리(이름 기준)
        entries = [e for e in entries if not should_ignore(e.name, ignore)]

        # 폴더 먼저, 그 다음 파일 (보기 좋게)
        dirs = sorted([e for e in entries if e.is_dir()], key=lambda x: x.name.lower())
        files = sorted([e for e in entries if e.is_file()], key=lambda x: x.name.lower())

        if include_files:
            ordered = dirs + files
        else:
            ordered = dirs

        for i, entry in enumerate(ordered):
            is_last = (i == len(ordered) - 1)
            branch = "└── " if is_last else "├── "
            lines.append(prefix + branch + entry.name)

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                walk(entry, prefix + extension, depth + 1)

    walk(root, "", 0)
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Cross-platform tree generator (good for DNL mapping)."
    )
    ap.add_argument("path", nargs="?", default=".", help="root directory (default: .)")
    ap.add_argument("--files", action="store_true", help="include files")
    ap.add_argument("--depth", type=int, default=4, help="max depth, -1 = unlimited (default: 4)")
    ap.add_argument("--hidden", action="store_true", help="include hidden entries")
    ap.add_argument("--ignore", action="append", default=[], help="ignore pattern (repeatable)")
    ap.add_argument("--out", default="", help="write output to file (utf-8)")

    args = ap.parse_args()

    ignore = DEFAULT_IGNORES + (args.ignore or [])
    lines = tree_lines(
        Path(args.path),
        include_files=args.files,
        max_depth=args.depth,
        ignore=ignore,
        show_hidden=args.hidden,
    )
    text = "\n".join(lines) + "\n"

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
