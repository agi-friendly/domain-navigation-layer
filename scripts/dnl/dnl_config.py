from __future__ import annotations

import fnmatch
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal


CONFIG_FILENAME = "dnl-config.toml"
DEFAULT_NAME = "dnl"
DEFAULT_VERSION = "0.1"
DEFAULT_SCAN_INCLUDE = ("docs", "DNL-system")
DEFAULT_SCAN_EXCLUDE = (".git", "node_modules")
POLICY_EXCLUDED_FILENAMES = ("SKILL.md",)
BUILTIN_INTERNAL_PATHS = {
    "dnl-root": ".",
}
DEFAULT_INTERNAL_PATHS = {
    **BUILTIN_INTERNAL_PATHS,
    "docs": "docs",
    "DNL-system": "DNL-system",
}
DEFAULT_EXTERNAL_PATHS = {}
DEFAULT_PROFILES = {
    "portal": ("docs/index.md", "DNL-system/README.md", "AGENTS.md"),
    "links": (*DEFAULT_SCAN_INCLUDE, "AGENTS.md"),
}
DEFAULT_PORTAL_README_DIRS = (
    "00_start-here",
    "ai",
    "authoring",
    "boundaries",
    "dnl-history",
    "glossary",
    "history",
    "links",
    "maps",
    "rules",
    "runbooks",
    "status",
    "templates",
    "workflow",
)
DEFAULT_REQUIRED_TAGS_BY_FILENAME = {
    "README.md": ("portal-dnl",),
}
DEFAULT_REQUIRED_TAGS_BY_PATH = {
    "DNL-system/authoring/rules/*.md": ("rule-dnl",),
}


PathVariableKind = Literal["internal", "external", "unknown"]


class DnlConfigError(ValueError):
    pass


@dataclass(frozen=True)
class ExternalPathRule:
    required: bool
    validate: str


@dataclass(frozen=True)
class DnlConfig:
    root: Path
    name: str
    version: str
    scan_include: tuple[str, ...]
    scan_exclude: tuple[str, ...]
    internal_paths: dict[str, str]
    external_paths: dict[str, ExternalPathRule]
    profiles: dict[str, tuple[str, ...]]
    portal_readme_dirs: tuple[str, ...]
    required_tags_by_filename: dict[str, tuple[str, ...]]
    required_tags_by_path: dict[str, tuple[str, ...]]


def default_dnl_config(root: Path) -> DnlConfig:
    return DnlConfig(
        root=Path(root).resolve(),
        name=DEFAULT_NAME,
        version=DEFAULT_VERSION,
        scan_include=DEFAULT_SCAN_INCLUDE,
        scan_exclude=DEFAULT_SCAN_EXCLUDE,
        internal_paths=_internal_paths(DEFAULT_INTERNAL_PATHS, "paths.internal"),
        external_paths=_parse_external_paths(DEFAULT_EXTERNAL_PATHS, "paths.external"),
        profiles=_profile_rules(DEFAULT_PROFILES, "profiles"),
        portal_readme_dirs=DEFAULT_PORTAL_README_DIRS,
        required_tags_by_filename=dict(DEFAULT_REQUIRED_TAGS_BY_FILENAME),
        required_tags_by_path=dict(DEFAULT_REQUIRED_TAGS_BY_PATH),
    )


def load_dnl_config(root: Path) -> DnlConfig:
    root = Path(root).resolve()
    path = root / CONFIG_FILENAME
    if not path.exists():
        return default_dnl_config(root)

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise DnlConfigError(f"{CONFIG_FILENAME} parse failed: {exc}") from exc

    dnl = _table(data, "dnl", {})
    scan = _table(data, "scan", {})
    paths = _table(data, "paths", {})
    profiles = {**DEFAULT_PROFILES, **_table(data, "profiles", {})}
    portal = _table(data, "portal", {})
    tags = _table(data, "tags", {})

    internal = _table(paths, "internal", DEFAULT_INTERNAL_PATHS)
    external = _table(paths, "external", DEFAULT_EXTERNAL_PATHS)

    return DnlConfig(
        root=root,
        name=_string(dnl, "name", DEFAULT_NAME),
        version=_string(dnl, "version", DEFAULT_VERSION),
        scan_include=_string_list(scan, "include", DEFAULT_SCAN_INCLUDE),
        scan_exclude=_string_list(scan, "exclude", DEFAULT_SCAN_EXCLUDE),
        internal_paths=_internal_paths(internal, "paths.internal"),
        external_paths=_parse_external_paths(external, "paths.external"),
        profiles=_profile_rules(profiles, "profiles"),
        portal_readme_dirs=_string_list(portal, "readme_dirs", DEFAULT_PORTAL_README_DIRS),
        required_tags_by_filename=_tag_rules(
            _table(tags, "required_by_filename", DEFAULT_REQUIRED_TAGS_BY_FILENAME),
            "tags.required_by_filename",
        ),
        required_tags_by_path=_tag_rules(
            _table(tags, "required_by_path", DEFAULT_REQUIRED_TAGS_BY_PATH),
            "tags.required_by_path",
        ),
    )


def required_tags_for_path(config: DnlConfig, rel_path: str) -> tuple[str, ...]:
    normalized = rel_path.replace("\\", "/")
    filename = normalized.rsplit("/", 1)[-1]
    tags: list[str] = []

    tags.extend(config.required_tags_by_filename.get(filename, ()))
    for pattern, pattern_tags in config.required_tags_by_path.items():
        if fnmatch.fnmatch(normalized, pattern):
            tags.extend(pattern_tags)

    return tuple(dict.fromkeys(tags))


def classify_path_variable(config: DnlConfig, name: str) -> PathVariableKind:
    if name in config.internal_paths:
        return "internal"
    if name in config.external_paths:
        return "external"
    return "unknown"


def is_dnl_search_target(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/").removeprefix("./")
    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return False
    if parts[-1] in POLICY_EXCLUDED_FILENAMES:
        return False
    return not any(part.startswith(".") for part in parts[:-1])


def _table(source: dict[str, Any], key: str, default: Any) -> dict[str, Any]:
    value = source.get(key, default)
    if not isinstance(value, dict):
        raise DnlConfigError(f"{key} must be a table")
    return value


def _string(source: dict[str, Any], key: str, default: str) -> str:
    value = source.get(key, default)
    if not isinstance(value, str):
        raise DnlConfigError(f"{key} must be a string")
    return value


def _string_list(source: dict[str, Any], key: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = source.get(key, default)
    if not isinstance(value, list | tuple) or not all(isinstance(item, str) for item in value):
        raise DnlConfigError(f"{key} must be a list of strings")
    return tuple(value)


def _string_map(source: dict[str, Any], label: str) -> dict[str, str]:
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in source.items()):
        raise DnlConfigError(f"{label} must be a string map")
    return dict(source)


def _internal_paths(source: dict[str, Any], label: str) -> dict[str, str]:
    paths = _string_map(source, label)
    return {**paths, **BUILTIN_INTERNAL_PATHS}


def _tag_rules(source: dict[str, Any], label: str) -> dict[str, tuple[str, ...]]:
    rules: dict[str, tuple[str, ...]] = {}
    for key, value in source.items():
        if not isinstance(key, str):
            raise DnlConfigError(f"{label} keys must be strings")
        if not isinstance(value, list | tuple) or not all(isinstance(item, str) for item in value):
            raise DnlConfigError(f"{label}.{key} must be a list of strings")
        rules[key] = tuple(value)
    return rules


def _profile_rules(source: dict[str, Any], label: str) -> dict[str, tuple[str, ...]]:
    rules: dict[str, tuple[str, ...]] = {}
    for key, value in source.items():
        if not isinstance(key, str):
            raise DnlConfigError(f"{label} keys must be strings")
        if not isinstance(value, list | tuple) or not all(isinstance(item, str) for item in value):
            raise DnlConfigError(f"{label}.{key} must be a list of strings")
        rules[key] = tuple(value)
    return rules


def _parse_external_paths(source: dict[str, Any], label: str) -> dict[str, ExternalPathRule]:
    rules: dict[str, ExternalPathRule] = {}
    for key, value in source.items():
        if not isinstance(key, str):
            raise DnlConfigError(f"{label} keys must be strings")
        if not isinstance(value, dict):
            raise DnlConfigError(f"{label}.{key} must be a table")
        required = value.get("required", False)
        validate = value.get("validate", "if-defined")
        if not isinstance(required, bool):
            raise DnlConfigError(f"{label}.{key}.required must be a boolean")
        if not isinstance(validate, str):
            raise DnlConfigError(f"{label}.{key}.validate must be a string")
        rules[key] = ExternalPathRule(required=required, validate=validate)
    return rules
