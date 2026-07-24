from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DnlQueryTest(unittest.TestCase):
    def run_query(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        script = Path(__file__).resolve().parents[2] / "scripts" / "dnl" / "query.py"
        return subprocess.run(
            [sys.executable, str(script), "--root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def write_index(self, root: Path) -> Path:
        index_dir = root / ".agents/skills/dnl-query/tag-index"
        tags_dir = index_dir / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)

        entries = [
            {
                "path": "docs/glossary/terms.md",
                "name": "Glossary Terms",
                "status": "draft",
                "tags": ["glossary-dnl"],
                "description": [],
            },
            {
                "path": "docs/sample-dnl/sample-product/sample-project/develop/rules/i18n/basics.md",
                "name": "Internationalization Basics",
                "status": "active",
                "tags": ["rule-dnl", "i18n"],
                "description": ["This document explains the internationalization basics."],
            },
            {
                "path": "docs/sample-dnl/sample-product/sample-project/glossary/path-tokens.md",
                "name": "Path Tokens",
                "status": "draft",
                "tags": ["glossary-dnl", "reference-dnl"],
                "description": [],
            },
            {
                "path": "docs/sample-dnl/sample-product/sample-project/modules/mail/README.md",
                "name": "Mail Portal",
                "status": "draft",
                "tags": ["portal-dnl", "sample-module"],
                "description": [],
            },
        ]
        tag_map = {
            "sample-module": [entries[3]],
            "glossary-dnl": [entries[0], entries[2]],
            "i18n": [entries[1]],
            "portal-dnl": [entries[3]],
            "reference-dnl": [entries[2]],
            "rule-dnl": [entries[1]],
        }
        manifest = {
            "schemaVersion": 1,
            "sources": ["docs", "DNL-system", "docs/sample-dnl", ".agents/skills"],
            "documents": len(entries),
            "statusCounts": {"active": 1, "draft": 3, "deprecated": 0},
            "untaggedDocuments": 0,
            "tags": {
                tag: {"file": f"tags/{tag}.jsonl", "count": len(tag_entries)}
                for tag, tag_entries in tag_map.items()
            },
        }

        (index_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (index_dir / "all-docs.jsonl").write_text(self.jsonl(entries), encoding="utf-8")
        for tag, tag_entries in tag_map.items():
            (tags_dir / f"{tag}.jsonl").write_text(self.jsonl(tag_entries), encoding="utf-8")
        return index_dir

    def write_link_index(self, root: Path) -> Path:
        index_dir = root / ".agents/skills/dnl-query/link-index"
        index_dir.mkdir(parents=True, exist_ok=True)
        links = [
            {
                "source": "docs/sample-dnl/README.md",
                "token": "@ai/README.md",
                "target": "{@DNL-system}/ai/README.md",
                "targetKind": "internal",
                "targetVariable": "DNL-system",
                "targetPath": "DNL-system/ai/README.md",
                "targetExists": True,
                "usedInBody": True,
            },
            {
                "source": "docs/sample-dnl/README.md",
                "token": "@missing.md",
                "target": "{@dnl-root}/docs/sample-dnl/missing.md",
                "targetKind": "internal",
                "targetVariable": "dnl-root",
                "targetPath": "docs/sample-dnl/missing.md",
                "targetExists": False,
                "usedInBody": True,
                "unresolvedReason": "target-not-found",
            },
        ]
        backlinks = [
            {
                "targetPath": "DNL-system/ai/README.md",
                "sources": [
                    {
                        "source": "docs/sample-dnl/README.md",
                        "token": "@ai/README.md",
                    }
                ],
            }
        ]
        unresolved = [links[1]]
        unused = [
            {
                "source": "docs/sample-dnl/README.md",
                "token": "@unused.md",
                "target": "{@dnl-root}/docs/sample-dnl/unused.md",
                "targetKind": "internal",
                "targetVariable": "dnl-root",
                "targetPath": "docs/sample-dnl/unused.md",
                "targetExists": True,
                "usedInBody": False,
            }
        ]
        missing_tokens = [
            {
                "source": "docs/sample-dnl/README.md",
                "token": "@undeclared.md",
                "count": 2,
            }
        ]
        manifest = {
            "schemaVersion": 1,
            "sources": ["docs", "DNL-system", "docs/sample-dnl"],
            "documents": 2,
            "links": len(links),
            "backlinks": len(backlinks),
            "unresolvedPaths": len(unresolved),
            "unusedPathTokens": len(unused),
            "missingPathTokens": len(missing_tokens),
        }
        (index_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (index_dir / "all-links.jsonl").write_text(self.jsonl(links), encoding="utf-8")
        (index_dir / "backlinks.jsonl").write_text(self.jsonl(backlinks), encoding="utf-8")
        (index_dir / "unresolved-paths.jsonl").write_text(self.jsonl(unresolved), encoding="utf-8")
        (index_dir / "unused-paths.jsonl").write_text(self.jsonl(unused), encoding="utf-8")
        (index_dir / "missing-path-tokens.jsonl").write_text(self.jsonl(missing_tokens), encoding="utf-8")
        return index_dir

    @staticmethod
    def jsonl(entries: list[dict[str, object]]) -> str:
        return "\n".join(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries) + "\n"

    def test_tags_lists_manifest_tags_by_count_then_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_index(root)

            completed = self.run_query(root, "tags")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                completed.stdout.splitlines(),
                [
                    "glossary-dnl 2",
                    "i18n 1",
                    "portal-dnl 1",
                    "reference-dnl 1",
                    "rule-dnl 1",
                    "sample-module 1",
                ],
            )

    def test_tags_can_output_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_index(root)

            completed = self.run_query(root, "tags", "--format", "json")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            tags = json.loads(completed.stdout)
            self.assertEqual(tags[0], {"tag": "glossary-dnl", "count": 2})

    def test_legacy_skill_path_shims_to_script_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_index(root)
            script = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "dnl-query" / "dnl_query.py"

            completed = subprocess.run(
                [sys.executable, str(script), "--root", str(root), "tags"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("glossary-dnl 2", completed.stdout)

    def test_docs_lists_documents_for_tag_in_text_paths_and_jsonl_formats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_index(root)

            text = self.run_query(root, "docs", "--tag", "glossary-dnl")
            paths = self.run_query(root, "docs", "--tag", "glossary-dnl", "--format", "paths")
            jsonl = self.run_query(root, "docs", "--tag", "glossary-dnl", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(
                text.stdout.splitlines(),
                [
                    "docs/glossary/terms.md | draft | Glossary Terms",
                    "docs/sample-dnl/sample-product/sample-project/glossary/path-tokens.md | draft | Path Tokens",
                ],
            )
            self.assertEqual(
                paths.stdout.splitlines(),
                [
                    "docs/glossary/terms.md",
                    "docs/sample-dnl/sample-product/sample-project/glossary/path-tokens.md",
                ],
            )
            self.assertEqual(
                [json.loads(line)["path"] for line in jsonl.stdout.splitlines()],
                [
                    "docs/glossary/terms.md",
                    "docs/sample-dnl/sample-product/sample-project/glossary/path-tokens.md",
                ],
            )

    def test_docs_filters_by_multiple_tags_status_under_and_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_index(root)

            completed = self.run_query(
                root,
                "docs",
                "--tag",
                "glossary-dnl",
                "--tag",
                "reference-dnl",
                "--status",
                "draft",
                "--under",
                "docs/sample-dnl/sample-product",
                "--name",
                "PATH",
                "--format",
                "paths",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                completed.stdout.splitlines(),
                ["docs/sample-dnl/sample-product/sample-project/glossary/path-tokens.md"],
            )

    def test_missing_index_fails_with_builder_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            completed = self.run_query(root, "tags")

            self.assertEqual(completed.returncode, 2)
            self.assertIn("DNL query index not found", completed.stderr)
            self.assertIn(".agents/skills/dnl-builder/dnl_util.py tag index build", completed.stderr)

    def test_links_lists_outbound_links_for_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            text = self.run_query(root, "links", "--path", "docs/sample-dnl/README.md")
            paths = self.run_query(root, "links", "--path", "docs/sample-dnl/README.md", "--format", "paths")
            jsonl = self.run_query(root, "links", "--path", "docs/sample-dnl/README.md", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(
                text.stdout.splitlines(),
                [
                    "docs/sample-dnl/README.md | @ai/README.md -> DNL-system/ai/README.md",
                    "docs/sample-dnl/README.md | @missing.md -> docs/sample-dnl/missing.md | target-not-found",
                ],
            )
            self.assertEqual(paths.stdout.splitlines(), ["DNL-system/ai/README.md", "docs/sample-dnl/missing.md"])
            self.assertEqual(
                [json.loads(line)["token"] for line in jsonl.stdout.splitlines()],
                ["@ai/README.md", "@missing.md"],
            )

    def test_backlinks_lists_sources_for_target_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            text = self.run_query(root, "backlinks", "--path", "DNL-system/ai/README.md")
            paths = self.run_query(root, "backlinks", "--path", "DNL-system/ai/README.md", "--format", "paths")
            jsonl = self.run_query(root, "backlinks", "--path", "DNL-system/ai/README.md", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(text.stdout.splitlines(), ["docs/sample-dnl/README.md | @ai/README.md -> DNL-system/ai/README.md"])
            self.assertEqual(paths.stdout.splitlines(), ["docs/sample-dnl/README.md"])
            self.assertEqual(json.loads(jsonl.stdout)["targetPath"], "DNL-system/ai/README.md")

    def test_deps_outputs_script_friendly_dependency_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            completed = self.run_query(
                root,
                "deps",
                "--path",
                "docs/sample-dnl/README.md",
                "--format",
                "json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            plan = json.loads(completed.stdout)
            self.assertEqual(plan["path"], "docs/sample-dnl/README.md")
            self.assertEqual(plan["counts"]["outboundLinks"], 2)
            self.assertEqual(plan["counts"]["backlinks"], 0)
            self.assertEqual(plan["counts"]["unresolvedOutboundLinks"], 1)
            self.assertEqual(
                [entry["token"] for entry in plan["outboundLinks"]],
                ["@ai/README.md", "@missing.md"],
            )
            self.assertEqual(plan["backlinks"], [])

            target_completed = self.run_query(
                root,
                "deps",
                "--path",
                "DNL-system/ai/README.md",
                "--format",
                "json",
            )

            self.assertEqual(target_completed.returncode, 0, target_completed.stderr)
            target_plan = json.loads(target_completed.stdout)
            self.assertEqual(target_plan["counts"]["outboundLinks"], 0)
            self.assertEqual(target_plan["counts"]["backlinks"], 1)
            self.assertEqual(target_plan["backlinks"][0]["source"], "docs/sample-dnl/README.md")
            self.assertEqual(target_plan["backlinks"][0]["token"], "@ai/README.md")

    def test_unresolved_lists_unresolved_link_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            completed = self.run_query(root, "unresolved")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                completed.stdout.splitlines(),
                ["docs/sample-dnl/README.md | @missing.md -> docs/sample-dnl/missing.md | target-not-found"],
            )

    def test_unresolved_summary_groups_by_source_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_dir = self.write_link_index(root)
            unresolved = [
                {
                    "source": "docs/sample-dnl/README.md",
                    "token": "@missing.md",
                    "targetPath": "docs/sample-dnl/missing.md",
                    "unresolvedReason": "target-not-found",
                },
                {
                    "source": "docs/sample-dnl/future/cmm/reserve/plan/01-context.md",
                    "token": "@plan.md",
                    "targetPath": "docs/sample-dnl/future/cmm/reserve/plan/README.md",
                    "unresolvedReason": "target-not-found",
                },
                {
                    "source": "docs/sample-dnl/future/cmm/reserve/plan/02-table.md",
                    "token": "@ddl.sql",
                    "targetPath": "docs/sample-dnl/future/cmm/reserve/database/ddl.sql",
                    "unresolvedReason": "target-not-found",
                },
            ]
            (index_dir / "unresolved-paths.jsonl").write_text(self.jsonl(unresolved), encoding="utf-8")

            text = self.run_query(root, "unresolved-summary", "--depth", "4")
            paths = self.run_query(root, "unresolved-summary", "--depth", "4", "--format", "paths")
            jsonl = self.run_query(root, "unresolved-summary", "--depth", "4", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(
                text.stdout.splitlines(),
                [
                    "docs/sample-dnl/future/cmm | unresolved=2 | sources=2",
                    "docs/sample-dnl | unresolved=1 | sources=1",
                ],
            )
            self.assertEqual(paths.stdout.splitlines(), ["docs/sample-dnl/future/cmm", "docs/sample-dnl"])
            self.assertEqual(
                [json.loads(line)["group"] for line in jsonl.stdout.splitlines()],
                ["docs/sample-dnl/future/cmm", "docs/sample-dnl"],
            )

    def test_missing_link_index_fails_with_link_builder_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            completed = self.run_query(root, "backlinks", "--path", "docs/sample-dnl/README.md")

            self.assertEqual(completed.returncode, 2)
            self.assertIn("DNL query index not found", completed.stderr)
            self.assertIn(".agents/skills/dnl-builder/dnl_util.py link index build", completed.stderr)

    def test_unused_lists_unused_path_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            text = self.run_query(root, "unused")
            paths = self.run_query(root, "unused", "--format", "paths")
            jsonl = self.run_query(root, "unused", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(text.stdout.splitlines(), ["docs/sample-dnl/README.md | @unused.md -> docs/sample-dnl/unused.md"])
            self.assertEqual(paths.stdout.splitlines(), ["docs/sample-dnl/unused.md"])
            self.assertEqual(json.loads(jsonl.stdout)["token"], "@unused.md")

    def test_missing_tokens_lists_missing_path_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_link_index(root)

            text = self.run_query(root, "missing-tokens")
            paths = self.run_query(root, "missing-tokens", "--format", "paths")
            jsonl = self.run_query(root, "missing-tokens", "--format", "jsonl")

            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(jsonl.returncode, 0, jsonl.stderr)
            self.assertEqual(text.stdout.splitlines(), ["docs/sample-dnl/README.md | @undeclared.md | count=2"])
            self.assertEqual(paths.stdout.splitlines(), ["docs/sample-dnl/README.md"])
            self.assertEqual(json.loads(jsonl.stdout)["token"], "@undeclared.md")

    def test_cli_handles_broken_pipe_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_dir = self.write_link_index(root)
            unused = [
                {
                    "source": f"docs/sample-dnl/source-{index}.md",
                    "token": f"@unused-{index}.md",
                    "targetPath": f"docs/sample-dnl/unused-{index}.md",
                }
                for index in range(10_000)
            ]
            (index_dir / "unused-paths.jsonl").write_text(self.jsonl(unused), encoding="utf-8")
            script = Path(__file__).resolve().parents[2] / "scripts" / "dnl" / "query.py"

            process = subprocess.Popen(
                [sys.executable, str(script), "--root", str(root), "unused"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertIsNotNone(process.stdout)
            self.assertIsNotNone(process.stderr)

            first_line = process.stdout.readline()
            process.stdout.close()
            stderr = process.stderr.read()
            process.stderr.close()
            returncode = process.wait(timeout=10)

            self.assertTrue(first_line)
            self.assertEqual(returncode, 0, stderr)
            self.assertNotIn("BrokenPipeError", stderr)
            self.assertNotIn("Traceback", stderr)


if __name__ == "__main__":
    unittest.main()
