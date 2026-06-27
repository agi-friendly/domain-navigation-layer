from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from qa import document_declares_paths, portal_doc, should_validate_yaml_frontmatter


class DnlQaYamlTest(unittest.TestCase):
    def run_qa(
        self,
        files: dict[str, str],
        include: str | None = "docs",
        profile: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        qa_script = Path(__file__).resolve().parent / "qa.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative_path, content in files.items():
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            if include is not None and "dnl-config.toml" not in files:
                (root / "dnl-config.toml").write_text(
                    f"""
[scan]
include = ["{include}"]
exclude = []
""".strip(),
                    encoding="utf-8",
                )

            command = [
                sys.executable,
                str(qa_script),
                "--root",
                str(root),
                "--report",
                "qa-report.md",
                "--json-summary",
            ]
            if profile is not None:
                command.extend(["--profile", profile])

            return subprocess.run(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

    def test_document_declares_paths_with_yaml_paths(self) -> None:
        lines = [
            "---",
            'name: "Workflow"',
            "paths:",
            '  "@workflow-root.md": "{@DNL-system}/workflow/README.md"',
            "---",
            "",
            "# Workflow",
        ]

        self.assertTrue(document_declares_paths(lines))

    def test_document_declares_paths_with_legacy_path(self) -> None:
        lines = [
            "- [PATH] `@workflow-root.md` : {@DNL-system}/workflow/README.md",
            "---",
            "",
            "# Workflow",
        ]

        self.assertTrue(document_declares_paths(lines))

    def test_document_without_yaml_or_legacy_paths_is_false(self) -> None:
        lines = [
            "---",
            'name: "Workflow"',
            "---",
            "",
            "# Workflow",
        ]

        self.assertFalse(document_declares_paths(lines))

    def test_qa_fails_when_required_status_and_tags_are_missing(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/doc.md": """---
name: "Workflow"
paths: {}
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_fails_when_required_name_is_missing(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/doc.md": """---
status: "draft"
tags: []
paths: {}
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_fails_when_status_is_not_allowed(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/doc.md": """---
name: "Workflow"
status: "review"
tags: []
paths: {}
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_fails_when_tags_are_invalid_or_duplicated(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/doc.md": """---
name: "Workflow"
status: "draft"
tags: ["Portal-DNL", "bad tag", "portal-dnl", "portal-dnl"]
paths: {}
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_fails_when_readme_is_missing_portal_tag(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/README.md": """---
name: "DNL Portal"
status: "draft"
tags: []
paths:
  "@doc.md": "{@dnl-root}/docs/sample-dnl/doc.md"
---

# DNL Portal
""",
                "docs/sample-dnl/doc.md": """---
name: "Workflow"
status: "draft"
tags: []
paths: {}
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_uses_config_required_tags_by_filename(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[scan]
include = ["docs"]
exclude = []

[tags.required_by_filename]
""",
                "docs/sample-dnl/README.md": """---
name: "DNL Portal"
status: "draft"
tags: []
paths:
  "@doc.md": "{@dnl-root}/docs/sample-dnl/doc.md"
---

# DNL Portal
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_uses_config_required_tags_by_path(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[scan]
include = ["docs"]
exclude = []

[tags.required_by_filename]

[tags.required_by_path]
"docs/rules/*.md" = ["rule-dnl"]
""",
                "docs/rules/path.md": """---
name: "Path Rule"
status: "draft"
tags: []
paths: {}
---

# Path Rule
""",
            },
            include=None,
            profile="full",
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 1)

    def test_qa_fails_when_paths_key_does_not_start_with_at(self) -> None:
        completed = self.run_qa(
            {
                "docs/sample-dnl/doc.md": """---
name: "Workflow"
status: "draft"
tags: []
paths:
  "workflow-root.md": "{@DNL-system}/workflow/README.md"
---

# Workflow
""",
            }
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "FAIL")
        self.assertGreater(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_qa_ignores_generated_reports_directory_for_yaml_frontmatter(self) -> None:
        completed = self.run_qa(
            {
                ".agents/skills/dnl-builder/reports/qa-report.md": """---
name: "DNL QA Report"
paths: {}
---

# DNL QA Report
""",
            },
            include=".agents",
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_dot_directories_and_skill_files_are_not_yaml_scope(self) -> None:
        self.assertFalse(should_validate_yaml_frontmatter(".agents/skills/dnl-builder/README.md"))
        self.assertFalse(should_validate_yaml_frontmatter(".agents/skills/dnl-builder/SKILL.md"))
        self.assertFalse(should_validate_yaml_frontmatter(".agents/skills/dnl-builder/reports/qa-report.md"))
        self.assertFalse(should_validate_yaml_frontmatter("docs/sample-dnl/.scratch/README.md"))
        self.assertFalse(should_validate_yaml_frontmatter("DNL-system/authoring/SKILL.md"))

    def test_sample_readmes_are_generic_portal_docs(self) -> None:
        self.assertTrue(
            portal_doc(
                "docs/sample-dnl/sample-product/sample-project/README.md",
                ["docs/sample-dnl/sample-product/sample-project"],
            )
        )

    def test_qa_skips_hidden_agents_skill_markdown(self) -> None:
        completed = self.run_qa(
            {
                ".agents/skills/sample/README.md": """---
name: "Sample Skill Portal"
status: "draft"
paths: {}
---

# Sample Skill Portal
""",
            },
            include=".agents",
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_full_profile_reads_scan_include_from_dnl_config(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[scan]
include = ["docs"]
exclude = []
""",
                "example-company/doc.md": """---
name: "Ignored"
status: "draft"
tags: []
paths: {}
---

# Ignored
""",
                "docs/doc.md": """---
name: "Configured"
paths: {}
---

# Configured
""",
            },
            include=None,
            profile="full",
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["files_checked"], 1)
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 2)

    def test_full_profile_reads_scan_exclude_from_dnl_config(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[scan]
include = ["docs"]
exclude = ["archive"]
""",
                "docs/live/doc.md": """---
name: "Live"
status: "draft"
tags: []
paths: {}
---

# Live
""",
                "docs/archive/doc.md": """---
name: "Archived"
paths: {}
---

# Archived
""",
            },
            include=None,
            profile="full",
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(summary["files_checked"], 1)
        self.assertEqual(summary["counts_by_kind"]["yaml_frontmatter"], 0)

    def test_portal_profile_reads_include_from_dnl_config(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[profiles]
portal = ["docs/README.md"]
""",
                "example-company/README.md": """---
name: "Ignored"
paths: {}
---

# Ignored
""",
                "docs/README.md": """---
name: "Configured Portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@doc.md": "{@dnl-root}/docs/doc.md"
---

# Configured Portal
""",
            },
            include=None,
            profile="portal",
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(summary["files_checked"], 1)
        self.assertEqual(summary["status"], "SUCCESS")

    def test_portal_profile_uses_configured_directories_for_portal_readmes(self) -> None:
        completed = self.run_qa(
            {
                "dnl-config.toml": """[profiles]
portal = ["DNL-shared", "sample-products/README.md", "sample-products/sample-product/projects/example-app"]

[portal]
readme_dirs = ["maps"]
""",
                "DNL-shared/README.md": """---
name: "Shared"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@maps.md": "{@dnl-root}/DNL-shared/maps/README.md"
---

# Shared
""",
                "DNL-shared/maps/README.md": """---
name: "Maps"
status: "draft"
tags: ["portal-dnl"]
---

# Maps
""",
                "sample-products/README.md": """---
name: "Sample Products"
status: "draft"
tags: ["portal-dnl"]
---

# Sample Products
""",
                "sample-products/sample-product/projects/example-app/README.md": """---
name: "Example App"
status: "draft"
tags: ["portal-dnl"]
---

# Example App
""",
                "sample-products/sample-product/projects/other-app/README.md": """---
name: "Other App"
status: "draft"
tags: ["portal-dnl"]
---

# Other App
""",
            },
            include=None,
            profile="portal",
        )

        summary = json.loads(completed.stdout)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(summary["files_checked"], 4)
        self.assertEqual(summary["portal_readmes_checked"], 4)
        self.assertEqual(summary["counts_by_kind"]["portal"], 3)

    def test_health_profile_reports_link_index_counts_without_findings(self) -> None:
        completed = self.run_qa(
            {
                ".agents/skills/dnl-query/link-index/manifest.json": json.dumps(
                    {
                        "schemaVersion": 1,
                        "sources": ["docs", "DNL-system", "docs/sample-dnl"],
                        "documents": 3,
                        "links": 7,
                        "backlinks": 2,
                        "unresolvedPaths": 1,
                        "unusedPathTokens": 4,
                        "missingPathTokens": 2,
                    }
                ),
            },
            include=None,
            profile="health",
        )

        summary = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["findings_total"], 0)
        self.assertEqual(summary["counts_by_kind"]["link_unresolved"], 1)
        self.assertEqual(summary["counts_by_kind"]["link_unused"], 4)
        self.assertEqual(summary["counts_by_kind"]["link_missing_token"], 2)


if __name__ == "__main__":
    unittest.main()
