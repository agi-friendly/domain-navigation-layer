from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DnlUtilMvTest(unittest.TestCase):
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

    def write_scan_config(self, root: Path, include: tuple[str, ...] = ("docs",)) -> None:
        include_block = ", ".join(f'"{item}"' for item in include)
        (root / "dnl-config.toml").write_text(
            f"""
[scan]
include = [{include_block}]
exclude = []

[paths.internal]
"docs" = "docs"
""".strip(),
            encoding="utf-8",
        )

    def write_doc(
        self,
        root: Path,
        relative_path: str,
        *,
        paths: dict[str, str] | None = None,
        body: str = "",
    ) -> Path:
        path_lines = ["paths:"]
        if paths:
            path_lines.extend(f'  "{token}": "{target}"' for token, target in paths.items())
        else:
            path_lines = ["paths: {}"]

        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                [
                    "---",
                    f'name: "{path.stem}"',
                    'status: "draft"',
                    'tags: ["sample"]',
                    *path_lines,
                    "---",
                    "",
                    f"# {path.stem}",
                    body,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return path

    def arrange_move_fixture(self, root: Path) -> tuple[Path, Path]:
        self.write_scan_config(root)
        source = self.write_doc(root, "docs/source/target.md")
        destination_dir = root / "docs/reference"
        destination_dir.mkdir(parents=True)
        self.write_doc(
            root,
            "docs/referrer.md",
            paths={"@target.md": "{@docs}/source/target.md"},
            body="Use @target.md for this sample route.",
        )
        return source, destination_dir

    def test_mv_dry_run_reports_plan_without_moving_or_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)
            referrer = root / "docs/referrer.md"

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/target.md",
                "--to",
                "docs/reference",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("DNL MV: mode=dry-run", completed.stdout)
            self.assertIn("source=docs/source/target.md", completed.stdout)
            self.assertIn("destination=docs/reference/target.md", completed.stdout)
            self.assertIn("backlink_updates=1", completed.stdout)
            self.assertIn("UPDATE source=docs/referrer.md token=@target.md", completed.stdout)
            self.assertTrue(source.exists())
            self.assertFalse((root / "docs/reference/target.md").exists())
            self.assertIn("{@docs}/source/target.md", referrer.read_text(encoding="utf-8"))

    def test_mv_write_moves_file_and_updates_backlink_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)
            referrer = root / "docs/referrer.md"

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "{@docs}/source/target.md",
                "--to",
                "{@docs}/reference",
                "--write",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("DNL MV: mode=write", completed.stdout)
            self.assertIn("moved=1", completed.stdout)
            self.assertFalse(source.exists())
            self.assertTrue((root / "docs/reference/target.md").exists())
            self.assertIn("{@docs}/reference/target.md", referrer.read_text(encoding="utf-8"))

    def test_mv_rejects_missing_destination_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/target.md",
                "--to",
                "docs/missing",
                "--write",
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("destination directory does not exist", completed.stderr)
            self.assertTrue(source.exists())

    def test_mv_rejects_file_destination_rename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/target.md",
                "--to",
                "docs/reference/renamed.md",
                "--write",
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("rename is not supported", completed.stderr)
            self.assertTrue(source.exists())

    def test_mv_rejects_external_token_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            source = self.write_doc(root, "docs/source/target.md")
            destination_dir = root / "docs/reference"
            destination_dir.mkdir(parents=True)
            config = (root / "dnl-config.toml").read_text(encoding="utf-8")
            (root / "dnl-config.toml").write_text(
                config
                + """

[paths.external.public-docs]
required = false
validate = "if-defined"
""",
                encoding="utf-8",
            )

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "{@public-docs}/target.md",
                "--to",
                "docs/reference",
                "--write",
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("path token must use [paths.internal]", completed.stderr)
            self.assertTrue(source.exists())

    def test_mv_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/../source/target.md",
                "--to",
                "docs/reference",
                "--write",
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("path must not contain parent traversal", completed.stderr)
            self.assertTrue(source.exists())

    def test_mv_rejects_source_with_local_markdown_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)
            source.write_text(
                source.read_text(encoding="utf-8")
                + "\n![sample-screen](assets/sample-screen.png)\n",
                encoding="utf-8",
            )

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/target.md",
                "--to",
                "docs/reference",
                "--write",
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("source document has local markdown links or images", completed.stderr)
            self.assertTrue(source.exists())

    def test_mv_ignores_markdown_link_examples_in_inline_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _ = self.arrange_move_fixture(root)
            source.write_text(
                source.read_text(encoding="utf-8")
                + "\nExample: `![sample-screen](assets/sample-screen.png)`\n",
                encoding="utf-8",
            )

            completed = self.run_util(
                root,
                "mv",
                "--path",
                "docs/source/target.md",
                "--to",
                "docs/reference",
                "--write",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(source.exists())
            self.assertTrue((root / "docs/reference/target.md").exists())


if __name__ == "__main__":
    unittest.main()
