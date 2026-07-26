from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DnlUtilTagIndexTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[2]
    DNL_UTIL_SCRIPT = REPO_ROOT / "scripts" / "dnl" / "dnl_util.py"

    def run_util(
        self,
        root: Path,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.DNL_UTIL_SCRIPT), "--root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def write_doc(
        self,
        root: Path,
        relative_path: str,
        *,
        name: str = "Sample",
        status: str = "draft",
        tags: str = "[]",
        description: str | None = None,
    ) -> Path:
        description_block = ""
        if description is not None:
            description_block = f'description:\n  - "{description}"\n'

        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"""---
name: "{name}"
status: "{status}"
tags: {tags}
{description_block}paths: {{}}
---

# {name}
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

    def read_jsonl(self, path: Path) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_index_build_writes_manifest_all_docs_and_tag_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(
                root,
                "docs/sample-dnl/README.md",
                name="Sample Portal",
                tags='["portal-dnl", "sample-module"]',
                description="This document describes the sample DNL portal.",
            )
            self.write_doc(root, "docs/sample-dnl/doc.md", name="Mail", tags='["sample-module"]')
            self.write_doc(root, "docs/sample-dnl/empty-tags.md", name="No Tag")

            completed = self.run_util(root, "tag", "index", "build")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_docs = self.read_jsonl(index_dir / "all-docs.jsonl")
            eml_docs = self.read_jsonl(index_dir / "tags/sample-module.jsonl")
            portal_docs = self.read_jsonl(index_dir / "tags/portal-dnl.jsonl")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("TAG INDEX BUILD", completed.stdout)
            self.assertEqual(manifest["schemaVersion"], 1)
            self.assertEqual(manifest["documents"], 3)
            self.assertNotIn("generatedBy", manifest)
            self.assertEqual(
                manifest["statusCounts"],
                {"active": 0, "draft": 3, "deprecated": 0},
            )
            self.assertEqual(manifest["untaggedDocuments"], 1)
            self.assertEqual(manifest["tags"]["sample-module"]["count"], 2)
            self.assertEqual(manifest["tags"]["portal-dnl"]["count"], 1)
            self.assertEqual([entry["path"] for entry in all_docs], ["docs/sample-dnl/README.md", "docs/sample-dnl/doc.md", "docs/sample-dnl/empty-tags.md"])
            self.assertEqual([entry["path"] for entry in eml_docs], ["docs/sample-dnl/README.md", "docs/sample-dnl/doc.md"])
            self.assertEqual([entry["path"] for entry in portal_docs], ["docs/sample-dnl/README.md"])
            self.assertEqual(all_docs[0]["description"], ["This document describes the sample DNL portal."])

    def test_index_build_encodes_colon_tag_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/doc.md", tags='["api:mail"]')

            completed = self.run_util(root, "tag", "index", "build")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(manifest["tags"]["api:mail"]["file"], "tags/api__mail.jsonl")
            self.assertTrue((index_dir / "tags/api__mail.jsonl").exists())

    def test_index_build_reads_scan_include_from_dnl_config(self) -> None:
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
            self.write_doc(root, "docs/doc.md", tags='["docs"]')
            self.write_doc(root, "example-company/doc.md", tags='["example"]')

            completed = self.run_util(root, "tag", "index", "build")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_docs = self.read_jsonl(index_dir / "all-docs.jsonl")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(manifest["sources"], ["docs"])
            self.assertEqual(manifest["documents"], 1)
            self.assertIn("docs", manifest["tags"])
            self.assertNotIn("dnl", manifest["tags"])
            self.assertEqual([entry["path"] for entry in all_docs], ["docs/doc.md"])

    def test_index_build_reads_scan_exclude_from_dnl_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dnl-config.toml").write_text(
                """
[scan]
include = ["docs"]
exclude = ["archive"]
""".strip(),
                encoding="utf-8",
            )
            self.write_doc(root, "docs/live/doc.md", tags='["live"]')
            self.write_doc(root, "docs/archive/doc.md", tags='["archive"]')

            completed = self.run_util(root, "tag", "index", "build")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_docs = self.read_jsonl(index_dir / "all-docs.jsonl")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(manifest["documents"], 1)
            self.assertIn("live", manifest["tags"])
            self.assertNotIn("archive", manifest["tags"])
            self.assertEqual([entry["path"] for entry in all_docs], ["docs/live/doc.md"])

    def test_index_update_moves_path_between_tag_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/doc.md", tags='["sample-module"]')
            build = self.run_util(root, "tag", "index", "build")
            self.assertEqual(build.returncode, 0, build.stderr)

            doc.write_text(
                """---
name: "Sample"
status: "draft"
tags: ["org"]
paths: {}
---

# Sample
""",
                encoding="utf-8",
            )

            update = self.run_util(root, "tag", "index", "update", "--path", "docs/sample-dnl/doc.md")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            org_docs = self.read_jsonl(index_dir / "tags/org.jsonl")

            self.assertEqual(update.returncode, 0, update.stderr)
            self.assertIn("action=updated", update.stdout)
            self.assertNotIn("sample-module", manifest["tags"])
            self.assertEqual(manifest["tags"]["org"]["count"], 1)
            self.assertEqual([entry["path"] for entry in org_docs], ["docs/sample-dnl/doc.md"])
            self.assertFalse((index_dir / "tags/sample-module.jsonl").exists())

    def test_index_update_removes_deleted_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/doc.md", tags='["sample-module"]')
            build = self.run_util(root, "tag", "index", "build")
            self.assertEqual(build.returncode, 0, build.stderr)
            doc.unlink()

            update = self.run_util(root, "tag", "index", "update", "--path", "docs/sample-dnl/doc.md")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_docs = self.read_jsonl(index_dir / "all-docs.jsonl")

            self.assertEqual(update.returncode, 0, update.stderr)
            self.assertIn("action=removed", update.stdout)
            self.assertEqual(manifest["documents"], 0)
            self.assertEqual(manifest["tags"], {})
            self.assertEqual(all_docs, [])

    def test_index_check_detects_stale_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            doc = self.write_doc(root, "docs/sample-dnl/doc.md", tags='["sample-module"]')
            build = self.run_util(root, "tag", "index", "build")
            self.assertEqual(build.returncode, 0, build.stderr)

            fresh = self.run_util(root, "tag", "index", "check")
            self.assertEqual(fresh.returncode, 0, fresh.stderr)
            self.assertIn("OK", fresh.stdout)

            doc.write_text(
                """---
name: "Sample"
status: "draft"
tags: ["org"]
paths: {}
---

# Sample
""",
                encoding="utf-8",
            )

            stale = self.run_util(root, "tag", "index", "check")

            self.assertEqual(stale.returncode, 1)
            self.assertIn("STALE", stale.stdout)

    def test_index_build_skips_hidden_skill_reports_and_fails_invalid_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/doc.md", tags='["sample-module"]')
            self.write_doc(root, "docs/sample-dnl/.hidden/doc.md", tags='["hidden"]')
            self.write_doc(root, ".agents/skills/sample/README.md", tags='["skill"]')
            self.write_doc(root, ".agents/skills/sample/SKILL.md", tags='["skill"]')
            self.write_doc(root, ".agents/skills/dnl-builder/reports/qa-report.md", tags='["report"]')
            self.write_doc(root, "docs/sample-dnl/bad.md", tags='["Bad Tag"]')

            completed = self.run_util(root, "tag", "index", "build")

            self.assertEqual(completed.returncode, 1)
            self.assertIn("invalid=1", completed.stdout)

    def test_index_build_skips_hidden_skill_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/doc.md", tags='["sample-module"]')
            self.write_doc(root, ".agents/skills/sample/README.md", tags='["skill"]')

            completed = self.run_util(root, "tag", "index", "build")

            index_dir = root / ".agents/skills/dnl-query/tag-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_docs = self.read_jsonl(index_dir / "all-docs.jsonl")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(manifest["documents"], 1)
            self.assertNotIn("skill", manifest["tags"])
            self.assertEqual([entry["path"] for entry in all_docs], ["docs/sample-dnl/doc.md"])


if __name__ == "__main__":
    unittest.main()
