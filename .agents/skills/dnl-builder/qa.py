#!/usr/bin/env python3
"""DNL QA / Lint utility.

Goals (low-friction):
- Detect forbidden HUMAN_LINKS sections / HUMAN_LINK lines
- Detect forbidden local markdown file/folder links
- Detect deep relative links (../../ etc.)
- Detect portal docs missing a PATH block
- Detect broken local links (best-effort)

Reports are written to a markdown file (default: .agents/skills/dnl-builder/reports/qa-report.md).
The CLI always prints a short status summary to stdout.
Use --json-summary when a machine-readable summary is needed.

Usage:
  python3 .agents/skills/dnl-builder/qa.py
  python3 .agents/skills/dnl-builder/qa.py --root . --report .agents/skills/dnl-builder/reports/qa-report.md
  python3 .agents/skills/dnl-builder/qa.py --fail-on all
  python3 .agents/skills/dnl-builder/qa.py --json-summary
  python3 .agents/skills/dnl-builder/qa.py --include docs DNL-system --exclude .git node_modules
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import urllib.parse
from dataclasses import dataclass
from typing import Iterable, List, Optional

from dnl_config import (
    DEFAULT_SCAN_EXCLUDE,
    DEFAULT_SCAN_INCLUDE,
    DnlConfigError,
    is_dnl_search_target,
    load_dnl_config,
    required_tags_for_path,
)
from yaml_header import parse_dnl_header


HUMAN_LINK_SECTION = re.compile(r"^\s*##\s+HUMAN_LINKS\b")
HUMAN_LINK_LINE = re.compile(r"^\s*-\s*\[HUMAN_LINK\](?:\s|$)")
PATH_LINE = re.compile(r"^\s*-\s*\[PATH\]\s*")

# Treat these missing targets as UNVERIFIED (they are commonly gitignored).
GITIGNORED_LIKE = {
    "PATHS.md",
    "CURRENT_USER.md",
    "CURRENT_USER",
}

# Markdown link (non-image) basic matcher. We keep it conservative.
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN = re.compile(r"`[^`]*`")
TOKEN_LINK = re.compile(r"^(?:\[@[^\]]+\]|@\{[^}]+\}|\{@[^}]+\}|@[A-Za-z0-9_.-]+)(?:/.*)?$")
WINDOWS_ABS_PATH = re.compile(r"^[A-Za-z]:[\\/]")
LINE_ANNOTATION = re.compile(r":L?\d+(?:-\d+)?$", re.IGNORECASE)
LINK_INDEX_MANIFEST = ".agents/skills/dnl-query/link-index/manifest.json"


def now_str() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def is_external(link: str) -> bool:
    link = link.strip()
    return link.startswith("http://") or link.startswith("https://")


def strip_fragment(link: str) -> str:
    # remove #anchor
    if "#" in link:
        return link.split("#", 1)[0]
    return link


def strip_angle(link: str) -> str:
    link = link.strip()
    if link.startswith("<") and link.endswith(">"):
        return link[1:-1].strip()
    return link


def depth_up(path: str) -> int:
    p = path.strip()
    d = 0
    while p.startswith("../"):
        d += 1
        p = p[3:]
    return d


def portal_doc(path: str) -> bool:
    """Heuristic: which README files should be treated as navigation portals."""
    p = path.replace("\\", "/")
    if not p.endswith(".md"):
        return False
    base = os.path.basename(p).lower()
    if base != "readme.md":
        return False

    parts = p.split("/")
    if p == "README.md":
        return False

    if p.startswith("docs/") or p.startswith("DNL-system/"):
        return True

    # Optional sample/example portals outside the main public skeleton.
    return any(part.startswith("sample-") or part.startswith("example-") for part in parts[:-1])


def should_skip_dir(dirpath: str, exclude: set[str]) -> bool:
    parts = dirpath.replace("\\", "/").split("/")
    return any(p in exclude for p in parts if p)


def iter_md_files(root: str, include: List[str], exclude: List[str]) -> Iterable[str]:
    ex = set(exclude)
    for inc in include:
        start = os.path.join(root, inc)
        if not os.path.exists(start):
            continue
        for dirpath, _, files in os.walk(start):
            if should_skip_dir(dirpath, ex):
                continue
            for fn in files:
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


def merge_unique(*groups: Iterable[str]) -> List[str]:
    merged: List[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            if item not in seen:
                merged.append(item)
                seen.add(item)
    return merged


@dataclass
class Finding:
    file: str
    line: int
    kind: str
    sev: str
    msg: str


def read_lines(fp: str) -> List[str]:
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def document_declares_paths(lines: List[str]) -> bool:
    text = "\n".join(lines)
    header = parse_dnl_header(text)
    if header.paths:
        return True

    return any(PATH_LINE.match(line.strip()) for line in lines[:40])


def should_validate_yaml_frontmatter(path: str, scan_include: Iterable[str] | None = None) -> bool:
    normalized = path.replace("\\", "/")
    if not is_dnl_search_target(normalized):
        return False
    parts = normalized.split("/")
    if "reports" in parts:
        return False
    if scan_include is None:
        return any(normalized == source or normalized.startswith(f"{source}/") for source in DEFAULT_SCAN_INCLUDE)
    return any(normalized == source or normalized.startswith(f"{source}/") for source in scan_include)


def yaml_frontmatter_findings(
    path: str,
    lines: List[str],
    scan_include: Iterable[str] | None = None,
    required_tags: Iterable[str] = (),
) -> List[Finding]:
    if not should_validate_yaml_frontmatter(path, scan_include):
        return []

    header = parse_dnl_header("\n".join(lines))
    findings: List[Finding] = []

    for error in header.errors:
        findings.append(Finding(path, 1, "yaml_frontmatter", "HIGH", error))

    if header.name is None:
        findings.append(
            Finding(path, 1, "yaml_frontmatter", "HIGH", "YAML frontmatter missing required name")
        )
    if header.status is None:
        findings.append(
            Finding(path, 1, "yaml_frontmatter", "HIGH", "YAML frontmatter missing required status")
        )
    if not has_tags_field(lines):
        findings.append(
            Finding(path, 1, "yaml_frontmatter", "HIGH", "YAML frontmatter missing required tags")
        )
    for required_tag in required_tags:
        if required_tag not in header.tags:
            filename = os.path.basename(path)
            findings.append(
                Finding(path, 1, "yaml_frontmatter", "HIGH", f"{filename} must include tag: {required_tag}")
            )

    return findings


def has_tags_field(lines: List[str]) -> bool:
    for line in lines[:40]:
        if line.strip().startswith("tags:"):
            return True
    return False


def strip_code_spans(line: str) -> str:
    return CODE_SPAN.sub("", line)


def normalize_link(link: str) -> str:
    return strip_fragment(strip_angle(link.strip()))


def strip_line_annotation(link: str) -> str:
    """Keep writer-facing references like :123-456 but validate file part only."""
    trimmed = link.strip()
    if "#" in trimmed:
        trimmed = strip_fragment(trimmed)

    # common source-range annotation style in design docs
    if ":" in trimmed and LINE_ANNOTATION.search(trimmed):
        return LINE_ANNOTATION.sub("", trimmed)
    return trimmed


def decode_percent_encoded(link: str) -> str:
    return urllib.parse.unquote(link)


def is_token_link(link: str) -> bool:
    return TOKEN_LINK.match(link) is not None


def is_windows_absolute_path(link: str) -> bool:
    return WINDOWS_ABS_PATH.match(link) is not None


def resolve_local_link(file_path: str, link: str) -> Optional[str]:
    link = normalize_link(link)
    link = decode_percent_encoded(link)
    if (
        not link
        or link.startswith("#")
        or is_token_link(link)
        or is_windows_absolute_path(link)
        or link.startswith("mailto:")
        or link.startswith("file:")
    ):
        return None
    if is_external(link):
        return None
    # absolute-like repo root: treat as root-relative
    if link.startswith("/"):
        link = link.lstrip("/")
        return os.path.normpath(os.path.join(os.getcwd(), link))
    # relative to file directory
    base = os.path.dirname(file_path)
    return os.path.normpath(os.path.join(base, link))


def link_exists(resolved: str) -> bool:
    return os.path.exists(resolved)


def is_gitignored_like(link: str) -> bool:
    # heuristic: links that commonly point to gitignored local config
    l = link.strip().strip("<>")
    base = os.path.basename(strip_fragment(l))
    if base in GITIGNORED_LIKE:
        return True
    if base.startswith("CURRENT_USER"):
        return True
    return False


def is_local_doc_link(link: str, resolved: Optional[str]) -> bool:
    normalized = decode_percent_encoded(normalize_link(link))
    if (
        not normalized
        or normalized.startswith("#")
        or is_external(normalized)
        or is_token_link(normalized)
        or is_windows_absolute_path(normalized)
        or normalized.startswith("mailto:")
        or normalized.startswith("file:")
    ):
        return False

    lowered = normalized.lower()
    if lowered.endswith(".md"):
        return True
    if normalized.endswith("/"):
        return True
    if resolved and os.path.isdir(resolved):
        return True
    if resolved and resolved.lower().endswith(".md"):
        return True
    return False


def should_fail(findings: List[Finding], fail_on: str) -> bool:
    if fail_on == "none":
        return False

    fail_map = {
        "low": 0,
        "all": 0,
        "med": 1,
        "high": 2,
    }
    severity_rank = {"LOW": 0, "MED": 1, "HIGH": 2}
    min_fail_level = fail_map[fail_on]
    return any(severity_rank[f.sev] >= min_fail_level for f in findings)


def build_status(findings: List[Finding], fail_on: str) -> str:
    if not findings:
        return "SUCCESS"
    if should_fail(findings, fail_on):
        return "FAIL"
    return "WARN"


def format_text_summary(
    *,
    status: str,
    total_findings: int,
    files_checked: int,
    portal_total: int,
    report_path: str,
    fail_on: str,
    kind_counts: dict[str, int],
    sev_counts: dict[str, int],
) -> str:
    if status == "SUCCESS":
        return (
            f"SUCCESS: no findings. files={files_checked}, "
            f"portal_readmes={portal_total}. report={report_path}"
        )

    kind_part = ", ".join(
        f"{kind}={count}" for kind, count in kind_counts.items()
    )
    sev_part = ", ".join(
        f"{sev}={count}" for sev, count in sev_counts.items()
    )
    return (
        f"{status}: findings={total_findings}. "
        f"types[{kind_part}]. severity[{sev_part}]. "
        f"fail_on={fail_on.upper()}. See {report_path}"
    )


def empty_link_health() -> dict[str, int]:
    return {
        "documents": 0,
        "links": 0,
        "backlinks": 0,
        "unresolvedPaths": 0,
        "unusedPathTokens": 0,
        "missingPathTokens": 0,
        "indexMissing": 0,
        "indexInvalid": 0,
    }


def read_link_health(root: str) -> dict[str, int]:
    health = empty_link_health()
    manifest_path = os.path.join(root, LINK_INDEX_MANIFEST)
    if not os.path.exists(manifest_path):
        health["indexMissing"] = 1
        return health

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError):
        health["indexInvalid"] = 1
        return health

    for key in ["documents", "links", "backlinks", "unresolvedPaths", "unusedPathTokens", "missingPathTokens"]:
        value = manifest.get(key, 0)
        if isinstance(value, int):
            health[key] = value
    return health


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument(
        "--profile",
        default="full",
        choices=["full", "portal", "links", "health"],
        help=(
            "QA preset. "
            "full=repo-wide (default), portal=public portal READMEs and optional sample/example portals, "
            "links=focus on link-related checks, health=link-index report-only summary."
        ),
    )
    ap.add_argument(
        "--include",
        nargs="*",
        default=None,
        help=(
            "Top-level paths to include (relative to root). "
            "If omitted, uses --profile preset."
        ),
    )
    ap.add_argument(
        "--exclude",
        nargs="*",
        default=None,
        help="Directory names to exclude anywhere in the path.",
    )
    ap.add_argument(
        "--fail-on",
        default="all",
        choices=["none", "low", "med", "high", "all"],
        help=(
            "Fail on violations at or above this severity. "
            "low/all=any severity, med=MED+/HIGH, high=HIGH only, none=no fail."
        ),
    )
    ap.add_argument("--report", default=".agents/skills/dnl-builder/reports/qa-report.md")
    ap.add_argument(
        "--json-summary",
        action="store_true",
        help="Print machine-readable JSON summary to stdout instead of text summary.",
    )

    args = ap.parse_args()

    root = os.path.abspath(args.root)
    os.chdir(root)
    try:
        config = load_dnl_config(root)
    except DnlConfigError as exc:
        print(f"ERROR: {exc}")
        return 2

    base_exclude = list(DEFAULT_SCAN_EXCLUDE)
    if args.exclude is None:
        args.exclude = base_exclude

    yaml_scan_include: tuple[str, ...] | None = None

    # profile presets
    if args.include is None:
        if args.profile == "full":
            args.include = list(config.scan_include)
            args.exclude = merge_unique(args.exclude, config.scan_exclude)
            yaml_scan_include = config.scan_include
        elif args.profile == "portal":
            args.include = list(config.profiles["portal"])
            args.exclude = merge_unique(args.exclude, config.scan_exclude)
        elif args.profile == "links":
            args.include = list(config.profiles["links"])
            args.exclude = merge_unique(args.exclude, config.scan_exclude)
        elif args.profile == "health":
            args.include = []
    md_files: List[str] = []
    # include can contain files too
    for inc in args.include:
        p = os.path.join(root, inc)
        if os.path.isfile(p) and p.endswith(".md"):
            md_files.append(p)
        else:
            md_files.extend(iter_md_files(root, [inc], args.exclude))

    md_files = [
        fp
        for fp in sorted(set(md_files))
        if is_dnl_search_target(os.path.relpath(fp, root))
    ]

    findings: List[Finding] = []
    portal_missing = 0
    portal_total = 0
    human_link_sections = 0
    human_link_lines = 0
    local_doc_links = 0
    deep_links = 0
    broken_md_links = 0
    broken_images = 0
    yaml_frontmatter = 0
    link_health = read_link_health(root) if args.profile == "health" else empty_link_health()
    sev_counts = {"LOW": 0, "MED": 0, "HIGH": 0}

    for fp in md_files:
        rel = os.path.relpath(fp, root)
        lines = read_lines(fp)

        yaml_findings = yaml_frontmatter_findings(
            rel,
            lines,
            yaml_scan_include,
            required_tags_for_path(config, rel),
        )
        yaml_frontmatter += len(yaml_findings)
        for finding in yaml_findings:
            sev_counts[finding.sev] += 1
            findings.append(finding)

        # portal PATH block check
        if portal_doc(rel):
            portal_total += 1
            if not document_declares_paths(lines):
                portal_missing += 1
                sev_counts["MED"] += 1
                findings.append(Finding(rel, 1, "portal", "MED", "Portal README missing YAML paths or - [PATH] block in first 40 lines"))

        in_code = False
        for i, line in enumerate(lines, 1):
            s = line.rstrip("\n")
            if s.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            stripped = s.strip()
            if HUMAN_LINK_SECTION.match(stripped):
                human_link_sections += 1
                sev_counts["HIGH"] += 1
                findings.append(
                    Finding(
                        rel,
                        i,
                        "human_link_section",
                        "HIGH",
                        "HUMAN_LINKS section is forbidden; use PATH/@tokens instead.",
                    )
                )

            is_human_link_line = HUMAN_LINK_LINE.match(stripped) is not None
            if is_human_link_line:
                human_link_lines += 1
                sev_counts["HIGH"] += 1
                findings.append(
                    Finding(
                        rel,
                        i,
                        "human_link_line",
                        "HIGH",
                        "HUMAN_LINK line is forbidden; replace it with PATH/@tokens.",
                    )
                )

            # deep relative markdown links in body (non-image)
            sanitized = strip_code_spans(s)
            if "](" in sanitized:
                for m in MD_LINK.finditer(sanitized):
                    if m.start() > 0 and sanitized[m.start() - 1] == "!":
                        continue
                    raw_link = m.group(2).strip()
                    link = strip_line_annotation(raw_link)
                    resolved = resolve_local_link(fp, link)

                    if not is_human_link_line and is_local_doc_link(link, resolved):
                        local_doc_links += 1
                        sev_counts["HIGH"] += 1
                        findings.append(
                            Finding(
                                rel,
                                i,
                                "file_link",
                                "HIGH",
                                f"Local markdown/file link is forbidden in DNL docs: {raw_link}",
                            )
                        )

                    if is_external(link) or link.startswith("#") or link.startswith("mailto:"):
                        continue
                    if depth_up(link) >= 2:
                        deep_links += 1
                        sev_counts["MED"] += 1
                        findings.append(Finding(rel, i, "deep_link", "MED", f"Deep relative link detected: {raw_link}"))

                    if (
                        is_external(link)
                        or link.startswith("#")
                        or is_token_link(link)
                        or is_windows_absolute_path(link)
                        or link.startswith("mailto:")
                        or link.startswith("file:")
                    ):
                        continue
                    if resolved and not link_exists(resolved):
                        broken_md_links += 1
                        sev = "LOW" if is_gitignored_like(link) else "HIGH"
                        msg = f"Broken link: {raw_link}"
                        if sev == "LOW":
                            msg += " (UNVERIFIED: likely gitignored/local-only)"
                        sev_counts[sev] += 1
                        findings.append(Finding(rel, i, "broken_link", sev, msg))

            if "![" in sanitized and "](" in sanitized:
                for m in MD_IMAGE.finditer(sanitized):
                    raw_link = m.group(1).strip()
                    link = strip_line_annotation(raw_link)
                    if (
                        is_external(link)
                        or is_token_link(link)
                        or is_windows_absolute_path(link)
                        or link.startswith("mailto:")
                        or link.startswith("file:")
                    ):
                        continue
                    resolved = resolve_local_link(fp, link)
                    if resolved and not link_exists(resolved):
                        broken_images += 1
                        sev_counts["MED"] += 1
                        findings.append(Finding(rel, i, "broken_image", "MED", f"Broken image link: {raw_link}"))

    report_abs = os.path.abspath(args.report)
    report_dir = os.path.dirname(report_abs)
    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
    report_rel = os.path.relpath(report_abs, root).replace("\\", "/")

    kind_counts = {
        "portal": portal_missing,
        "human_link_section": human_link_sections,
        "human_link_line": human_link_lines,
        "file_link": local_doc_links,
        "deep_link": deep_links,
        "broken_link": broken_md_links,
        "broken_image": broken_images,
        "yaml_frontmatter": yaml_frontmatter,
        "link_unresolved": link_health["unresolvedPaths"],
        "link_unused": link_health["unusedPathTokens"],
        "link_missing_token": link_health["missingPathTokens"],
        "link_index_missing": link_health["indexMissing"],
        "link_index_invalid": link_health["indexInvalid"],
    }
    total_findings = len(findings)
    status = build_status(findings, args.fail_on)
    exit_code = 1 if status == "FAIL" else 0

    # group by file
    by_file: dict[str, List[Finding]] = {}
    for finding in findings:
        by_file.setdefault(finding.file, []).append(finding)

    out: List[str] = []
    out.append("---")
    out.append('name: "DNL QA Report"')
    out.append("paths: {}")
    out.append("---")
    out.append("")
    out.append("# DNL QA Report")
    out.append("")
    out.append(f"- Generated: {now_str()}")
    out.append(f"- Files checked: {len(md_files)}")
    out.append("")
    out.append("## Summary")
    out.append(f"- Status: {status}")
    out.append(f"- Portal READMEs checked: {portal_total}")
    out.append(f"- Portal READMEs missing PATH block: {portal_missing}")
    out.append(f"- Forbidden HUMAN_LINKS sections: {human_link_sections}")
    out.append(f"- Forbidden HUMAN_LINK lines: {human_link_lines}")
    out.append(f"- Forbidden local markdown/file links: {local_doc_links}")
    out.append(f"- Deep relative links (../../+): {deep_links}")
    out.append(f"- Broken local markdown links (best-effort): {broken_md_links}")
    out.append(f"- Broken local image links (best-effort): {broken_images}")
    out.append(f"- YAML frontmatter findings: {yaml_frontmatter}")
    out.append(f"- Link index documents: {link_health['documents']}")
    out.append(f"- Link index links: {link_health['links']}")
    out.append(f"- Link index backlinks: {link_health['backlinks']}")
    out.append(f"- Link unresolved paths: {link_health['unresolvedPaths']}")
    out.append(f"- Link unused path tokens: {link_health['unusedPathTokens']}")
    out.append(f"- Link missing path tokens: {link_health['missingPathTokens']}")
    out.append(f"- Total findings: {total_findings}")
    out.append(f"- Findings by severity: LOW={sev_counts['LOW']}, MED={sev_counts['MED']}, HIGH={sev_counts['HIGH']}")
    out.append(f"- Exit policy: fail on {args.fail_on.upper()}")

    out.append("")
    out.append("## Findings")

    # stable ordering
    for file in sorted(by_file.keys()):
        out.append("")
        out.append(f"### {file}")
        for finding in sorted(by_file[file], key=lambda item: (item.kind, item.line)):
            out.append(f"- [SEV:{finding.sev}] {finding.kind} — line {finding.line} — {finding.msg}")

    with open(report_abs, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    summary = {
        "status": status,
        "report": report_rel,
        "files_checked": len(md_files),
        "portal_readmes_checked": portal_total,
        "findings_total": total_findings,
        "fail_on": args.fail_on,
        "counts_by_kind": kind_counts,
        "counts_by_severity": sev_counts,
        "link_health": link_health,
        "exit_code": exit_code,
    }

    if args.json_summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            format_text_summary(
                status=status,
                total_findings=total_findings,
                files_checked=len(md_files),
                portal_total=portal_total,
                report_path=report_rel,
                fail_on=args.fail_on,
                kind_counts=kind_counts,
                sev_counts=sev_counts,
            )
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
