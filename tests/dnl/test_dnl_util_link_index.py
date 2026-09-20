from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DnlUtilLinkIndexTest(unittest.TestCase):
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

    def read_jsonl(self, path: Path) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_link_index_build_reports_links_and_token_health(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/target.md")
            self.write_doc(root, "docs/sample-dnl/unused.md")
            self.write_doc(
                root,
                "docs/sample-dnl/source.md",
                paths={
                    "@target.md": "{@dnl-root}/docs/sample-dnl/target.md",
                    "@missing.md": "{@dnl-root}/docs/sample-dnl/missing.md",
                    "@unused.md": "{@dnl-root}/docs/sample-dnl/unused.md",
                },
                body="When reading, use @target.md and @missing.md, and also mention @undeclared.md.",
            )

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("LINK INDEX BUILD", completed.stdout)

            index_dir = root / ".agents/skills/dnl-query/link-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
            all_links = self.read_jsonl(index_dir / "all-links.jsonl")
            backlinks = self.read_jsonl(index_dir / "backlinks.jsonl")
            unresolved = self.read_jsonl(index_dir / "unresolved-paths.jsonl")
            unused = self.read_jsonl(index_dir / "unused-paths.jsonl")
            missing_tokens = self.read_jsonl(index_dir / "missing-path-tokens.jsonl")

            self.assertEqual(manifest["schemaVersion"], 1)
            self.assertEqual(manifest["documents"], 3)
            self.assertEqual(manifest["links"], 3)
            self.assertEqual(manifest["unresolvedPaths"], 1)
            self.assertEqual(manifest["unusedPathTokens"], 1)
            self.assertEqual(manifest["missingPathTokens"], 1)
            self.assertEqual([entry["token"] for entry in all_links], ["@missing.md", "@target.md", "@unused.md"])
            self.assertEqual(unresolved[0]["token"], "@missing.md")
            self.assertEqual(unused[0]["token"], "@unused.md")
            self.assertEqual(missing_tokens[0]["token"], "@undeclared.md")
            self.assertEqual(backlinks[0]["targetPath"], "docs/sample-dnl/target.md")
            self.assertEqual(backlinks[0]["sources"][0]["source"], "docs/sample-dnl/source.md")

    def test_link_index_build_resolves_dnl_root_as_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/target.md")
            self.write_doc(
                root,
                "docs/sample-dnl/source.md",
                paths={"@target.md": "{@dnl-root}/docs/sample-dnl/target.md"},
                body="The root-variable link resolves through @target.md.",
            )

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)

            index_dir = root / ".agents/skills/dnl-query/link-index"
            all_links = self.read_jsonl(index_dir / "all-links.jsonl")
            unresolved = self.read_jsonl(index_dir / "unresolved-paths.jsonl")

            self.assertEqual(all_links[0]["targetKind"], "internal")
            self.assertEqual(all_links[0]["targetPath"], "docs/sample-dnl/target.md")
            self.assertEqual(unresolved, [])

    def test_link_index_build_resolves_literal_targets_from_source_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/area/target.md")
            self.write_doc(
                root,
                "docs/sample-dnl/area/source.md",
                paths={"@target.md": "target.md"},
                body="The relative link resolves through @target.md.",
            )

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            all_links = self.read_jsonl(index_dir / "all-links.jsonl")
            unresolved = self.read_jsonl(index_dir / "unresolved-paths.jsonl")

            self.assertEqual(all_links[0]["targetKind"], "literal")
            self.assertEqual(all_links[0]["targetPath"], "docs/sample-dnl/area/target.md")
            self.assertEqual(unresolved, [])

    def test_link_index_build_reads_slash_tokens_as_one_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root, include=("docs", "DNL-system"))
            self.write_doc(root, "DNL-system/ai/README.md")
            self.write_doc(
                root,
                "docs/sample-dnl/README.md",
                paths={"@ai/README.md": "{@DNL-system}/ai/README.md"},
                body="The AI rules live under @ai/README.md.",
            )

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            all_links = self.read_jsonl(index_dir / "all-links.jsonl")
            missing_tokens = self.read_jsonl(index_dir / "missing-path-tokens.jsonl")

            self.assertTrue(all_links[0]["usedInBody"])
            self.assertEqual(missing_tokens, [])

    def test_link_index_build_reports_only_path_like_missing_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(
                root,
                "docs/sample-dnl/source.md",
                body=(
                    "The only missing-path candidate is @undeclared.md, "
                    "while @example.com, @ControllerAdvice, and @sample-token stay ignored."
                ),
            )

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            missing_tokens = self.read_jsonl(index_dir / "missing-path-tokens.jsonl")

            self.assertEqual([entry["token"] for entry in missing_tokens], ["@undeclared.md"])

    def test_directory_alias_indexes_children_and_supports_queries_and_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/guides/target.md")
            self.write_doc(
                root, "docs/source.md", paths={"@guide": "{@docs}/guides/"},
                body="Use `@guide/target.md` twice: @guide/target.md. Also @guide/missing.md.",
            )
            completed = self.run_util(root, "link", "index", "build")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            links = self.read_jsonl(index_dir / "all-links.jsonl")
            self.assertEqual(len(links), 3)
            self.assertTrue(all(row["usedInBody"] for row in links))
            self.assertEqual(self.read_jsonl(index_dir / "unused-paths.jsonl"), [])
            self.assertEqual(self.read_jsonl(index_dir / "missing-path-tokens.jsonl"), [])
            unresolved = self.read_jsonl(index_dir / "unresolved-paths.jsonl")
            self.assertEqual([row["token"] for row in unresolved], ["@guide/missing.md"])
            self.assertEqual(unresolved[0]["unresolvedReason"], "target-not-found")
            query_script = self.REPO_ROOT / "scripts/dnl/query.py"
            query = subprocess.run(
                [sys.executable, str(query_script), "--root", str(root), "backlinks",
                 "--path", "docs/guides/target.md", "--format", "jsonl"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(query.returncode, 0, query.stderr)
            self.assertEqual(json.loads(query.stdout)["token"], "@guide/target.md")
            qa_script = self.REPO_ROOT / "scripts/dnl/qa.py"
            qa = subprocess.run(
                [sys.executable, str(qa_script), "--root", str(root), "--profile", "health",
                 "--json-summary"], capture_output=True, text=True, check=False,
            )
            self.assertEqual(qa.returncode, 0, qa.stderr)
            health = json.loads(qa.stdout)["link_health"]
            self.assertEqual(health["missingPathTokens"], 0)
            self.assertEqual(health["unusedPathTokens"], 0)
            self.assertEqual(health["unresolvedPaths"], 1)

    def test_directory_alias_exact_then_longest_prefix_with_slash_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            for name in ["general/one.md", "special/two.md", "override.md"]:
                self.write_doc(root, f"docs/{name}")
            self.write_doc(
                root, "docs/source.md",
                paths={"@guide": "{@docs}/general", "@guide/sub": "{@docs}/special",
                       "@guide/sub/exact.md": "{@docs}/override.md"},
                body="@guide/one.md @guide/sub/two.md @guide/sub/exact.md @guides/no.md",
            )
            result = self.run_util(root, "link", "index", "build")
            self.assertEqual(result.returncode, 0, result.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            links = {row["token"]: row for row in self.read_jsonl(index_dir / "all-links.jsonl")}
            self.assertEqual(links["@guide/one.md"]["targetPath"], "docs/general/one.md")
            self.assertEqual(links["@guide/sub/two.md"]["targetPath"], "docs/special/two.md")
            self.assertEqual(links["@guide/sub/exact.md"]["targetPath"], "docs/override.md")
            missing = self.read_jsonl(index_dir / "missing-path-tokens.jsonl")
            self.assertEqual([row["token"] for row in missing], ["@guides/no.md"])

    def test_external_directory_alias_preserves_unverified_external_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            with (root / "dnl-config.toml").open("a", encoding="utf-8") as stream:
                stream.write('\n[paths.external]\n"server" = {required = false, validate = "if-defined"}\n')
            self.write_doc(
                root, "docs/source.md", paths={"@dev": "{@server}/docs/04-development"},
                body="`@dev/query-guide.md`",
            )
            result = self.run_util(root, "link", "index", "build")
            self.assertEqual(result.returncode, 0, result.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            links = self.read_jsonl(index_dir / "all-links.jsonl")
            child = next(row for row in links if row["token"] == "@dev/query-guide.md")
            self.assertEqual(child["target"], "{@server}/docs/04-development/query-guide.md")
            self.assertEqual(child["declaredToken"], "@dev")
            self.assertEqual(child["targetKind"], "external")
            self.assertIsNone(child["targetExists"])
            self.assertEqual(self.read_jsonl(index_dir / "missing-path-tokens.jsonl"), [])

    def test_invalid_directory_references_are_unresolved_not_backlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/guides/target.md")
            self.write_doc(root, "docs/outside.md")
            self.write_doc(
                root, "docs/source.md",
                paths={"@guide": "{@docs}/guides", "@file": "{@docs}/outside.md",
                       "@web": "https://example.com/docs", "@unused": "{@docs}"},
                body=("@guide/../outside.md @guide//target.md @file/child.md @web/child.md\n"
                      "```md\n@unused/outside.md\n```\n"),
            )
            result = self.run_util(root, "link", "index", "build")
            self.assertEqual(result.returncode, 0, result.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            unresolved = self.read_jsonl(index_dir / "unresolved-paths.jsonl")
            reasons = {row["token"]: row["unresolvedReason"] for row in unresolved}
            self.assertEqual(reasons["@guide/../outside.md"], "invalid-alias-suffix")
            self.assertEqual(reasons["@guide//target.md"], "invalid-alias-suffix")
            self.assertEqual(reasons["@file/child.md"], "alias-base-not-directory")
            self.assertEqual(reasons["@web/child.md"], "directory-alias-requires-local-path")
            unused = self.read_jsonl(index_dir / "unused-paths.jsonl")
            self.assertEqual([row["token"] for row in unused], ["@unused"])
            backlinks = self.read_jsonl(index_dir / "backlinks.jsonl")
            self.assertEqual(backlinks[0]["sources"][0]["token"], "@file")

    def test_link_index_build_skips_hidden_dirs_and_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/live.md")
            self.write_doc(root, "docs/sample-dnl/.hidden/doc.md")
            self.write_doc(root, "docs/sample-dnl/SKILL.md")

            completed = self.run_util(root, "link", "index", "build")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(manifest["documents"], 1)

    def test_link_index_check_detects_stale_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            source = self.write_doc(
                root,
                "docs/sample-dnl/source.md",
                paths={"@target.md": "{@dnl-root}/docs/sample-dnl/target.md"},
                body="This source currently uses @target.md.",
            )
            self.write_doc(root, "docs/sample-dnl/target.md")

            build = self.run_util(root, "link", "index", "build")
            self.assertEqual(build.returncode, 0, build.stderr)

            fresh = self.run_util(root, "link", "index", "check")
            self.assertEqual(fresh.returncode, 0, fresh.stderr)
            self.assertIn("OK", fresh.stdout)

            source.write_text(
                source.read_text(encoding="utf-8").replace("@target.md", "@missing-token.md"),
                encoding="utf-8",
            )

            stale = self.run_util(root, "link", "index", "check")

            self.assertEqual(stale.returncode, 1)
            self.assertIn("STALE", stale.stdout)

    def test_link_index_check_detects_extra_index_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_scan_config(root)
            self.write_doc(root, "docs/sample-dnl/source.md")

            build = self.run_util(root, "link", "index", "build")
            self.assertEqual(build.returncode, 0, build.stderr)
            index_dir = root / ".agents/skills/dnl-query/link-index"
            (index_dir / "old-report.jsonl").write_text("", encoding="utf-8")

            stale = self.run_util(root, "link", "index", "check")

            self.assertEqual(stale.returncode, 1)
            self.assertIn("extra_files=1", stale.stdout)


if __name__ == "__main__":
    unittest.main()
