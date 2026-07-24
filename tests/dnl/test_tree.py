from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DNL = REPO_ROOT / "scripts" / "dnl"
sys.path.insert(0, str(SCRIPTS_DNL))

from tree import DEFAULT_IGNORES, IgnoreMatcher, build_tree, format_tree_text, load_gitignore_patterns


def find_child(node_name: str, children: list) -> object | None:
    for child in children:
        if child.name == node_name:
            return child
    return None


class TreeSkillSmokeTest(unittest.TestCase):
    def test_legacy_skill_path_shims_to_script_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Compatibility Root\n", encoding="utf-8")
            script = REPO_ROOT / ".agents" / "skills" / "tree" / "tree.py"

            completed = subprocess.run(
                [sys.executable, str(script), "--root", str(root), "--depth", "1", "--ascii"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("Compatibility Root", completed.stdout)

    def test_directory_readme_h1_is_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Docs Folder\n\ncontent\n", encoding="utf-8")
            (docs / "notes.txt").write_text("x", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=3,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            docs_node = find_child("docs", tree.children)
            self.assertIsNotNone(docs_node)
            self.assertEqual(docs_node.readme_title, "Docs Folder")

    def test_root_readme_title_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Sample DNL Root\n\ncontent\n", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=False,
                max_depth=2,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            self.assertEqual(tree.readme_title, "Sample DNL Root")

    def test_tree_text_uses_hash_separator_for_readme_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Sample DNL Root\n", encoding="utf-8")
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Docs Folder\n", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=False,
                max_depth=3,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            rendered = format_tree_text(tree, use_unicode=True)
            self.assertIn(f"{root.name}/ [1 dirs, 2 files] # Sample DNL Root", rendered)
            self.assertIn("docs/ [0 dirs, 1 files] # Docs Folder", rendered)
            self.assertNotIn(" — ", rendered)
            self.assertNotIn(" - ", rendered)

    def test_tree_text_adds_trailing_slash_to_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample_product = root / "sample-product"
            sample_product.mkdir()
            skills = root / ".agents" / "skills"
            skills.mkdir(parents=True)
            (sample_product / "README.md").write_text("# Sample Product", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=3,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            rendered = format_tree_text(tree, use_unicode=True)
            self.assertIn("sample-product/ [0 dirs, 1 files] # Sample Product", rendered)
            self.assertIn(".agents/ [1 dirs, 0 files]", rendered)

    def test_readme_h1_is_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text("# DNL Root\n\ncontent\n", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=2,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            readme_node = find_child("README.md", tree.children)
            self.assertIsNotNone(readme_node)
            self.assertEqual(readme_node.readme_title, "DNL Root")

    def test_markdown_file_h1_is_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "notes.md"
            doc.write_text("# Notes File\n\ncontent\n", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=2,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            doc_node = find_child("notes.md", tree.children)
            self.assertIsNotNone(doc_node)
            self.assertEqual(doc_node.readme_title, "Notes File")

    def test_markdown_file_yaml_name_takes_priority_over_h1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "notes.md"
            doc.write_text('---\nname: "YAML Notes"\npaths: {}\n---\n# H1 Notes\n', encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=2,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            doc_node = find_child("notes.md", tree.children)
            self.assertIsNotNone(doc_node)
            self.assertEqual(doc_node.readme_title, "YAML Notes")

    def test_markdown_file_starting_with_horizontal_rule_keeps_h1_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "notes.md"
            doc.write_text("---\n\n# H1 Notes\n\n---\n", encoding="utf-8")

            matcher = IgnoreMatcher(root=root, patterns=[])
            tree = build_tree(
                root,
                include_files=True,
                max_depth=2,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=True,
                absolute_paths=False,
            )

            doc_node = find_child("notes.md", tree.children)
            self.assertIsNotNone(doc_node)
            self.assertEqual(doc_node.readme_title, "H1 Notes")

    def test_gitignore_patterns_are_applied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text("ignored_dir/\n*.tmp\n", encoding="utf-8")
            (root / "ignored_dir").mkdir()
            (root / "ignored_dir" / "blocked.txt").write_text("x", encoding="utf-8")
            (root / "visible_dir").mkdir()
            (root / "visible_dir" / "ok.txt").write_text("ok", encoding="utf-8")
            (root / "note.tmp").write_text("tmp", encoding="utf-8")

            patterns = list(DEFAULT_IGNORES)
            patterns.extend(load_gitignore_patterns(root))
            matcher = IgnoreMatcher(root=root, patterns=patterns)
            tree = build_tree(
                root,
                include_files=True,
                max_depth=3,
                show_hidden=True,
                matcher=matcher,
                readme_title_enabled=False,
                absolute_paths=False,
            )

            top_names = [child.name for child in tree.children]
            self.assertNotIn("ignored_dir", top_names)
            self.assertNotIn("note.tmp", top_names)
            self.assertIn("visible_dir", top_names)


if __name__ == "__main__":
    unittest.main()
