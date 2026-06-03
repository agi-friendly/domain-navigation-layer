from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from dnl_config import DnlConfig, classify_path_variable, is_dnl_search_target, load_dnl_config
from dnl_util_core.commands.tag_index import (
    gitignored_paths,
    is_in_excluded_dir,
    is_in_scan_sources,
    iter_candidate_markdown,
    jsonl,
    resolve_output_dir,
    resolve_root,
)
from yaml_header import extract_frontmatter, parse_dnl_header


DEFAULT_INDEX_DIR = ".agents/skills/dnl-query/link-index"
SCHEMA_VERSION = 1
VARIABLE_TARGET = re.compile(r"^\{@([^}]+)\}(?:/(.*))?$")
BODY_TOKEN = re.compile(r"(?<![\w.{])@[A-Za-z0-9가-힣_./-]*[A-Za-z0-9가-힣_]")
FENCE_START = re.compile(r"^\s*(```|~~~)")
PATH_TOKEN_EXTENSIONS = {
    ".css",
    ".csv",
    ".docx",
    ".gif",
    ".html",
    ".java",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".jsp",
    ".md",
    ".pdf",
    ".png",
    ".ps1",
    ".py",
    ".scss",
    ".sh",
    ".sql",
    ".svg",
    ".svelte",
    ".toml",
    ".ts",
    ".txt",
    ".webp",
    ".xlsx",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass
class LinkBuild:
    documents: int
    links: list[dict[str, object]]
    backlinks: list[dict[str, object]]
    unresolved_paths: list[dict[str, object]]
    unused_paths: list[dict[str, object]]
    missing_path_tokens: list[dict[str, object]]
    invalid: list[str]
    files: dict[str, str]


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    link_parser = subparsers.add_parser("link", help="Link health utilities.")
    link_subparsers = link_parser.add_subparsers(dest="link_command", required=True)

    index_parser = link_subparsers.add_parser("index", help="Build and check link index files.")
    index_subparsers = index_parser.add_subparsers(dest="index_command", required=True)

    build_parser = index_subparsers.add_parser("build", help="Rebuild the full link index.")
    build_parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_DIR,
        help=f"Index output directory. Defaults to {DEFAULT_INDEX_DIR}.",
    )
    build_parser.set_defaults(func=run_build)

    check_parser = index_subparsers.add_parser("check", help="Check whether the link index is stale.")
    check_parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_DIR,
        help=f"Index output directory. Defaults to {DEFAULT_INDEX_DIR}.",
    )
    check_parser.set_defaults(func=run_check)


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
            "LINK INDEX BUILD: "
            f"documents={build.documents} links=0 invalid={len(build.invalid)} "
            f"output={index_dir.relative_to(root).as_posix()}",
        )
        print_invalid(build.invalid)
        return 1

    write_index_files(index_dir, build.files)
    print(
        "LINK INDEX BUILD: "
        f"documents={build.documents} "
        f"links={len(build.links)} "
        f"unresolved={len(build.unresolved_paths)} "
        f"unused={len(build.unused_paths)} "
        f"missing_tokens={len(build.missing_path_tokens)} "
        f"output={index_dir.relative_to(root).as_posix()}"
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
        print(f"LINK INDEX CHECK: INVALID invalid={len(build.invalid)}")
        print_invalid(build.invalid)
        return 1

    actual_files = read_link_index_files(index_dir)
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
            "LINK INDEX CHECK: STALE "
            f"changed_files={len(changed)} missing_files={len(missing)} extra_files={len(extra)}"
        )
        return 1

    print(
        "LINK INDEX CHECK: OK "
        f"documents={build.documents} links={len(build.links)} "
        f"unresolved={len(build.unresolved_paths)} missing_tokens={len(build.missing_path_tokens)}"
    )
    return 0


def build_current_index(root: Path) -> LinkBuild:
    config = load_dnl_config(root)
    markdown_paths = list(iter_candidate_markdown(root, config.scan_include))
    ignored = gitignored_paths(root, [path.relative_to(root).as_posix() for path in markdown_paths])
    documents = 0
    links: list[dict[str, object]] = []
    unresolved_paths: list[dict[str, object]] = []
    unused_paths: list[dict[str, object]] = []
    missing_path_tokens: list[dict[str, object]] = []
    invalid: list[str] = []

    for path in markdown_paths:
        rel_path = path.relative_to(root).as_posix()
        if rel_path in ignored:
            continue
        if not should_process_markdown(rel_path, config):
            continue

        document_links, document_unused, document_missing, errors = parse_document_links(
            root,
            path,
            config,
        )
        if errors:
            invalid.extend(errors)
            continue

        documents += 1
        links.extend(document_links)
        unresolved_paths.extend(link for link in document_links if link.get("unresolvedReason"))
        unused_paths.extend(document_unused)
        missing_path_tokens.extend(document_missing)

    links.sort(key=lambda entry: (str(entry["source"]), str(entry["token"])))
    unresolved_paths.sort(key=lambda entry: (str(entry["source"]), str(entry["token"])))
    unused_paths.sort(key=lambda entry: (str(entry["source"]), str(entry["token"])))
    missing_path_tokens.sort(key=lambda entry: (str(entry["source"]), str(entry["token"])))
    backlinks = build_backlinks(links)
    files = make_index_files(
        config,
        documents,
        links,
        backlinks,
        unresolved_paths,
        unused_paths,
        missing_path_tokens,
    )
    return LinkBuild(
        documents=documents,
        links=links,
        backlinks=backlinks,
        unresolved_paths=unresolved_paths,
        unused_paths=unused_paths,
        missing_path_tokens=missing_path_tokens,
        invalid=invalid,
        files=files,
    )


def should_process_markdown(rel_path: str, config: DnlConfig) -> bool:
    if not is_dnl_search_target(rel_path):
        return False
    if not is_in_scan_sources(rel_path, config.scan_include):
        return False
    if is_in_excluded_dir(rel_path, config.scan_exclude):
        return False
    return rel_path.endswith(".md")


def parse_document_links(
    root: Path,
    path: Path,
    config: DnlConfig,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[str]]:
    rel_path = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    header = parse_dnl_header(text)
    if header.errors:
        return [], [], [], [f"{rel_path}: {error}" for error in header.errors]

    _, body = extract_frontmatter(text)
    body_tokens = body_token_counts(body)
    declared_tokens = set(header.paths)
    links: list[dict[str, object]] = []
    unused_paths: list[dict[str, object]] = []

    for token, target in header.paths.items():
        resolved = resolve_target(root, config, rel_path, target)
        used = token in body_tokens
        link = {
            "source": rel_path,
            "token": token,
            "target": target,
            "targetKind": resolved["kind"],
            "targetVariable": resolved["variable"],
            "targetPath": resolved["path"],
            "targetExists": resolved["exists"],
            "usedInBody": used,
        }
        if resolved["reason"]:
            link["unresolvedReason"] = resolved["reason"]
        links.append(link)
        if not used:
            unused_paths.append(link)

    missing_path_tokens = [
        {
            "source": rel_path,
            "token": token,
            "count": count,
        }
        for token, count in body_tokens.items()
        if token not in declared_tokens and is_missing_path_token_candidate(token)
    ]

    return links, unused_paths, missing_path_tokens, []


def resolve_target(root: Path, config: DnlConfig, source_rel_path: str, target: str) -> dict[str, object]:
    match = VARIABLE_TARGET.match(target)
    if match:
        variable = match.group(1)
        suffix = match.group(2) or ""
        variable_kind = classify_path_variable(config, variable)
        if variable_kind == "internal":
            rel_path = join_logical_path(config.internal_paths[variable], suffix)
            exists = (root / rel_path).exists()
            return {
                "kind": "internal",
                "variable": variable,
                "path": rel_path,
                "exists": exists,
                "reason": None if exists else "target-not-found",
            }
        if variable_kind == "external":
            return {
                "kind": "external",
                "variable": variable,
                "path": None,
                "exists": None,
                "reason": None,
            }
        return {
            "kind": "unknown",
            "variable": variable,
            "path": None,
            "exists": None,
            "reason": "unknown-variable",
        }

    if target.startswith(("http://", "https://")):
        return {
            "kind": "url",
            "variable": None,
            "path": None,
            "exists": None,
            "reason": None,
        }

    rel_path = resolve_literal_target(source_rel_path, target)
    exists = (root / rel_path).exists()
    return {
        "kind": "literal",
        "variable": None,
        "path": rel_path,
        "exists": exists,
        "reason": None if exists else "target-not-found",
    }


def join_logical_path(base: str, suffix: str) -> str:
    if not suffix:
        return normalize_logical_path(base)
    if base in {"", "."}:
        return normalize_logical_path(suffix)
    return normalize_logical_path(f"{base.rstrip('/')}/{suffix}")


def resolve_literal_target(source_rel_path: str, target: str) -> str:
    if target.startswith("/"):
        return normalize_logical_path(target.removeprefix("/"))
    source_dir = posixpath.dirname(source_rel_path)
    if not source_dir:
        return normalize_logical_path(target)
    return normalize_logical_path(f"{source_dir}/{target}")


def normalize_logical_path(path: str) -> str:
    normalized = posixpath.normpath(path.replace("\\", "/"))
    if normalized == ".":
        return "."
    return normalized.removeprefix("./")


def body_token_counts(body: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in BODY_TOKEN.findall(strip_fenced_code_blocks(body)):
        counts[token] = counts.get(token, 0) + 1
    return counts


def is_missing_path_token_candidate(token: str) -> bool:
    if "/" in token:
        return True
    lower_token = token.lower()
    return any(lower_token.endswith(extension) for extension in PATH_TOKEN_EXTENSIONS)


def strip_fenced_code_blocks(text: str) -> str:
    result: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_START.match(line):
            in_fence = not in_fence
            result.append("")
            continue
        if in_fence:
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def build_backlinks(links: list[dict[str, object]]) -> list[dict[str, object]]:
    backlinks: dict[str, list[dict[str, str]]] = {}
    for link in links:
        if link["targetKind"] != "internal":
            continue
        if not link["targetExists"]:
            continue
        target_path = link["targetPath"]
        if not isinstance(target_path, str) or not target_path.endswith(".md"):
            continue
        backlinks.setdefault(target_path, []).append(
            {
                "source": str(link["source"]),
                "token": str(link["token"]),
            }
        )

    return [
        {
            "targetPath": target_path,
            "sources": sorted(sources, key=lambda entry: (entry["source"], entry["token"])),
        }
        for target_path, sources in sorted(backlinks.items())
    ]


def make_index_files(
    config: DnlConfig,
    documents: int,
    links: list[dict[str, object]],
    backlinks: list[dict[str, object]],
    unresolved_paths: list[dict[str, object]],
    unused_paths: list[dict[str, object]],
    missing_path_tokens: list[dict[str, object]],
) -> dict[str, str]:
    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "sources": list(config.scan_include),
        "documents": documents,
        "links": len(links),
        "backlinks": len(backlinks),
        "unresolvedPaths": len(unresolved_paths),
        "unusedPathTokens": len(unused_paths),
        "missingPathTokens": len(missing_path_tokens),
    }
    return {
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        "all-links.jsonl": jsonl(links),
        "backlinks.jsonl": jsonl(backlinks),
        "unresolved-paths.jsonl": jsonl(unresolved_paths),
        "unused-paths.jsonl": jsonl(unused_paths),
        "missing-path-tokens.jsonl": jsonl(missing_path_tokens),
    }


def write_index_files(index_dir: Path, files: dict[str, str]) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, content in files.items():
        path = index_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def read_link_index_files(index_dir: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    if not index_dir.exists():
        return files
    for path in sorted(index_dir.rglob("*")):
        if path.is_file():
            files[path.relative_to(index_dir).as_posix()] = path.read_text(encoding="utf-8")
    return files


def print_invalid(errors: list[str]) -> None:
    for error in errors[:20]:
        print(f"INVALID: {error}", file=sys.stderr)
    if len(errors) > 20:
        print(f"INVALID: ... {len(errors) - 20} more", file=sys.stderr)
