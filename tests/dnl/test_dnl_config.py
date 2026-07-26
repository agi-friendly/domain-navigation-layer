from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DNL = REPO_ROOT / "scripts" / "dnl"
sys.path.insert(0, str(SCRIPTS_DNL))

from dnl_config import (
    DnlConfigError,
    classify_path_variable,
    default_dnl_config,
    is_dnl_search_target,
    load_dnl_config,
    required_tags_for_path,
)


class DnlConfigTest(unittest.TestCase):
    def test_default_config_matches_current_scan_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            config = default_dnl_config(root)

            self.assertEqual(config.name, "dnl")
            self.assertEqual(config.scan_include, ("docs", "DNL-system"))
            self.assertIn("node_modules", config.scan_exclude)
            self.assertNotIn("CURRENT_WORKING", config.scan_exclude)
            self.assertEqual(config.internal_paths["dnl-root"], ".")
            self.assertEqual(config.internal_paths["docs"], "docs")
            self.assertEqual(config.internal_paths["DNL-system"], "DNL-system")
            self.assertEqual(classify_path_variable(config, "dnl-root"), "internal")
            self.assertEqual(classify_path_variable(config, "docs"), "internal")
            self.assertEqual(classify_path_variable(config, "DNL-system"), "internal")
            self.assertEqual(classify_path_variable(config, "unknown"), "unknown")
            self.assertEqual(config.profiles["portal"], ("docs/index.md", "DNL-system/README.md", "AGENTS.md"))
            self.assertEqual(config.profiles["links"], ("docs", "DNL-system", "AGENTS.md"))
            self.assertIn("maps", config.portal_readme_dirs)
            self.assertIn("workflow", config.portal_readme_dirs)
            self.assertEqual(required_tags_for_path(config, "docs/README.md"), ("portal-dnl",))
            self.assertEqual(required_tags_for_path(config, "DNL-system/authoring/rules/path.md"), ("rule-dnl",))

    def test_dnl_search_policy_excludes_dot_dirs_and_skill_files(self) -> None:
        self.assertTrue(is_dnl_search_target("docs/README.md"))
        self.assertTrue(is_dnl_search_target("DNL-system/README.md"))
        self.assertTrue(is_dnl_search_target("docs/sample-dnl/sample-product/README.md"))
        self.assertFalse(is_dnl_search_target("docs/.scratch/doc.md"))
        self.assertFalse(is_dnl_search_target(".agents/skills/dnl-builder/README.md"))
        self.assertFalse(is_dnl_search_target("DNL-system/authoring/SKILL.md"))

    def test_load_config_reads_project_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dnl-config.toml").write_text(
                """
[dnl]
version = "0.1"
name = "custom-dnl"

[scan]
include = ["docs"]
exclude = ["tmp"]

[paths.internal]
Docs = "docs"

[paths.external]
Project = { required = true, validate = "if-defined" }

[profiles]
portal = ["docs/README.md"]

[portal]
readme_dirs = ["maps"]

[tags.required_by_filename]
"README.md" = ["portal-dnl"]

[tags.required_by_path]
"docs/rules/*.md" = ["rule-dnl"]
""".strip(),
                encoding="utf-8",
            )

            config = load_dnl_config(root)

            self.assertEqual(config.name, "custom-dnl")
            self.assertEqual(config.scan_include, ("docs",))
            self.assertEqual(config.scan_exclude, ("tmp",))
            self.assertEqual(config.internal_paths, {"Docs": "docs", "dnl-root": "."})
            self.assertTrue(config.external_paths["Project"].required)
            self.assertEqual(config.profiles["portal"], ("docs/README.md",))
            self.assertEqual(config.portal_readme_dirs, ("maps",))
            self.assertEqual(required_tags_for_path(config, "docs/README.md"), ("portal-dnl",))
            self.assertEqual(required_tags_for_path(config, "docs/rules/path.md"), ("rule-dnl",))

    def test_load_config_rejects_wrong_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dnl-config.toml").write_text(
                """
[scan]
include = "docs"
""".strip(),
                encoding="utf-8",
            )

            with self.assertRaises(DnlConfigError):
                load_dnl_config(root)


if __name__ == "__main__":
    unittest.main()
