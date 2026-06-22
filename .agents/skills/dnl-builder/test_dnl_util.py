from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DnlUtilTagAddTest(unittest.TestCase):
    def run_util(
        self,
        root: Path,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        script = Path(__file__).resolve().parent / "dnl_util.py"
        return subprocess.run(
            [sys.executable, str(script), "--root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def write_doc(self, root: Path, relative_path: str, tags: str = "[]") -> Path:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"""---
name: "Sample"
status: "draft"
tags: {tags}
paths: {{}}
---

# Sample
""",
            encoding="utf-8",
        )
        return path

    def write_scan_config(self, root: Path, include: tuple[str, ...] = ("docs",)) -> None:
        include_block = ", ".join(f'"{item}"' for item in include)
        (root / "dnl-config.toml").write_text(
            f"""
[scan]
include = [{include_block}]
exclude = []
""".strip(),
            encoding="utf-8",
        )

    def test_tag_add_dry_run_reports_change_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/doc.md")

            completed = self.run_util(
                root,
                "tag",
                "add",
                "--dir",
                "docs/sample-dnl",
                "--tag",
                "sample-module",
                "--recursive",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("mode=dry-run", completed.stdout)
            self.assertIn("would_change=1", completed.stdout)
            self.assertIn("tags: []", doc.read_text(encoding="utf-8"))

    def test_tag_add_write_appends_tag_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/doc.md")

            first = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                "docs/sample-dnl",
                "--tag",
                "sample-module",
                "--recursive",
                "--write",
            )
            second = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                "docs/sample-dnl",
                "--tag",
                "sample-module",
                "--recursive",
                "--write",
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn('tags: ["sample-module"]', doc.read_text(encoding="utf-8"))
            self.assertIn("changed=1", first.stdout)
            self.assertIn("already_tagged=1", second.stdout)
            self.assertIn("changed=0", second.stdout)

    def test_tag_add_preserves_readme_portal_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/README.md", '["portal-dnl"]')

            completed = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                "docs/sample-dnl",
                "--tag",
                "sample-module",
                "--recursive",
                "--write",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn(
                'tags: ["portal-dnl", "sample-module"]',
                doc.read_text(encoding="utf-8"),
            )

    def test_tag_add_rejects_invalid_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/doc.md")

            completed = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                "docs/sample-dnl",
                "--tag",
                "EML",
                "--recursive",
                "--write",
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid tag", completed.stderr)

    def test_tag_add_skips_hidden_skill_and_reports_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            editable = self.write_doc(root, "docs/sample-dnl/doc.md")
            hidden = self.write_doc(root, "docs/sample-dnl/.hidden/doc.md")
            hidden_skill_readme = self.write_doc(root, ".agents/skills/sample/README.md")
            skill = self.write_doc(root, ".agents/skills/sample/SKILL.md")
            report = self.write_doc(root, ".agents/skills/dnl-builder/reports/qa-report.md")

            completed = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                ".",
                "--tag",
                "sample-module",
                "--recursive",
                "--write",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('tags: ["sample-module"]', editable.read_text(encoding="utf-8"))
            self.assertIn("tags: []", hidden.read_text(encoding="utf-8"))
            self.assertIn("tags: []", hidden_skill_readme.read_text(encoding="utf-8"))
            self.assertIn("tags: []", skill.read_text(encoding="utf-8"))
            self.assertIn("tags: []", report.read_text(encoding="utf-8"))

    def test_tag_add_reads_scan_include_from_dnl_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dnl-config.toml").write_text(
                """
[scan]
include = ["docs"]
exclude = []
""".strip(),
                encoding="utf-8",
            )
            configured = self.write_doc(root, "docs/doc.md")
            default_scope = self.write_doc(root, "example-company/doc.md")

            completed = self.run_util(
                root,
                "tag",
                "add",
                "--path",
                ".",
                "--tag",
                "sample-module",
                "--recursive",
                "--write",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('tags: ["sample-module"]', configured.read_text(encoding="utf-8"))
            self.assertIn("tags: []", default_scope.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
