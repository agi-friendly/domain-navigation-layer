from __future__ import annotations

import re
import subprocess
import tomllib
import unittest
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
KOREAN_TEXT = re.compile(r"[\uac00-\ud7a3]")


def repo_path(*parts: str) -> str:
    return "/".join(parts)


TREE_LEGACY = repo_path(".agents", "skills", "tree", "tree.py")
QUERY_LEGACY = repo_path(".agents", "skills", "dnl-query", "dnl_query.py")
QA_LEGACY = repo_path(".agents", "skills", "dnl-builder", "qa.py")
UTIL_LEGACY = repo_path(".agents", "skills", "dnl-builder", "dnl_util.py")
LEGACY_PATHS = (TREE_LEGACY, QUERY_LEGACY, QA_LEGACY, UTIL_LEGACY)


@dataclass(frozen=True)
class AllowedLegacyReference:
    file: str
    legacy_path: str
    exact_context: str
    occurrences: int = 1


ALLOWED_LEGACY_REFERENCES = (
    AllowedLegacyReference(
        TREE_LEGACY,
        TREE_LEGACY,
        f'LEGACY_PATH = "{TREE_LEGACY}"',
    ),
    AllowedLegacyReference(
        QUERY_LEGACY,
        QUERY_LEGACY,
        f'LEGACY_PATH = "{QUERY_LEGACY}"',
    ),
    AllowedLegacyReference(
        QA_LEGACY,
        QA_LEGACY,
        f'LEGACY_PATH = "{QA_LEGACY}"',
    ),
    AllowedLegacyReference(
        UTIL_LEGACY,
        UTIL_LEGACY,
        f'LEGACY_PATH = "{UTIL_LEGACY}"',
    ),
    AllowedLegacyReference(
        repo_path(".agents", "skills", "dnl-builder", "README.md"),
        QA_LEGACY,
        (
            f"`{QA_LEGACY}` and\n"
            f"`{UTIL_LEGACY}` are temporary compatibility shims."
        ),
    ),
    AllowedLegacyReference(
        repo_path(".agents", "skills", "dnl-builder", "README.md"),
        UTIL_LEGACY,
        (
            f"`{QA_LEGACY}` and\n"
            f"`{UTIL_LEGACY}` are temporary compatibility shims."
        ),
    ),
    AllowedLegacyReference(
        repo_path("tests", "dnl", "test_compatibility_shims.py"),
        TREE_LEGACY,
        f'("{TREE_LEGACY}", "scripts/dnl/tree.py")',
    ),
    AllowedLegacyReference(
        repo_path("tests", "dnl", "test_compatibility_shims.py"),
        QUERY_LEGACY,
        f'("{QUERY_LEGACY}", "scripts/dnl/query.py")',
    ),
    AllowedLegacyReference(
        repo_path("tests", "dnl", "test_compatibility_shims.py"),
        QA_LEGACY,
        f'("{QA_LEGACY}", "scripts/dnl/qa.py")',
    ),
    AllowedLegacyReference(
        repo_path("tests", "dnl", "test_compatibility_shims.py"),
        UTIL_LEGACY,
        f'("{UTIL_LEGACY}", "scripts/dnl/dnl_util.py")',
    ),
)

PORTABLE_DOCS = (
    REPO_ROOT / ".agents/skills/README.md",
    REPO_ROOT / ".agents/skills/dnl-builder/README.md",
    REPO_ROOT / ".agents/skills/dnl-builder/SKILL.md",
    REPO_ROOT / ".agents/skills/dnl-query/README.md",
    REPO_ROOT / ".agents/skills/dnl-query/SKILL.md",
    REPO_ROOT / ".agents/skills/multi-agent-skill-guide.md",
    REPO_ROOT / ".agents/skills/tree/SKILL.md",
    REPO_ROOT / "scripts/dnl/README.md",
    REPO_ROOT / "scripts/dnl/tree.md",
    REPO_ROOT / "scripts/dnl/query.md",
    REPO_ROOT / "scripts/dnl/qa.md",
    REPO_ROOT / "scripts/dnl/dnl_util.md",
)


class PortableToolingDocsTest(unittest.TestCase):
    def test_portable_tooling_docs_are_english(self) -> None:
        for path in PORTABLE_DOCS:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertTrue(path.is_file(), f"missing portable doc: {path}")
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(
                    KOREAN_TEXT.search(text),
                    f"Korean text remains in {path}",
                )

    def test_tooling_portal_routes_all_four_tools_and_guides(self) -> None:
        portal = (REPO_ROOT / "scripts/dnl/README.md").read_text(encoding="utf-8")

        required = (
            "scripts/dnl/tree.py",
            "scripts/dnl/tree.md",
            "scripts/dnl/query.py",
            "scripts/dnl/query.md",
            "scripts/dnl/qa.py",
            "scripts/dnl/qa.md",
            "scripts/dnl/dnl_util.py",
            "scripts/dnl/dnl_util.md",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertIn(path, portal)

    def test_tree_and_query_skills_are_thin_script_routers(self) -> None:
        cases = (
            ("tree", "scripts/dnl/tree.py", "scripts/dnl/tree.md", 80),
            ("dnl-query", "scripts/dnl/query.py", "scripts/dnl/query.md", 90),
        )
        for skill_name, script, guide, line_limit in cases:
            with self.subTest(skill=skill_name):
                skill_path = REPO_ROOT / ".agents/skills" / skill_name / "SKILL.md"
                text = skill_path.read_text(encoding="utf-8")
                self.assertIn(script, text)
                self.assertIn(guide, text)
                self.assertIn("compatibility shim", text)
                self.assertLessEqual(len(text.splitlines()), line_limit)

    def test_builder_skill_routes_to_canonical_rules_and_script_guides(self) -> None:
        skill = (REPO_ROOT / ".agents/skills/dnl-builder/SKILL.md").read_text(
            encoding="utf-8"
        )

        required = (
            "DNL-system/authoring/README.md",
            "DNL-system/workflow/README.md",
            "scripts/dnl/README.md",
            "scripts/dnl/qa.md",
            "scripts/dnl/dnl_util.md",
            "python3 scripts/dnl/qa.py",
            "python3 scripts/dnl/dnl_util.py",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertIn(path, skill)
        self.assertLessEqual(len(skill.splitlines()), 80)

    def test_query_recovery_routes_to_canonical_maintenance_tool(self) -> None:
        query_source = (REPO_ROOT / "scripts/dnl/query.py").read_text(
            encoding="utf-8"
        )
        query_guide = (REPO_ROOT / "scripts/dnl/query.md").read_text(
            encoding="utf-8"
        )

        for text in (query_source, query_guide):
            self.assertIn("scripts/dnl/dnl_util.py tag index build", text)
            self.assertIn("scripts/dnl/dnl_util.py link index build", text)

    def test_structure_documents_complete_tooling_ownership(self) -> None:
        structure = (
            REPO_ROOT / "DNL-system/authoring/rules/dnl-structure.md"
        ).read_text(encoding="utf-8")

        required = (
            "scripts/dnl/tree.py",
            "scripts/dnl/query.py",
            "scripts/dnl/qa.py",
            "scripts/dnl/dnl_util.py",
            "scripts/dnl/dnl_config.py",
            "scripts/dnl/yaml_header.py",
            "scripts/dnl/dnl_util_core/",
            "tests/dnl/",
            "runtime paths",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertIn(path, structure)
        self.assertFalse((REPO_ROOT / "scripts/dnl/mv.py").exists())

    def test_script_guides_remain_outside_the_dnl_scan(self) -> None:
        config = tomllib.loads(
            (REPO_ROOT / "dnl-config.toml").read_text(encoding="utf-8")
        )
        self.assertNotIn("scripts/dnl", config["scan"]["include"])

    def test_verification_uses_the_canonical_portable_test_suite(self) -> None:
        migration_guide = (
            REPO_ROOT / "docs/skill-source-migration.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "python3 -m unittest discover -s tests/dnl",
            migration_guide,
        )
        self.assertNotIn(
            "unittest discover -s .agents/skills/dnl-builder",
            migration_guide,
        )

    def test_legacy_paths_have_exact_compatibility_contexts_only(self) -> None:
        completed = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

        allowed = {
            (item.file, item.legacy_path): item
            for item in ALLOWED_LEGACY_REFERENCES
        }
        self.assertEqual(len(allowed), len(ALLOWED_LEGACY_REFERENCES))

        observed: set[tuple[str, str]] = set()
        violations: list[str] = []
        for relative_path in filter(None, completed.stdout.split("\0")):
            candidate = REPO_ROOT / relative_path
            if not candidate.is_file():
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for legacy_path in LEGACY_PATHS:
                occurrence_count = text.count(legacy_path)
                if occurrence_count == 0:
                    continue
                item = allowed.get((relative_path, legacy_path))
                if item is None:
                    violations.append(
                        f"unexpected legacy path: {relative_path}: {legacy_path}"
                    )
                    continue
                observed.add((relative_path, legacy_path))
                if occurrence_count != item.occurrences:
                    violations.append(
                        f"unexpected count: {relative_path}: {legacy_path}: "
                        f"expected {item.occurrences}, found {occurrence_count}"
                    )
                if text.count(item.exact_context) != 1:
                    violations.append(
                        f"missing exact context: {relative_path}: {legacy_path}"
                    )

        missing = set(allowed) - observed
        violations.extend(
            f"missing allowed compatibility reference: {path}: {legacy}"
            for path, legacy in sorted(missing)
        )
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
