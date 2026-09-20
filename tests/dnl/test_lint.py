from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts/dnl/lint.py"


class LintTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "dnl-config.toml").write_text(
            '[scan]\ninclude = ["docs"]\nexclude = ["excluded"]\n',
            encoding="utf-8",
        )

    def document(self, name: str, count: int) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        entries = "\n".join(f'  "@p{i}": "target{i}"' for i in range(count))
        path.write_text(
            '---\nname: "Test"\nstatus: "draft"\ntags: []\npaths:\n'
            + entries + '\n---\n# Body\n', encoding="utf-8",
        )
        return path

    def run_lint(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            cwd=self.root, capture_output=True, text=True, check=False,
        )

    def test_inclusive_threshold_sorting_and_warning_exit(self) -> None:
        self.document("docs/below.md", 14)
        self.document("docs/boundary.md", 15)
        self.document("docs/largest.md", 20)
        result = self.run_lint()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("below.md", result.stdout)
        self.assertIn("paths=15 (>= 15)", result.stdout)
        self.assertLess(result.stdout.index("largest.md"), result.stdout.index("boundary.md"))
        self.assertIn("3 Markdown files: 2 warnings, 0 errors", result.stdout)

    def test_scope_exclusions_deduplication_and_custom_threshold(self) -> None:
        self.document("docs/selected.md", 2)
        self.document("docs/excluded/ignored.md", 20)
        self.document("docs/.hidden/ignored.md", 20)
        self.document("docs/SKILL.md", 20)
        self.document("other/not-selected.md", 20)
        result = self.run_lint("docs", "docs/selected.md", "--paths-threshold", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 Markdown files: 1 warnings", result.stdout)

    def test_body_examples_are_not_paths(self) -> None:
        path = self.document("docs/example.md", 1)
        with path.open("a", encoding="utf-8") as stream:
            stream.write('\n```yaml\npaths:\n  "@body": "example"\n```\n')
        result = self.run_lint("docs/example.md", "--paths-threshold", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0 warnings, 0 errors", result.stdout)

    def test_bad_input_is_not_a_clean_run(self) -> None:
        self.document("docs/good.md", 1)
        for args in [("missing.md",), ("--paths-threshold", "0"), ("../outside",)]:
            with self.subTest(args=args):
                self.assertEqual(self.run_lint(*args).returncode, 2)

    def test_directory_alias_counts_once_and_lint_leaves_files_unchanged(self) -> None:
        path = self.document("docs/aliases.md", 1)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n".join(f"See @p0/child{i}.md" for i in range(20)))
        before = {
            file.relative_to(self.root): (file.read_bytes(), file.stat().st_mtime_ns)
            for file in self.root.rglob("*") if file.is_file()
        }
        result = self.run_lint("--paths-threshold", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 Markdown files: 0 warnings, 0 errors", result.stdout)
        after = {
            file.relative_to(self.root): (file.read_bytes(), file.stat().st_mtime_ns)
            for file in self.root.rglob("*") if file.is_file()
        }
        self.assertEqual(after, before)

    def test_duplicate_paths_report_parse_error(self) -> None:
        path = self.document("docs/duplicate.md", 1)
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace('  "@p0": "target0"',
                                    '  "@p0": "target0"\n  "@p0": "other"'),
                        encoding="utf-8")
        result = self.run_lint()
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR docs/duplicate.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
