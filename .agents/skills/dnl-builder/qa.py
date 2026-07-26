#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path

LEGACY_PATH = ".agents/skills/dnl-builder/qa.py"
CANONICAL_PATH = "scripts/dnl/qa.py"


def find_repo_root(start: Path) -> Path:
    current = start.absolute()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
        if (candidate / CANONICAL_PATH).is_file():
            return candidate
    return start.absolute().parents[3]


def main() -> int:
    repo_root = find_repo_root(Path(__file__))
    target = repo_root / CANONICAL_PATH
    print(
        f"[deprecated] {LEGACY_PATH} is a compatibility shim; "
        f"use {CANONICAL_PATH} instead.",
        file=sys.stderr,
        flush=True,
    )
    if not target.is_file():
        print(f"[error] {CANONICAL_PATH} not found: {target}", file=sys.stderr)
        return 2

    sys.path.insert(0, str(target.parent))
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
