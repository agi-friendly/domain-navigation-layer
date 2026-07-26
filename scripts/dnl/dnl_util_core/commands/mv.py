from __future__ import annotations

import argparse
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from dnl_config import DnlConfig, classify_path_variable, is_dnl_search_target, load_dnl_config
from dnl_util_core.commands import link, tag_index
from yaml_header import QUOTED_MAP_LINE, extract_frontmatter, parse_dnl_header


TOKEN_PATH = re.compile(r"^\{@([^}]+)\}(?:/(.*))?$")
BODY_MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
INLINE_CODE_SPAN = re.compile(r"`[^`]*`")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FENCE_START = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class MovePlan:
    source_rel: str
    destination_rel: str
    destination_target: str
    backlink_updates: list[dict[str, str]]


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    mv_parser = subparsers.add_parser("mv", help="Move one DNL markdown file and rewrite YAML path backlinks.")
    mv_parser.add_argument("--path", required=True, help="Source markdown file. Use a repo-relative or internal token path.")
    mv_parser.add_argument("--to", required=True, help="Existing destination directory. Rename targets are not supported.")
    mode = mv_parser.add_mutually_exclusive_group()
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
    mv_parser.set_defaults(func=run_mv)


def run_mv(args: argparse.Namespace) -> int:
    try:
        root = tag_index.resolve_root(args.root)
        config = load_dnl_config(root)
        source = resolve_source_file(root, config, args.path)
        destination_dir = resolve_destination_dir(root, config, args.to)
        build = refresh_link_index(root)
        plan = make_move_plan(root, config, build, source, destination_dir)
        changed_texts = planned_backlink_rewrites(root, plan)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    mode = "write" if args.write else "dry-run"
    moved = 0
    if args.write:
        for rel_path, text in changed_texts.items():
            (root / rel_path).write_text(text, encoding="utf-8")
        (root / plan.source_rel).rename(root / plan.destination_rel)
        refresh_link_index(root)
        refresh_tag_index(root)
        moved = 1

    print(format_summary(mode, plan, moved=moved))
    for update in plan.backlink_updates:
        print(
            "UPDATE "
            f"source={update['source']} "
            f"token={update['token']} "
            f"target={update['target']}"
        )
    return 0


def resolve_source_file(root: Path, config: DnlConfig, raw_path: str) -> Path:
    path = resolve_internal_user_path(root, config, raw_path, label="path")
    if not path.exists():
        raise ValueError(f"source file does not exist: {path.relative_to(root).as_posix()}")
    if not path.is_file() or path.suffix != ".md":
        raise ValueError(f"source must be a markdown file: {path.relative_to(root).as_posix()}")

    rel_path = path.relative_to(root).as_posix()
    ensure_dnl_scope(root, config, rel_path, label="source")
    return path


def resolve_destination_dir(root: Path, config: DnlConfig, raw_path: str) -> Path:
    if looks_like_markdown_file(raw_path):
        raise ValueError("rename is not supported; --to must be an existing directory")

    path = resolve_internal_user_path(root, config, raw_path, label="to")
    if not path.exists():
        raise ValueError(f"destination directory does not exist: {path.relative_to(root).as_posix()}")
    if not path.is_dir():
        raise ValueError("rename is not supported; --to must be an existing directory")

    rel_path = path.relative_to(root).as_posix()
    ensure_dnl_scope(root, config, f"{rel_path}/placeholder.md", label="destination")
    return path


def resolve_internal_user_path(root: Path, config: DnlConfig, raw_path: str, *, label: str) -> Path:
    raw_path = raw_path.strip()
    if not raw_path:
        raise ValueError(f"{label} must not be empty")
    if Path(raw_path).expanduser().is_absolute():
        raise ValueError(f"{label} must be repo-relative or an internal token path")

    match = TOKEN_PATH.match(raw_path)
    if match:
        variable = match.group(1)
        suffix = match.group(2) or ""
        if classify_path_variable(config, variable) != "internal":
            raise ValueError(f"{label} token must use [paths.internal]: {variable}")
        ensure_no_parent_traversal(suffix, label=label)
        rel_path = join_logical_path(config.internal_paths[variable], suffix)
    else:
        ensure_no_parent_traversal(raw_path, label=label)
        rel_path = normalize_logical_path(raw_path)

    path = (root / rel_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside root: {raw_path}") from exc
    return path


def ensure_dnl_scope(root: Path, config: DnlConfig, rel_path: str, *, label: str) -> None:
    rel_path = normalize_logical_path(rel_path)
    if not is_dnl_search_target(rel_path):
        raise ValueError(f"{label} is not a DNL markdown target: {rel_path}")
    if not tag_index.is_in_scan_sources(rel_path, config.scan_include):
        raise ValueError(f"{label} is outside configured DNL scan scope: {rel_path}")
    if tag_index.is_in_excluded_dir(rel_path, config.scan_exclude):
        raise ValueError(f"{label} is excluded by DNL config: {rel_path}")
    if rel_path in tag_index.gitignored_paths(root, [rel_path]):
        raise ValueError(f"{label} is gitignored: {rel_path}")


def make_move_plan(
    root: Path,
    config: DnlConfig,
    build: link.LinkBuild,
    source: Path,
    destination_dir: Path,
) -> MovePlan:
    source_rel = source.relative_to(root).as_posix()
    destination_rel = (destination_dir / source.name).relative_to(root).as_posix()
    if source_rel == destination_rel:
        raise ValueError("source is already in the destination directory")
    if (root / destination_rel).exists():
        raise ValueError(f"destination file already exists: {destination_rel}")

    source_links = [entry for entry in build.links if entry.get("source") == source_rel]
    unresolved = [entry for entry in source_links if entry.get("unresolvedReason")]
    if unresolved:
        raise ValueError("source document has unresolved outbound YAML paths")
    literal_links = [entry for entry in source_links if entry.get("targetKind") == "literal"]
    if literal_links:
        raise ValueError("source document has literal YAML paths; convert them to internal token paths first")
    local_body_links = local_markdown_targets(source.read_text(encoding="utf-8"))
    if local_body_links:
        raise ValueError(
            "source document has local markdown links or images; "
            f"move assets/update references manually first: {local_body_links[0]}"
        )

    destination_target = canonical_internal_target(config, destination_rel)
    backlink_updates = [
        {
            "source": source_ref["source"],
            "token": source_ref["token"],
            "target": destination_target,
        }
        for source_ref in backlinks_for(build, source_rel)
    ]
    return MovePlan(
        source_rel=source_rel,
        destination_rel=destination_rel,
        destination_target=destination_target,
        backlink_updates=backlink_updates,
    )


def backlinks_for(build: link.LinkBuild, target_path: str) -> list[dict[str, str]]:
    for entry in build.backlinks:
        if entry.get("targetPath") != target_path:
            continue
        sources = entry.get("sources", [])
        if not isinstance(sources, list):
            return []
        return [
            {
                "source": str(source_ref.get("source", "")),
                "token": str(source_ref.get("token", "")),
            }
            for source_ref in sources
            if isinstance(source_ref, dict)
        ]
    return []


def planned_backlink_rewrites(root: Path, plan: MovePlan) -> dict[str, str]:
    replacements_by_source: dict[str, dict[str, str]] = {}
    for update in plan.backlink_updates:
        replacements_by_source.setdefault(update["source"], {})[update["token"]] = update["target"]

    changed_texts: dict[str, str] = {}
    for rel_path, replacements in replacements_by_source.items():
        path = root / rel_path
        text = path.read_text(encoding="utf-8")
        next_text = rewrite_yaml_path_targets(text, replacements)
        if next_text == text:
            raise ValueError(f"no YAML path target changed in backlink source: {rel_path}")
        changed_texts[rel_path] = next_text
    return changed_texts


def rewrite_yaml_path_targets(text: str, replacements: dict[str, str]) -> str:
    header = parse_dnl_header(text)
    if header.errors:
        raise ValueError(f"backlink source has invalid YAML frontmatter: {header.errors[0]}")

    lines = text.splitlines(keepends=True)
    closing_index = find_frontmatter_end(lines)
    if closing_index is None:
        raise ValueError("backlink source has no YAML frontmatter")

    in_paths = False
    changed_tokens: set[str] = set()
    for index in range(1, closing_index):
        line = lines[index]
        stripped = line.strip()
        if in_paths and not line.startswith((" ", "\t")):
            in_paths = False
        if in_paths:
            match = QUOTED_MAP_LINE.match(line.rstrip("\r\n"))
            if match and match.group(2) in replacements:
                indent = line[: len(line) - len(line.lstrip())]
                key_quote = match.group(1)
                token = match.group(2)
                value_quote = match.group(3)
                lines[index] = (
                    f"{indent}{key_quote}{token}{key_quote}: "
                    f"{value_quote}{replacements[token]}{value_quote}{line_ending(line)}"
                )
                changed_tokens.add(token)
            continue
        if stripped == "paths:":
            in_paths = True

    missing = sorted(set(replacements) - changed_tokens)
    if missing:
        raise ValueError(f"backlink source missing YAML path token: {', '.join(missing)}")
    return "".join(lines)


def local_markdown_targets(text: str) -> list[str]:
    _, body = extract_frontmatter(text)
    targets: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_START.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        line_without_code = INLINE_CODE_SPAN.sub("", line)
        for match in BODY_MARKDOWN_LINK.finditer(line_without_code):
            target = normalize_markdown_target(match.group(1))
            if is_local_markdown_target(target):
                targets.append(target)
    return targets


def normalize_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split(maxsplit=1)[0] if target else ""


def is_local_markdown_target(target: str) -> bool:
    if not target:
        return False
    if target.startswith("#"):
        return False
    if target.startswith("{@"):
        return False
    if URI_SCHEME.match(target):
        return False
    return True


def refresh_link_index(root: Path) -> link.LinkBuild:
    build = link.build_current_index(root)
    if build.invalid:
        raise ValueError(f"link index is invalid: {build.invalid[0]}")
    index_dir = link.resolve_output_dir(root, link.DEFAULT_INDEX_DIR)
    link.write_index_files(index_dir, build.files)
    return build


def refresh_tag_index(root: Path) -> tag_index.IndexBuild:
    build = tag_index.build_current_index(root)
    if build.invalid:
        raise ValueError(f"tag index is invalid: {build.invalid[0]}")
    index_dir = tag_index.resolve_output_dir(root, tag_index.DEFAULT_INDEX_DIR)
    tag_index.write_index_files(index_dir, build.files)
    return build


def canonical_internal_target(config: DnlConfig, rel_path: str) -> str:
    rel_path = normalize_logical_path(rel_path)
    candidates: list[tuple[int, str, str]] = []
    for variable, base in config.internal_paths.items():
        normalized_base = normalize_logical_path(base)
        if normalized_base == ".":
            candidates.append((0, variable, normalized_base))
            continue
        if rel_path == normalized_base or rel_path.startswith(f"{normalized_base}/"):
            candidates.append((len(normalized_base.split("/")), variable, normalized_base))

    if not candidates:
        return f"{{@dnl-root}}/{rel_path}"

    _, variable, base = max(candidates, key=lambda item: (item[0], item[1] != "dnl-root"))
    if base == ".":
        return f"{{@{variable}}}/{rel_path}"
    suffix = rel_path.removeprefix(base).lstrip("/")
    return f"{{@{variable}}}/{suffix}" if suffix else f"{{@{variable}}}"


def ensure_no_parent_traversal(path: str, *, label: str) -> None:
    parts = path.replace("\\", "/").split("/")
    if any(part == ".." for part in parts):
        raise ValueError(f"{label} must not contain parent traversal")


def looks_like_markdown_file(raw_path: str) -> bool:
    return normalize_logical_path(raw_path).lower().endswith(".md")


def join_logical_path(base: str, suffix: str) -> str:
    if not suffix:
        return normalize_logical_path(base)
    if base in {"", "."}:
        return normalize_logical_path(suffix)
    return normalize_logical_path(f"{base.rstrip('/')}/{suffix}")


def normalize_logical_path(path: str) -> str:
    normalized = posixpath.normpath(path.replace("\\", "/").strip())
    if normalized == ".":
        return "."
    return normalized.removeprefix("./").strip("/")


def find_frontmatter_end(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index
    return None


def line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def format_summary(mode: str, plan: MovePlan, *, moved: int) -> str:
    return (
        "DNL MV: "
        f"mode={mode} "
        f"source={plan.source_rel} "
        f"destination={plan.destination_rel} "
        f"backlink_updates={len(plan.backlink_updates)} "
        f"moved={moved}"
    )
