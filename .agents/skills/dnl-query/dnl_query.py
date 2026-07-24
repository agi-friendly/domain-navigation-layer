#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "scripts" / "dnl" / "query.py").is_file():
            return candidate
    return start.resolve().parents[3]


def main() -> int:
    repo_root = find_repo_root(Path(__file__))
    target = repo_root / "scripts" / "dnl" / "query.py"
    if not target.is_file():
        print(f"[error] scripts/dnl/query.py not found: {target}", file=sys.stderr)
        return 2
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
