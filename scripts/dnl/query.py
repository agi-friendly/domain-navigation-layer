#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_TAG_INDEX_DIR = ".agents/skills/dnl-query/tag-index"
DEFAULT_LINK_INDEX_DIR = ".agents/skills/dnl-query/link-index"
TAG_INDEX_BUILD_COMMAND = "python3 .agents/skills/dnl-builder/dnl_util.py tag index build"
LINK_INDEX_BUILD_COMMAND = "python3 .agents/skills/dnl-builder/dnl_util.py link index build"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        root = resolve_root(args.root)
        return args.func(args, root)
    except BrokenPipeError:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
        return 0
    except QueryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="query.py",
        description="Read the generated DNL query index.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the current git worktree root.",
    )
    parser.add_argument(
        "--index",
        default=None,
        help="Index directory override. Defaults to the command-specific tag/link index.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    tags_parser = subparsers.add_parser("tags", help="List tags from the DNL query index.")
    tags_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    tags_parser.set_defaults(func=run_tags)

    docs_parser = subparsers.add_parser("docs", help="Find documents from the DNL query index.")
    docs_parser.add_argument("--tag", action="append", default=[], help="Require a tag. Can be repeated.")
    docs_parser.add_argument("--status", action="append", default=[], help="Allow a status. Can be repeated.")
    docs_parser.add_argument("--under", action="append", default=[], help="Restrict to a path prefix. Can be repeated.")
    docs_parser.add_argument("--name", default=None, help="Case-insensitive name substring.")
    docs_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    docs_parser.set_defaults(func=run_docs)

    links_parser = subparsers.add_parser("links", help="List outbound links for one source document.")
    links_parser.add_argument("--path", required=True, help="Source document path.")
    links_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    links_parser.set_defaults(func=run_links)

    backlinks_parser = subparsers.add_parser("backlinks", help="List inbound links for one target document.")
    backlinks_parser.add_argument("--path", required=True, help="Target document path.")
    backlinks_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    backlinks_parser.set_defaults(func=run_backlinks)

    deps_parser = subparsers.add_parser("deps", help="Print outbound links and backlinks for one document.")
    deps_parser.add_argument("--path", required=True, help="Document path.")
    deps_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    deps_parser.set_defaults(func=run_deps)

    unresolved_parser = subparsers.add_parser("unresolved", help="List unresolved internal link targets.")
    unresolved_parser.add_argument(
        "--under",
        action="append",
        default=[],
        help="Restrict to a source path prefix. Can be repeated.",
    )
    unresolved_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    unresolved_parser.set_defaults(func=run_unresolved)

    unresolved_summary_parser = subparsers.add_parser(
        "unresolved-summary",
        help="Group unresolved internal link targets by source directory.",
    )
    unresolved_summary_parser.add_argument(
        "--under",
        action="append",
        default=[],
        help="Restrict to a source path prefix. Can be repeated.",
    )
    unresolved_summary_parser.add_argument(
        "--depth",
        type=int,
        default=4,
        help="Number of path parts to keep for the source directory group. Defaults to 4.",
    )
    unresolved_summary_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    unresolved_summary_parser.set_defaults(func=run_unresolved_summary)

    unused_parser = subparsers.add_parser("unused", help="List declared path tokens unused in document bodies.")
    unused_parser.add_argument(
        "--under",
        action="append",
        default=[],
        help="Restrict to a source path prefix. Can be repeated.",
    )
    unused_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    unused_parser.set_defaults(func=run_unused)

    missing_tokens_parser = subparsers.add_parser(
        "missing-tokens",
        help="List path-like body tokens missing from YAML paths.",
    )
    missing_tokens_parser.add_argument(
        "--under",
        action="append",
        default=[],
        help="Restrict to a source path prefix. Can be repeated.",
    )
    missing_tokens_parser.add_argument(
        "--format",
        choices=("text", "paths", "jsonl", "json"),
        default="text",
        help="Output format.",
    )
    missing_tokens_parser.set_defaults(func=run_missing_tokens)
    return parser


def run_tags(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_TAG_INDEX_DIR)
    manifest = read_manifest(index_dir, TAG_INDEX_BUILD_COMMAND)
    rows = tag_rows(manifest)

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    for row in rows:
        print(f"{row['tag']} {row['count']}")
    return 0


def run_docs(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_TAG_INDEX_DIR)
    entries = entries_for_query(index_dir, required_tags=args.tag)
    entries = filter_entries(
        entries,
        required_tags=args.tag,
        statuses=args.status,
        under_prefixes=args.under,
        name=args.name,
    )
    entries.sort(key=lambda entry: str(entry["path"]))
    print_entries(entries, args.format)
    return 0


def run_links(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    source_path = normalize_path(args.path)
    entries = outbound_link_rows(index_dir, source_path)
    print_link_entries(entries, args.format, path_field="targetPath")
    return 0


def run_backlinks(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    target_path = normalize_path(args.path)
    rows = backlink_rows(index_dir, target_path)
    print_link_entries(rows, args.format, path_field="source")
    return 0


def run_deps(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    document_path = normalize_path(args.path)
    outbound_links = outbound_link_rows(index_dir, document_path)
    backlinks = backlink_rows(index_dir, document_path)
    plan = dependency_plan(document_path, outbound_links, backlinks)

    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    counts = plan["counts"]
    print(
        f"{plan['path']} | "
        f"outbound={counts['outboundLinks']} "
        f"backlinks={counts['backlinks']} "
        f"unresolved_outbound={counts['unresolvedOutboundLinks']}"
    )
    return 0


def run_unresolved(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    entries = unresolved_entries(index_dir, args.under)
    entries.sort(key=lambda entry: (str(entry.get("source", "")), str(entry.get("token", ""))))
    print_link_entries(entries, args.format, path_field="targetPath")
    return 0


def run_unresolved_summary(args: argparse.Namespace, root: Path) -> int:
    if args.depth < 1:
        raise QueryError("--depth must be 1 or greater")

    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    entries = unresolved_entries(index_dir, args.under)
    rows = summarize_by_source_dir(entries, depth=args.depth)
    print_summary_rows(rows, args.format)
    return 0


def run_unused(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    entries = source_filtered_entries(index_dir / "unused-paths.jsonl", args.under)
    entries.sort(key=lambda entry: (str(entry.get("source", "")), str(entry.get("token", ""))))
    print_link_entries(entries, args.format, path_field="targetPath")
    return 0


def run_missing_tokens(args: argparse.Namespace, root: Path) -> int:
    index_dir = resolve_index_dir(root, args.index, DEFAULT_LINK_INDEX_DIR)
    entries = source_filtered_entries(index_dir / "missing-path-tokens.jsonl", args.under)
    entries.sort(key=lambda entry: (str(entry.get("source", "")), str(entry.get("token", ""))))
    print_missing_token_entries(entries, args.format)
    return 0


def unresolved_entries(index_dir: Path, under_prefixes: list[str]) -> list[dict[str, object]]:
    return source_filtered_entries(index_dir / "unresolved-paths.jsonl", under_prefixes)


def outbound_link_rows(index_dir: Path, source_path: str) -> list[dict[str, object]]:
    rows = [
        entry
        for entry in read_jsonl_entries(index_dir / "all-links.jsonl", LINK_INDEX_BUILD_COMMAND)
        if normalize_path(str(entry.get("source", ""))) == source_path
    ]
    rows.sort(key=lambda entry: str(entry.get("token", "")))
    return rows


def backlink_rows(index_dir: Path, target_path: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for entry in read_jsonl_entries(index_dir / "backlinks.jsonl", LINK_INDEX_BUILD_COMMAND):
        entry_target = normalize_path(str(entry.get("targetPath", "")))
        if entry_target != target_path:
            continue
        for source in entry.get("sources", []):
            if not isinstance(source, dict):
                continue
            rows.append(
                {
                    "targetPath": str(entry.get("targetPath", "")),
                    "source": str(source.get("source", "")),
                    "token": str(source.get("token", "")),
                }
            )
    rows.sort(key=lambda entry: (str(entry.get("source", "")), str(entry.get("token", ""))))
    return rows


def dependency_plan(
    document_path: str,
    outbound_links: list[dict[str, object]],
    backlinks: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "path": document_path,
        "counts": {
            "outboundLinks": len(outbound_links),
            "backlinks": len(backlinks),
            "unresolvedOutboundLinks": sum(
                1 for link in outbound_links if link.get("unresolvedReason")
            ),
        },
        "outboundLinks": outbound_links,
        "backlinks": backlinks,
    }


def source_filtered_entries(path: Path, under_prefixes: list[str]) -> list[dict[str, object]]:
    entries = read_jsonl_entries(path, LINK_INDEX_BUILD_COMMAND)
    normalized_prefixes = [normalize_prefix(prefix) for prefix in under_prefixes]
    if not normalized_prefixes:
        return entries
    return [
        entry
        for entry in entries
        if any(is_under(str(entry.get("source", "")), prefix) for prefix in normalized_prefixes)
    ]


def entries_for_query(index_dir: Path, *, required_tags: list[str]) -> list[dict[str, object]]:
    if len(required_tags) == 1:
        manifest = read_manifest(index_dir, TAG_INDEX_BUILD_COMMAND)
        tag_info = manifest.get("tags", {}).get(required_tags[0])
        if tag_info is None:
            return []
        tag_file = tag_info.get("file")
        if not isinstance(tag_file, str):
            raise QueryError(f"invalid tag file in manifest for tag: {required_tags[0]}")
        return read_jsonl_entries(index_dir / tag_file, TAG_INDEX_BUILD_COMMAND)

    return read_jsonl_entries(index_dir / "all-docs.jsonl", TAG_INDEX_BUILD_COMMAND)


def filter_entries(
    entries: Iterable[dict[str, object]],
    *,
    required_tags: list[str],
    statuses: list[str],
    under_prefixes: list[str],
    name: str | None,
) -> list[dict[str, object]]:
    normalized_prefixes = [normalize_prefix(prefix) for prefix in under_prefixes]
    lowered_name = name.casefold() if name else None
    result: list[dict[str, object]] = []

    for entry in entries:
        entry_tags = {str(tag) for tag in entry.get("tags", [])}
        if any(tag not in entry_tags for tag in required_tags):
            continue
        if statuses and str(entry.get("status", "")) not in statuses:
            continue
        path = str(entry.get("path", ""))
        if normalized_prefixes and not any(is_under(path, prefix) for prefix in normalized_prefixes):
            continue
        entry_name = str(entry.get("name", ""))
        if lowered_name and lowered_name not in entry_name.casefold():
            continue
        result.append(entry)

    return result


def print_entries(entries: list[dict[str, object]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return

    if output_format == "jsonl":
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False, separators=(",", ":")))
        return

    if output_format == "paths":
        for entry in entries:
            print(entry.get("path", ""))
        return

    for entry in entries:
        print(f"{entry.get('path', '')} | {entry.get('status', '')} | {entry.get('name', '')}")


def print_link_entries(entries: list[dict[str, object]], output_format: str, *, path_field: str) -> None:
    if output_format == "json":
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return

    if output_format == "jsonl":
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False, separators=(",", ":")))
        return

    if output_format == "paths":
        for entry in entries:
            print(entry.get(path_field, ""))
        return

    for entry in entries:
        print(format_link_text(entry))


def print_missing_token_entries(entries: list[dict[str, object]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return

    if output_format == "jsonl":
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False, separators=(",", ":")))
        return

    if output_format == "paths":
        for entry in entries:
            print(entry.get("source", ""))
        return

    for entry in entries:
        print(f"{entry.get('source', '')} | {entry.get('token', '')} | count={entry.get('count', 0)}")


def print_summary_rows(rows: list[dict[str, object]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    if output_format == "jsonl":
        for row in rows:
            print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
        return

    if output_format == "paths":
        for row in rows:
            print(row.get("group", ""))
        return

    for row in rows:
        print(f"{row.get('group', '')} | unresolved={row.get('unresolved', 0)} | sources={row.get('sources', 0)}")


def format_link_text(entry: dict[str, object]) -> str:
    source = str(entry.get("source", ""))
    token = str(entry.get("token", ""))
    target = str(entry.get("targetPath") or entry.get("target") or "")
    reason = entry.get("unresolvedReason")
    line = f"{source} | {token} -> {target}"
    if reason:
        line = f"{line} | {reason}"
    return line


def summarize_by_source_dir(entries: Iterable[dict[str, object]], *, depth: int) -> list[dict[str, object]]:
    groups: dict[str, dict[str, object]] = {}
    for entry in entries:
        source = normalize_path(str(entry.get("source", "")))
        group = source_dir_group(source, depth=depth)
        row = groups.setdefault(group, {"group": group, "unresolved": 0, "sources": set()})
        row["unresolved"] = int(row["unresolved"]) + 1
        sources = row["sources"]
        if isinstance(sources, set):
            sources.add(source)

    rows: list[dict[str, object]] = []
    for row in groups.values():
        sources = row["sources"]
        rows.append(
            {
                "group": row["group"],
                "unresolved": row["unresolved"],
                "sources": len(sources) if isinstance(sources, set) else 0,
            }
        )

    rows.sort(key=lambda row: (-int(row["unresolved"]), str(row["group"])))
    return rows


def source_dir_group(source_path: str, *, depth: int) -> str:
    path = normalize_path(source_path)
    parent = path.rsplit("/", 1)[0] if "/" in path else path
    parts = [part for part in parent.split("/") if part]
    if not parts:
        return "."
    return "/".join(parts[:depth])


def tag_rows(manifest: dict[str, object]) -> list[dict[str, object]]:
    tags = manifest.get("tags", {})
    if not isinstance(tags, dict):
        raise QueryError("invalid manifest: tags must be an object")

    rows: list[dict[str, object]] = []
    for tag, info in tags.items():
        if not isinstance(info, dict):
            raise QueryError(f"invalid manifest tag entry: {tag}")
        count = info.get("count")
        if not isinstance(count, int):
            raise QueryError(f"invalid manifest tag count: {tag}")
        rows.append({"tag": str(tag), "count": count})

    rows.sort(key=lambda row: (-int(row["count"]), str(row["tag"])))
    return rows


def read_manifest(index_dir: Path, build_command: str) -> dict[str, object]:
    manifest_path = index_dir / "manifest.json"
    ensure_index_file(manifest_path, build_command)
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise QueryError(f"invalid DNL query index manifest: {manifest_path}") from exc


def read_jsonl_entries(path: Path, build_command: str) -> list[dict[str, object]]:
    ensure_index_file(path, build_command)
    entries: list[dict[str, object]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                entries.append(json.loads(line))
    except json.JSONDecodeError as exc:
        raise QueryError(f"invalid DNL query index jsonl: {path}") from exc
    return entries


def ensure_index_file(path: Path, build_command: str) -> None:
    if path.exists():
        return
    rel_path = path.as_posix()
    raise QueryError(
        f"DNL query index not found: {rel_path}\n"
        f"Run: {build_command}"
    )


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
        root = Path(completed.stdout.strip()).resolve() if completed.returncode == 0 else Path.cwd().resolve()

    if not root.exists() or not root.is_dir():
        raise QueryError(f"root does not exist or is not a directory: {root}")
    return root


def resolve_index_dir(root: Path, raw_index: str | None, default_index: str) -> Path:
    index_dir = Path(raw_index or default_index).expanduser()
    if not index_dir.is_absolute():
        index_dir = root / index_dir
    return index_dir.resolve()


def normalize_path(raw_path: str) -> str:
    return raw_path.strip().replace("\\", "/").strip("/")


def normalize_prefix(raw_prefix: str) -> str:
    prefix = raw_prefix.strip().replace("\\", "/").strip("/")
    return prefix


def is_under(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


class QueryError(Exception):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
