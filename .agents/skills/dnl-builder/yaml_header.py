from __future__ import annotations

import re
from dataclasses import dataclass


FRONTMATTER_DELIMITER = "---"
LEGACY_PATH_LINE = re.compile(r"^\s*-\s*\[PATH\]\s*`([^`]+)`(?:\s*:\s*(.*?))?\s*$")
QUOTED_MAP_LINE = re.compile(r"^\s+([\"'])(.+?)\1\s*:\s*([\"'])(.*?)\3\s*$")
QUOTED_SCALAR_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*([\"'])(.*?)\2\s*$")
EMPTY_SCALAR_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*$")
FRONTMATTER_KEY_LINE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*\s*:")
INLINE_LIST_ITEM = re.compile(r"\s*([\"'])(.*?)\1\s*(?:,|$)")
QUOTED_LIST_ITEM_LINE = re.compile(r"^\s+-\s+([\"'])(.*?)\1\s*$")
TAG_VALUE = re.compile(r"^[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?$")
VALID_STATUSES = {"active", "draft", "deprecated"}
FRONTMATTER_FIELD_ORDER = ["name", "status", "tags", "description", "paths"]
FRONTMATTER_FIELD_INDEX = {
    field_name: index for index, field_name in enumerate(FRONTMATTER_FIELD_ORDER)
}
TAG_PATTERN_TEXT = r"^[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?$"


@dataclass
class DnlHeader:
    name: str | None
    status: str | None
    tags: list[str]
    description: list[str]
    paths: dict[str, str]
    errors: list[str]


@dataclass
class LegacyPathEntry:
    token: str
    path: str
    line_index: int
    multiline: bool


def extract_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        return None, text

    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_DELIMITER:
            frontmatter = "".join(lines[1:index]).rstrip("\r\n")
            if not is_probable_frontmatter(frontmatter):
                return None, text
            body = "".join(lines[index + 1 :])
            return frontmatter, body

    return None, text


def is_probable_frontmatter(frontmatter: str) -> bool:
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if FRONTMATTER_KEY_LINE.match(stripped):
            return True
    return False


def parse_dnl_header(text: str) -> DnlHeader:
    frontmatter, _ = extract_frontmatter(text)
    if frontmatter is None:
        return DnlHeader(name=None, status=None, tags=[], description=[], paths={}, errors=[])

    name: str | None = None
    status: str | None = None
    tags: list[str] = []
    description: list[str] = []
    paths: dict[str, str] = {}
    errors: list[str] = []
    in_paths = False
    in_description = False
    max_field_index = -1
    field_order_reported = False
    path_values: dict[str, str] = {}

    lines = frontmatter.splitlines()
    for line_no, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        if line.startswith((" ", "\t")):
            if in_description:
                match = QUOTED_LIST_ITEM_LINE.match(line)
                if match:
                    description.append(match.group(2))
                else:
                    errors.append(
                        f"description entry must be a quoted list item on line {line_no}"
                    )
                continue
        else:
            in_description = False

        if in_paths and not line.startswith((" ", "\t")):
            in_paths = False

        if in_paths:
            if stripped.startswith("- "):
                errors.append(
                    f"paths must be a map of quoted token/path pairs; list item found on line {line_no}"
                )
                continue

            match = QUOTED_MAP_LINE.match(line)
            if not match:
                errors.append(
                    f"paths entry must be a quoted map pair on line {line_no}"
                )
                continue

            token = match.group(2)
            path = match.group(4)
            if not token.startswith("@"):
                errors.append(f"paths key must start with @ on line {line_no}: {token}")
            if token in paths:
                errors.append(f"duplicate paths key found on line {line_no}: {token}")
            if path in path_values:
                errors.append(f"duplicate paths value found on line {line_no}: {path}")
            path_values[path] = token
            paths[token] = path
            continue

        key = top_level_key(stripped)
        if key in FRONTMATTER_FIELD_INDEX:
            current_field_index = FRONTMATTER_FIELD_INDEX[key]
            if current_field_index < max_field_index and not field_order_reported:
                errors.append(
                    "frontmatter field order must be name, status, tags, description, paths"
                )
                field_order_reported = True
            max_field_index = max(max_field_index, current_field_index)

        if stripped == "paths: {}":
            continue

        if stripped == "paths:":
            in_paths = True
            continue

        if stripped == "description:":
            in_description = True
            continue

        match = QUOTED_SCALAR_LINE.match(stripped)
        if match and match.group(1) == "name":
            name = match.group(3)
            continue

        if match and match.group(1) == "status":
            status = match.group(3)
            if status not in VALID_STATUSES:
                errors.append(
                    f"status must be one of active, draft, deprecated on line {line_no}"
                )
            continue

        match = EMPTY_SCALAR_LINE.match(stripped)
        if match and match.group(1) == "name":
            name = ""
            continue

        if stripped == "tags: []":
            tags = []
            continue

        if stripped.startswith("tags:"):
            parsed_tags = parse_inline_list(stripped.split(":", 1)[1].strip())
            if parsed_tags is None:
                errors.append(f"tags must be an inline quoted list on line {line_no}")
                continue

            tags = parsed_tags
            seen_tags: set[str] = set()
            for tag in tags:
                if not TAG_VALUE.match(tag):
                    errors.append(
                        f"tag must match {TAG_PATTERN_TEXT} on line {line_no}: {tag}"
                    )
                if tag in seen_tags:
                    errors.append(f"duplicate tag found on line {line_no}: {tag}")
                seen_tags.add(tag)

    return DnlHeader(
        name=name,
        status=status,
        tags=tags,
        description=description,
        paths=paths,
        errors=errors,
    )


def top_level_key(stripped_line: str) -> str | None:
    match = FRONTMATTER_KEY_LINE.match(stripped_line)
    if not match:
        return None
    return stripped_line.split(":", 1)[0]


def parse_inline_list(raw_value: str) -> list[str] | None:
    if raw_value == "[]":
        return []
    if not raw_value.startswith("[") or not raw_value.endswith("]"):
        return None

    content = raw_value[1:-1].strip()
    if not content:
        return []

    values: list[str] = []
    position = 0
    while position < len(content):
        match = INLINE_LIST_ITEM.match(content, position)
        if not match:
            return None
        values.append(match.group(2))
        position = match.end()
    return values


def parse_legacy_path_entries(lines: list[str]) -> list[LegacyPathEntry]:
    entries: list[LegacyPathEntry] = []

    for index, line in enumerate(lines):
        match = LEGACY_PATH_LINE.match(line)
        if not match:
            continue

        token = match.group(1).strip()
        path = (match.group(2) or "").strip()
        entries.append(
            LegacyPathEntry(
                token=token,
                path=path,
                line_index=index,
                multiline=not bool(path),
            )
        )

    return entries
