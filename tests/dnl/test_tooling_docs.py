from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
KOREAN_TEXT = re.compile(r"[\uac00-\ud7a3]")

PORTABLE_DOCS = [
    REPO_ROOT / ".agents" / "skills" / "README.md",
    REPO_ROOT / ".agents" / "skills" / "dnl-query" / "README.md",
    REPO_ROOT / ".agents" / "skills" / "dnl-query" / "SKILL.md",
    REPO_ROOT / ".agents" / "skills" / "multi-agent-skill-guide.md",
    REPO_ROOT / ".agents" / "skills" / "tree" / "SKILL.md",
    REPO_ROOT / "scripts" / "dnl" / "query.md",
    REPO_ROOT / "scripts" / "dnl" / "tree.md",
]

OFFICIAL_TOOLING_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "docs" / "dnl-config.md",
    REPO_ROOT / "docs" / "getting-started.md",
    REPO_ROOT / "docs" / "how-dnl-works.md",
    REPO_ROOT / "docs" / "repository-layout.md",
    REPO_ROOT / "docs" / "skill-source-migration.md",
    REPO_ROOT / "docs" / "skills.md",
    REPO_ROOT / "DNL-system" / "README.md",
    REPO_ROOT / "DNL-system" / "authoring" / "README.md",
    REPO_ROOT / "DNL-system" / "authoring" / "rules" / "dnl-structure.md",
    REPO_ROOT / ".agents" / "skills" / "README.md",
    REPO_ROOT / ".agents" / "skills" / "dnl-builder" / "README.md",
    REPO_ROOT / ".agents" / "skills" / "dnl-query" / "README.md",
    REPO_ROOT / ".agents" / "skills" / "dnl-query" / "SKILL.md",
    REPO_ROOT / ".agents" / "skills" / "multi-agent-skill-guide.md",
    REPO_ROOT / ".agents" / "skills" / "tree" / "SKILL.md",
    REPO_ROOT / "scripts" / "dnl" / "query.md",
    REPO_ROOT / "scripts" / "dnl" / "tree.md",
]


class PortableToolingDocsTest(unittest.TestCase):
    def test_portable_tooling_docs_are_english(self) -> None:
        for path in PORTABLE_DOCS:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertTrue(path.is_file(), f"missing portable doc: {path}")
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(KOREAN_TEXT.search(text), f"Korean text remains in {path}")

    def test_tree_tool_has_script_side_guide(self) -> None:
        guide = REPO_ROOT / "scripts" / "dnl" / "tree.md"
        text = guide.read_text(encoding="utf-8")

        required_snippets = [
            "scripts/dnl/tree.py",
            "python3 scripts/dnl/tree.py --root docs --depth 3 --files --ascii",
            "--root",
            "--files",
            "--depth",
            "--json",
            "--ascii",
            "pathspec",
            "scripts/dnl/requirements.txt",
        ]
        for snippet in required_snippets:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_tree_skill_is_thin_router_to_script_docs(self) -> None:
        skill = REPO_ROOT / ".agents" / "skills" / "tree" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")

        self.assertIn("scripts/dnl/tree.py", text)
        self.assertIn("scripts/dnl/tree.md", text)
        self.assertIn("compatibility shim", text)
        self.assertLessEqual(len(text.splitlines()), 80)
        self.assertNotIn(".agents/skills/tree/tree.py --root", text)

    def test_query_tool_has_script_side_guide(self) -> None:
        guide = REPO_ROOT / "scripts" / "dnl" / "query.md"
        text = guide.read_text(encoding="utf-8")

        required_snippets = [
            "scripts/dnl/query.py",
            "python3 scripts/dnl/query.py tags",
            "python3 scripts/dnl/query.py docs --tag glossary-dnl --format paths",
            "links",
            "backlinks",
            "deps",
            "unresolved-summary",
            "tag index",
            "link index",
        ]
        for snippet in required_snippets:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_query_skill_is_thin_router_to_script_docs(self) -> None:
        skill = REPO_ROOT / ".agents" / "skills" / "dnl-query" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")

        self.assertIn("scripts/dnl/query.py", text)
        self.assertIn("scripts/dnl/query.md", text)
        self.assertLessEqual(len(text.splitlines()), 90)
        self.assertNotIn(".agents/skills/dnl-query/dnl_query.py tags", text)

    def test_official_examples_use_script_paths(self) -> None:
        forbidden = [
            ".agents/skills/tree/tree.py --",
            ".agents/skills/dnl-query/dnl_query.py tags",
            ".agents/skills/dnl-query/dnl_query.py docs",
            ".agents/skills/dnl-query/dnl_query.py links",
            ".agents/skills/dnl-query/dnl_query.py backlinks",
            ".agents/skills/dnl-query/dnl_query.py unresolved",
            ".agents/skills/dnl-query/dnl_query.py unused",
            ".agents/skills/dnl-query/dnl_query.py missing-tokens",
            "unittest discover -s .agents/skills/dnl-query",
            "unittest discover -s .agents/skills/tree",
        ]
        for path in OFFICIAL_TOOLING_DOCS:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8")
                for snippet in forbidden:
                    self.assertNotIn(snippet, text)

    def test_dnl_structure_lists_official_tooling_surfaces(self) -> None:
        structure = REPO_ROOT / "DNL-system" / "authoring" / "rules" / "dnl-structure.md"
        text = structure.read_text(encoding="utf-8")

        required_snippets = [
            "scripts/dnl",
            "query.py",
            "query.md",
            "tree.py",
            "tree.md",
            "tests/dnl",
            "portable DNL",
            "compatibility shim",
        ]
        for snippet in required_snippets:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_mv_remains_a_builder_maintenance_command(self) -> None:
        builder_skill = (
            REPO_ROOT / ".agents" / "skills" / "dnl-builder" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn(".agents/skills/dnl-builder/dnl_util.py mv", builder_skill)
        self.assertFalse((REPO_ROOT / "scripts" / "dnl" / "mv.py").exists())


if __name__ == "__main__":
    unittest.main()
