from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dnl_config import DnlConfig, load_dnl_config
from dnl_util_core.commands import tag_index
from qa import should_validate_yaml_frontmatter
from yaml_header import TAG_PATTERN_TEXT, TAG_VALUE, extract_frontmatter, parse_dnl_header


@dataclass
class TagAddSummary:
    mode: str
    scanned: int = 0
    eligible: int = 0
    changed: int = 0
    would_change: int = 0
    already_tagged: int = 0
    skipped: int = 0
    invalid: int = 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    tag_parser = subparsers.add_parser("tag", help="Tag utilities.")
    tag_subparsers = tag_parser.add_subparsers(dest="tag_command", required=True)
    tag_index.register(tag_subparsers)

    add_parser = tag_subparsers.add_parser(
        "add",
        help="Add one tag to DNL markdown files.",
    )
    add_parser.add_argument(
        "--path",
        "--dir",
        dest="path",
        required=True,
        help="Target markdown file or directory. Relative paths are resolved from --root.",
    )
    add_parser.add_argument("--tag", required=True, help="Tag to add.")
    add_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories when --path points to a directory.",
    )
    mode = add_parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--write",
        action="store_true",
        help="Write changes. Without this flag, the command only reports a dry run.",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing. This is the default.",
    )
    add_parser.set_defaults(func=run_add)


def run_add(args: argparse.Namespace) -> int:
    if TAG_VALUE.match(args.tag) is None:
        print(
            f"ERROR: invalid tag: {args.tag} (must match {TAG_PATTERN_TEXT})",
            file=sys.stderr,
        )
        return 2

    try:
        root = resolve_root(args.root)
        target = resolve_target(root, args.path)
        config = load_dnl_config(root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    mode = "write" if args.write else "dry-run"
    summary = TagAddSummary(mode=mode)

    for path in iter_markdown_paths(target, recursive=args.recursive):
        summary.scanned += 1
        rel_path = path.relative_to(root).as_posix()

        if not should_process_file(root, rel_path, config):
            summary.skipped += 1
            continue

        summary.eligible += 1
        result = add_tag_to_file(path, args.tag, write=args.write)

        if result == "changed":
            summary.changed += 1
        elif result == "would_change":
            summary.would_change += 1
        elif result == "already_tagged":
            summary.already_tagged += 1
        elif result == "invalid":
            summary.invalid += 1
        else:
            summary.skipped += 1

    print(format_summary(summary))
    return 1 if summary.invalid else 0


def resolve_root(raw_root: str | None) -> Path:
    if raw_root:
        root = Path(raw_root).expanduser().resolve()
    else:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            root = Path.cwd().resolve()
        else:
            root = Path(completed.stdout.strip()).resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError(f"root does not exist or is not a directory: {root}")
    return root


def resolve_target(root: Path, raw_path: str) -> Path:
    target = Path(raw_path).expanduser()
    if not target.is_absolute():
        target = root / target
    target = target.resolve()

    if not target.exists():
        raise ValueError(f"path does not exist: {target}")

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path must be inside root: {target}") from exc

    return target


def iter_markdown_paths(target: Path, *, recursive: bool) -> Iterable[Path]:
    if target.is_file():
        if target.suffix == ".md":
            yield target
        return

    pattern = "**/*.md" if recursive else "*.md"
    yield from sorted(target.glob(pattern))


def should_process_file(root: Path, rel_path: str, config: DnlConfig) -> bool:
    if not should_validate_yaml_frontmatter(rel_path, config.scan_include):
        return False
    if tag_index.is_in_excluded_dir(rel_path, config.scan_exclude):
        return False
    return not is_gitignored(root, rel_path)


def is_gitignored(root: Path, rel_path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", "--", rel_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def add_tag_to_file(path: Path, tag: str, *, write: bool) -> str:
    text = path.read_text(encoding="utf-8")
    next_text = add_tag_to_text(text, tag)

    if next_text is None:
        return "invalid"
    if next_text == text:
        return "already_tagged"
    if not write:
        return "would_change"

    path.write_text(next_text, encoding="utf-8")
    return "changed"


def add_tag_to_text(text: str, tag: str) -> str | None:
    frontmatter, _ = extract_frontmatter(text)
    if frontmatter is None:
        return None

    header = parse_dnl_header(text)
    if header.errors:
        return None
    if tag in header.tags:
        return text

    lines = text.splitlines(keepends=True)
    closing_index = find_frontmatter_end(lines)
    if closing_index is None:
        return None

    next_tags = [*header.tags, tag]
    for index in range(1, closing_index):
        if lines[index].startswith("tags:"):
            lines[index] = f"tags: {format_inline_tags(next_tags)}{line_ending(lines[index])}"
            return "".join(lines)

    return None


def find_frontmatter_end(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index
    return None


def format_inline_tags(tags: list[str]) -> str:
    if not tags:
        return "[]"
    return "[" + ", ".join(f'"{tag}"' for tag in tags) + "]"


def line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def format_summary(summary: TagAddSummary) -> str:
    return (
        "TAG ADD: "
        f"mode={summary.mode} "
        f"scanned={summary.scanned} "
        f"eligible={summary.eligible} "
        f"changed={summary.changed} "
        f"would_change={summary.would_change} "
        f"already_tagged={summary.already_tagged} "
        f"skipped={summary.skipped} "
        f"invalid={summary.invalid}"
    )
