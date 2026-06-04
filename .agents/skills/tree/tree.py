#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Iterable


LOCAL_DEP_DIR_NAMES = (".vendor", ".deps", "vendor")


def bootstrap_local_dependency_paths() -> list[Path]:
    script_dir = Path(__file__).resolve().parent
    added: list[Path] = []
    for dep_dir_name in LOCAL_DEP_DIR_NAMES:
        dep_dir = script_dir / dep_dir_name
        if dep_dir.is_dir():
            dep_dir_str = str(dep_dir)
            if dep_dir_str not in sys.path:
                sys.path.insert(0, dep_dir_str)
                added.append(dep_dir)
    return added


LOCAL_DEP_PATHS = bootstrap_local_dependency_paths()

try:
    import pathspec  # type: ignore
except Exception:
    pathspec = None


DEFAULT_IGNORES = [
    ".git/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    ".svelte-kit/",
    ".idea/",
    ".vscode/",
    ".pytest_cache/",
    ".mypy_cache/",
]

README_ENCODINGS = ("utf-8-sig", "utf-8", "cp949")
MAX_README_BYTES = 512 * 1024


@dataclass
class TreeNode:
    name: str
    path: str
    type: str
    readme_title: str | None = None
    lines: int | None = None
    size: int | None = None
    num_files: int = 0
    num_dirs: int = 0
    error: str | None = None
    children: list["TreeNode"] = field(default_factory=list)


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def find_repo_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        git_marker = candidate / ".git"
        if git_marker.exists():
            return candidate
    return None


def iter_ancestor_chain(start: Path, stop: Path | None) -> list[Path]:
    chain: list[Path] = []
    current = start.resolve()
    while True:
        chain.append(current)
        if stop is not None and current == stop:
            break
        parent = current.parent
        if parent == current:
            break
        current = parent
    chain.reverse()
    return chain


def parse_gitignore_lines(raw_text: str) -> list[str]:
    patterns: list[str] = []
    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def read_text_with_fallbacks(path: Path, encodings: Iterable[str]) -> str | None:
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeError, OSError):
            continue
    return None


def count_file_lines_and_size(path: Path) -> tuple[int | None, int | None, str | None]:
    try:
        size = path.stat().st_size
    except OSError:
        return None, None, "[error] OSError"

    if size > 5 * 1024 * 1024:
        return None, size, "[🚨BIG_FILE]"

    for encoding in README_ENCODINGS:
        try:
            with path.open("r", encoding=encoding, errors="strict") as handle:
                lines = sum(1 for _ in handle)
                return lines, size, None
        except (UnicodeError, OSError):
            continue
    return None, size, None


def load_gitignore_patterns(root: Path) -> list[str]:
    repo_root = find_repo_root(root)
    if repo_root is not None and is_relative_to(root, repo_root):
        search_dirs = iter_ancestor_chain(root, repo_root)
    else:
        search_dirs = iter_ancestor_chain(root, None)

    patterns: list[str] = []
    for directory in search_dirs:
        ignore_path = directory / ".gitignore"
        if not ignore_path.is_file():
            continue
        content = read_text_with_fallbacks(ignore_path, README_ENCODINGS)
        if content is None:
            continue
        patterns.extend(parse_gitignore_lines(content))
    return patterns


class IgnoreMatcher:
    def __init__(self, root: Path, patterns: Iterable[str]):
        self.root = root.resolve()
        self.patterns = [p for p in patterns if p]
        self._spec = None
        if pathspec is not None:
            try:
                self._spec = pathspec.PathSpec.from_lines("gitwildmatch", self.patterns)
            except Exception:
                self._spec = None

    def matches(self, candidate: Path, is_dir: bool) -> bool:
        try:
            rel_path = candidate.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return False

        if rel_path in ("", "."):
            return False

        if self._spec is not None:
            if self._spec.match_file(rel_path):
                return True
            if is_dir and self._spec.match_file(f"{rel_path}/"):
                return True
            return False

        return self._matches_fallback(rel_path, is_dir)

    def _matches_fallback(self, rel_path: str, is_dir: bool) -> bool:
        ignored = False
        for raw_pattern in self.patterns:
            negated = raw_pattern.startswith("!")
            pattern = raw_pattern[1:] if negated else raw_pattern
            if not pattern:
                continue

            dir_only = pattern.endswith("/")
            if dir_only:
                pattern = pattern[:-1]
            if dir_only and not is_dir:
                continue

            anchored = pattern.startswith("/")
            if anchored:
                pattern = pattern[1:]
            if not pattern:
                continue

            if self._single_pattern_match(rel_path, pattern, anchored):
                ignored = not negated
        return ignored

    @staticmethod
    def _single_pattern_match(rel_path: str, pattern: str, anchored: bool) -> bool:
        parts = rel_path.split("/")
        if anchored:
            return fnmatchcase(rel_path, pattern)

        if "/" in pattern:
            suffixes = ("/".join(parts[i:]) for i in range(len(parts)))
            return any(fnmatchcase(suffix, pattern) for suffix in suffixes)

        return any(fnmatchcase(part, pattern) for part in parts)


def is_hidden(entry: os.DirEntry[str]) -> bool:
    if entry.name.startswith("."):
        return True
    if os.name != "nt":
        return False
    try:
        attrs = entry.stat(follow_symlinks=False).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attrs & 0x2)


def extract_yaml_frontmatter_name(lines: list[str]) -> tuple[str | None, int]:
    if not lines or lines[0].strip() != "---":
        return None, 0

    name: str | None = None
    saw_frontmatter_key = False
    for index, line in enumerate(lines[1:], start=1):
        text = line.strip()
        if text == "---":
            return name, index + 1 if saw_frontmatter_key else 0

        key, separator, value = text.partition(":")
        if separator and key.strip():
            saw_frontmatter_key = True
        if separator and key.strip() == "name":
            name = value.strip()
            if len(name) >= 2 and name[0] == name[-1] and name[0] in ("'", '"'):
                name = name[1:-1].strip()
            name = name or None

    return None, 0


def extract_readme_h1(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_README_BYTES:
            return None
    except OSError:
        return None

    for encoding in README_ENCODINGS:
        try:
            with path.open("r", encoding=encoding, errors="strict") as handle:
                lines = []
                for index, line in enumerate(handle):
                    if index > 300:
                        break
                    lines.append(line)

                frontmatter_name, start_index = extract_yaml_frontmatter_name(lines)
                if frontmatter_name:
                    return frontmatter_name

                for line in lines[start_index:]:
                    text = line.strip()
                    if text.startswith("# "):
                        title = text[2:].strip()
                        return title or None
                return None
        except (UnicodeError, OSError):
            continue
    return None


def make_output_path(path: Path, root: Path, absolute_paths: bool) -> str:
    if absolute_paths:
        return path.resolve().as_posix()
    return path.resolve().relative_to(root.resolve()).as_posix() or "."


def build_tree(
    root: Path,
    *,
    include_files: bool,
    max_depth: int,
    show_hidden: bool,
    matcher: IgnoreMatcher,
    readme_title_enabled: bool,
    absolute_paths: bool,
) -> TreeNode:
    resolved_root = root.resolve()
    root_name = resolved_root.name or str(resolved_root)
    root_node = TreeNode(
        name=root_name,
        path=make_output_path(resolved_root, resolved_root, absolute_paths),
        type="dir",
    )
    if readme_title_enabled:
        root_readme = resolved_root / "README.md"
        if root_readme.is_file():
            root_node.readme_title = extract_readme_h1(root_readme)

    def walk(current_dir: Path, parent: TreeNode, depth: int) -> None:
        try:
            with os.scandir(current_dir) as scan_it:
                raw_entries = list(scan_it)
        except PermissionError:
            if max_depth < 0 or depth < max_depth:
                parent.children.append(
                    TreeNode(
                        name="[error] PermissionError",
                        path=make_output_path(current_dir, resolved_root, absolute_paths),
                        type="file",
                    )
                )
            return
        except OSError as exc:
            if max_depth < 0 or depth < max_depth:
                parent.children.append(
                    TreeNode(
                        name=f"[error] {exc.__class__.__name__}",
                        path=make_output_path(current_dir, resolved_root, absolute_paths),
                        type="file",
                    )
                )
            return

        entries: list[tuple[os.DirEntry[str], bool]] = []
        for entry in raw_entries:
            if not show_hidden and is_hidden(entry):
                continue

            entry_path = Path(entry.path)
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError:
                is_dir = False

            if matcher.matches(entry_path, is_dir):
                continue

            entries.append((entry, is_dir))

        entries.sort(key=lambda item: (0 if item[1] else 1, item[0].name.lower(), item[0].name))

        for entry, is_dir in entries:
            entry_path = Path(entry.path)
            if is_dir:
                parent.num_dirs += 1
                should_add_dir = (max_depth < 0 or depth < max_depth)
                node = TreeNode(
                    name=entry.name,
                    path=make_output_path(entry_path, resolved_root, absolute_paths),
                    type="dir",
                )

                if should_add_dir:
                    if readme_title_enabled:
                        readme_path = entry_path / "README.md"
                        if readme_path.is_file():
                            node.readme_title = extract_readme_h1(readme_path)
                    parent.children.append(node)

                walk(entry_path, node, depth + 1)
                parent.num_dirs += node.num_dirs
                parent.num_files += node.num_files
            else:
                parent.num_files += 1
                should_add_file = include_files and (max_depth < 0 or depth < max_depth)
                if should_add_file:
                    node = TreeNode(
                        name=entry.name,
                        path=make_output_path(entry_path, resolved_root, absolute_paths),
                        type="file",
                    )

                    if readme_title_enabled and entry_path.suffix.lower() == ".md":
                        node.readme_title = extract_readme_h1(entry_path)

                    lines, size, error = count_file_lines_and_size(entry_path)
                    node.lines = lines
                    node.size = size
                    node.error = error
                    parent.children.append(node)

    walk(resolved_root, root_node, depth=0)
    return root_node


def stream_supports_utf8() -> bool:
    encoding = (sys.stdout.encoding or "").lower()
    return "utf" in encoding


def format_tree_text(root: TreeNode, *, use_unicode: bool, absolute_paths: bool = False) -> str:
    branch_mid = "├── " if use_unicode else "|-- "
    branch_last = "└── " if use_unicode else "`-- "
    extension_mid = "│   " if use_unicode else "|   "
    extension_last = "    "
    readme_separator = " # "
    def node_label(node: TreeNode) -> str:
        label = node.path if absolute_paths else node.name
        if node.type == "dir":
            label += f"/ [{node.num_dirs} dirs, {node.num_files} files]"
        else:
            if node.error == "[🚨BIG_FILE]":
                size_mb = (node.size or 0) / (1024 * 1024)
                label += f" {node.error} [{size_mb:.1f}MB]"
            elif node.error:
                label += f" {node.error}"
            elif node.lines is not None:
                label += f" [{node.lines} lines]"
            else:
                # Binary files or others without text lines
                pass

        if node.readme_title:
            label += f"{readme_separator}{node.readme_title}"
        return label

    root_label = node_label(root)
    lines: list[str] = [root_label]

    def render_children(nodes: list[TreeNode], prefix: str) -> None:
        for idx, node in enumerate(nodes):
            is_last = idx == len(nodes) - 1
            branch = branch_last if is_last else branch_mid
            label = node_label(node)
            lines.append(f"{prefix}{branch}{label}")
            if node.type == "dir":
                extension = extension_last if is_last else extension_mid
                render_children(node.children, prefix + extension)

    render_children(root.children, "")
    return "\n".join(lines)


def to_jsonable(root: TreeNode) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": root.name,
        "path": root.path,
        "type": root.type,
        "children": [to_jsonable(child) for child in root.children],
    }
    if root.readme_title:
        payload["readme_title"] = root.readme_title
    if root.type == "dir":
        payload["num_dirs"] = root.num_dirs
        payload["num_files"] = root.num_files
    else:
        if root.lines is not None:
            payload["lines"] = root.lines
        if root.size is not None:
            payload["size"] = root.size
        if root.error is not None:
            payload["error"] = root.error
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-platform DNL tree generator with .gitignore/README/JSON support."
    )
    parser.add_argument("path", nargs="?", default=None, help="(optional) root path alias")
    parser.add_argument("--root", default=".", help="root directory (default: current directory)")
    parser.add_argument("--files", action="store_true", help="include files in output")
    parser.add_argument("--depth", type=int, default=5, help="max depth (default: 5, -1 for unlimited)")
    parser.add_argument("--hidden", action="store_true", help="include hidden files/directories")
    parser.add_argument("--ignore", action="append", default=[], help="additional ignore pattern (repeatable)")
    parser.add_argument("--no-gitignore", action="store_true", help="disable .gitignore based excludes")
    parser.add_argument("--no-readme-title", action="store_true", help="disable README.md H1 extraction")
    parser.add_argument("--json", action="store_true", help="print as JSON")
    parser.add_argument("--ascii", action="store_true", help="force ASCII tree characters")
    parser.add_argument("--absolute-path", action="store_true", help="emit absolute paths")
    parser.add_argument("--out", default="", help="output file path (UTF-8)")

    args = parser.parse_args(argv)
    if args.path and args.root == ".":
        args.root = args.path
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser()
    if not root.exists():
        print(f"[error] root path does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"[error] root path is not a directory: {root}", file=sys.stderr)
        return 2

    patterns = list(DEFAULT_IGNORES)
    if not args.no_gitignore:
        patterns.extend(load_gitignore_patterns(root))
    patterns.extend(args.ignore or [])

    if not args.no_gitignore and pathspec is None:
        print(
            "[warn] pathspec not installed; running fallback matcher. "
            "Install local deps: python -m pip install --target .agents/skills/tree/.vendor "
            "-r .agents/skills/tree/requirements.txt",
            file=sys.stderr,
        )

    matcher = IgnoreMatcher(root=root, patterns=patterns)
    tree = build_tree(
        root,
        include_files=args.files,
        max_depth=args.depth,
        show_hidden=args.hidden,
        matcher=matcher,
        readme_title_enabled=not args.no_readme_title,
        absolute_paths=args.absolute_path,
    )

    if args.json:
        output = json.dumps(to_jsonable(tree), ensure_ascii=False, indent=2)
    else:
        use_unicode = stream_supports_utf8() and not args.ascii
        output = format_tree_text(tree, use_unicode=use_unicode, absolute_paths=args.absolute_path)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
