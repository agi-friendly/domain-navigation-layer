from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dnl_config import DnlConfig, is_dnl_search_target, load_dnl_config
from qa import has_tags_field
from yaml_header import parse_dnl_header


DEFAULT_INDEX_DIR = ".agents/skills/dnl-query/tag-index"
SCHEMA_VERSION = 1
STATUSES = ["active", "draft", "deprecated"]


@dataclass
class IndexBuild:
    entries: list[dict[str, object]]
    invalid: list[str]
    files: dict[str, str]


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    index_parser = subparsers.add_parser("index", help="Build and check tag index files.")
    index_subparsers = index_parser.add_subparsers(dest="index_command", required=True)

    build_parser = index_subparsers.add_parser("build", help="Rebuild the full tag index.")
    build_parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_DIR,
        help=f"Index output directory. Defaults to {DEFAULT_INDEX_DIR}.",
    )
    build_parser.set_defaults(func=run_build)

    check_parser = index_subparsers.add_parser("check", help="Check whether the tag index is stale.")
    check_parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_DIR,
        help=f"Index output directory. Defaults to {DEFAULT_INDEX_DIR}.",
    )
    check_parser.set_defaults(func=run_check)

    update_parser = index_subparsers.add_parser("update", help="Update the index for one markdown path.")
    update_parser.add_argument(
        "--path",
        required=True,
        help="Markdown file path to update. Relative paths are resolved from --root.",
    )
    update_parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_DIR,
        help=f"Index output directory. Defaults to {DEFAULT_INDEX_DIR}.",
    )
    update_parser.set_defaults(func=run_update)


def run_build(args: argparse.Namespace) -> int:
    try:
        root = resolve_root(args.root)
        index_dir = resolve_output_dir(root, args.output)
        build = build_current_index(root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if build.invalid:
        print(
            f"TAG INDEX BUILD: documents={len(build.entries)} tags=0 invalid={len(build.invalid)} output={index_dir.relative_to(root).as_posix()}",
        )
        print_invalid(build.invalid)
        return 1

    write_index_files(index_dir, build.files)
    print(
        f"TAG INDEX BUILD: documents={len(build.entries)} tags={tag_count(build.files)} invalid=0 output={index_dir.relative_to(root).as_posix()}"
    )
    return 0


def run_check(args: argparse.Namespace) -> int:
    try:
        root = resolve_root(args.root)
        index_dir = resolve_output_dir(root, args.output)
        build = build_current_index(root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if build.invalid:
        print(f"TAG INDEX CHECK: INVALID invalid={len(build.invalid)}")
        print_invalid(build.invalid)
        return 1

    actual_files = read_index_files(index_dir)
    expected_files = build.files
    missing = sorted(set(expected_files) - set(actual_files))
    extra = sorted(set(actual_files) - set(expected_files))
    changed = sorted(
        path
        for path in set(expected_files) & set(actual_files)
        if expected_files[path] != actual_files[path]
    )

    if missing or extra or changed:
        print(
            "TAG INDEX CHECK: STALE "
            f"changed_files={len(changed)} missing_files={len(missing)} extra_files={len(extra)}"
        )
        return 1

    print(f"TAG INDEX CHECK: OK documents={len(build.entries)} tags={tag_count(build.files)}")
    return 0


def run_update(args: argparse.Namespace) -> int:
    try:
        root = resolve_root(args.root)
        index_dir = resolve_output_dir(root, args.output)
        target = resolve_update_path(root, args.path)
        config = load_dnl_config(root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_docs_path = index_dir / "all-docs.jsonl"
    if not all_docs_path.exists():
        print(
            f"ERROR: index does not exist: {all_docs_path.relative_to(root).as_posix()} (run tag index build first)",
            file=sys.stderr,
        )
        return 2

    entries_by_path = {
        str(entry["path"]): entry for entry in read_jsonl_entries(all_docs_path)
    }
    rel_path = target.relative_to(root).as_posix()
    had_entry = rel_path in entries_by_path
    entries_by_path.pop(rel_path, None)

    action = "removed" if had_entry else "missing"
    if target.exists():
        entry, errors = parse_entry(root, target, config)
        if errors:
            print(f"TAG INDEX UPDATE: path={rel_path} action=invalid invalid=1")
            print_invalid(errors)
            return 1
        if entry is not None:
            entries_by_path[rel_path] = entry
            action = "updated" if had_entry else "added"
        elif not had_entry:
            action = "skipped"

    entries = sorted(entries_by_path.values(), key=lambda entry: str(entry["path"]))
    files = make_index_files(entries, config.scan_include)
    write_index_files(index_dir, files)
    print(
        f"TAG INDEX UPDATE: path={rel_path} action={action} documents={len(entries)} tags={tag_count(files)}"
    )
    return 0


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


def resolve_output_dir(root: Path, raw_output: str) -> Path:
    output = Path(raw_output).expanduser()
    if not output.is_absolute():
        output = root / output
    output = output.resolve()

    try:
        output.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"output must be inside root: {output}") from exc

    return output


def resolve_update_path(root: Path, raw_path: str) -> Path:
    target = Path(raw_path).expanduser()
    if not target.is_absolute():
        target = root / target
    target = target.resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path must be inside root: {target}") from exc

    return target


def build_current_index(root: Path) -> IndexBuild:
    config = load_dnl_config(root)
    markdown_paths = list(iter_candidate_markdown(root, config.scan_include))
    ignored = gitignored_paths(root, [path.relative_to(root).as_posix() for path in markdown_paths])
    entries: list[dict[str, object]] = []
    invalid: list[str] = []

    for path in markdown_paths:
        rel_path = path.relative_to(root).as_posix()
        if rel_path in ignored:
            continue

        entry, errors = parse_entry(root, path, config)
        if errors:
            invalid.extend(errors)
            continue
        if entry is not None:
            entries.append(entry)

    entries.sort(key=lambda entry: str(entry["path"]))
    return IndexBuild(entries=entries, invalid=invalid, files=make_index_files(entries, config.scan_include))


def iter_candidate_markdown(root: Path, sources: tuple[str, ...]) -> Iterable[Path]:
    for source in sources:
        start = root / source
        if not start.exists():
            continue
        if start.is_file():
            if start.suffix == ".md":
                yield start
            continue
        yield from sorted(start.glob("**/*.md"))


def gitignored_paths(root: Path, rel_paths: list[str]) -> set[str]:
    if not rel_paths:
        return set()

    completed = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "--stdin"],
        input="\n".join(rel_paths) + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode not in {0, 1}:
        return set()
    return {line.strip() for line in completed.stdout.splitlines() if line.strip()}


def parse_entry(root: Path, path: Path, config: DnlConfig) -> tuple[dict[str, object] | None, list[str]]:
    rel_path = path.relative_to(root).as_posix()
    if not is_dnl_search_target(rel_path):
        return None, []
    if not is_in_scan_sources(rel_path, config.scan_include):
        return None, []
    if is_in_excluded_dir(rel_path, config.scan_exclude):
        return None, []
    if path.suffix != ".md":
        return None, []

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    header = parse_dnl_header(text)
    errors: list[str] = []
    errors.extend(f"{rel_path}: {error}" for error in header.errors)

    if header.name is None:
        errors.append(f"{rel_path}: YAML frontmatter missing required name")
    if header.status is None:
        errors.append(f"{rel_path}: YAML frontmatter missing required status")
    if not has_tags_field(lines):
        errors.append(f"{rel_path}: YAML frontmatter missing required tags")

    if errors:
        return None, errors

    return (
        {
            "path": rel_path,
            "name": header.name or "",
            "status": header.status or "",
            "tags": header.tags,
            "description": header.description,
        },
        [],
    )


def make_index_files(entries: list[dict[str, object]], sources: tuple[str, ...]) -> dict[str, str]:
    files: dict[str, str] = {
        "all-docs.jsonl": jsonl(entries),
    }

    tags: dict[str, list[dict[str, object]]] = {}
    for entry in entries:
        for tag in entry["tags"]:
            tags.setdefault(str(tag), []).append(entry)

    manifest_tags: dict[str, dict[str, object]] = {}
    for tag in sorted(tags):
        tag_entries = sorted(tags[tag], key=lambda entry: str(entry["path"]))
        tag_file = f"tags/{tag_filename(tag)}"
        files[tag_file] = jsonl(tag_entries)
        manifest_tags[tag] = {
            "file": tag_file,
            "count": len(tag_entries),
        }

    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "sources": list(sources),
        "documents": len(entries),
        "statusCounts": status_counts(entries),
        "untaggedDocuments": untagged_documents(entries),
        "tags": manifest_tags,
    }
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    return files


def status_counts(entries: list[dict[str, object]]) -> dict[str, int]:
    counts = {status: 0 for status in STATUSES}
    for entry in entries:
        status = str(entry["status"])
        if status in counts:
            counts[status] += 1
    return counts


def untagged_documents(entries: list[dict[str, object]]) -> int:
    return sum(1 for entry in entries if not entry["tags"])


def is_in_scan_sources(rel_path: str, sources: tuple[str, ...]) -> bool:
    return any(rel_path == source or rel_path.startswith(f"{source}/") for source in sources)


def is_in_excluded_dir(rel_path: str, excluded_dirs: tuple[str, ...]) -> bool:
    parts = rel_path.split("/")[:-1]
    return any(part in excluded_dirs for part in parts)


def tag_filename(tag: str) -> str:
    return f"{tag.replace(':', '__')}.jsonl"


def jsonl(entries: list[dict[str, object]]) -> str:
    if not entries:
        return ""
    return "\n".join(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries) + "\n"


def write_index_files(index_dir: Path, files: dict[str, str]) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    tags_dir = index_dir / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)

    for stale_file in tags_dir.glob("*.jsonl"):
        stale_file.unlink()

    for relative_path, content in files.items():
        path = index_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def read_index_files(index_dir: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for relative_path in ["all-docs.jsonl", "manifest.json"]:
        path = index_dir / relative_path
        if path.exists():
            files[relative_path] = path.read_text(encoding="utf-8")

    tags_dir = index_dir / "tags"
    if tags_dir.exists():
        for path in sorted(tags_dir.glob("*.jsonl")):
            files[f"tags/{path.name}"] = path.read_text(encoding="utf-8")

    return files


def read_jsonl_entries(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def tag_count(files: dict[str, str]) -> int:
    return sum(1 for path in files if path.startswith("tags/"))


def print_invalid(errors: list[str]) -> None:
    for error in errors[:20]:
        print(f"INVALID: {error}", file=sys.stderr)
    if len(errors) > 20:
        print(f"INVALID: ... {len(errors) - 20} more", file=sys.stderr)
