from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SHIMS = (
    (".agents/skills/tree/tree.py", "scripts/dnl/tree.py"),
    (".agents/skills/dnl-query/dnl_query.py", "scripts/dnl/query.py"),
    (".agents/skills/dnl-builder/qa.py", "scripts/dnl/qa.py"),
    (".agents/skills/dnl-builder/dnl_util.py", "scripts/dnl/dnl_util.py"),
)


def deprecation_warning(legacy: str, canonical: str) -> str:
    return (
        f"[deprecated] {legacy} is a compatibility shim; "
        f"use {canonical} instead."
    )


def run_script(
    script: Path,
    *args: str,
    cwd: Path,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class CompatibilityShimTest(unittest.TestCase):
    def assert_matches_canonical(
        self,
        legacy: str,
        canonical: str,
        args: tuple[str, ...],
        *,
        cwd: Path,
    ) -> None:
        canonical_result = run_script(REPO_ROOT / canonical, *args, cwd=cwd)
        shim_result = run_script(REPO_ROOT / legacy, *args, cwd=cwd)

        self.assertEqual(shim_result.returncode, canonical_result.returncode)
        self.assertEqual(shim_result.stdout, canonical_result.stdout)
        self.assertEqual(
            shim_result.stderr,
            f"{deprecation_warning(legacy, canonical)}\n{canonical_result.stderr}",
        )

    def test_help_matches_canonical_for_all_four_shims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            for legacy, canonical in SHIMS:
                with self.subTest(legacy=legacy):
                    self.assert_matches_canonical(
                        legacy,
                        canonical,
                        ("--help",),
                        cwd=cwd,
                    )

    def test_representative_read_only_invocations_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cwd = root / "outside"
            cwd.mkdir()

            tree_root = root / "tree"
            tree_root.mkdir()
            (tree_root / "sample.md").write_text("# Sample\n", encoding="utf-8")

            query_root = root / "query"
            tag_index = query_root / ".agents/skills/dnl-query/tag-index"
            tag_index.mkdir(parents=True)
            (tag_index / "manifest.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "documents": 1,
                        "tags": {
                            "guide-dnl": {
                                "file": "tags/guide-dnl.jsonl",
                                "count": 1,
                            }
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            qa_root = root / "qa"
            qa_doc = qa_root / "docs/README.md"
            qa_doc.parent.mkdir(parents=True)
            qa_doc.write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: "Docs"
                    status: "draft"
                    tags: ["portal-dnl"]
                    paths: {}
                    ---

                    # Docs
                    """
                ),
                encoding="utf-8",
            )

            util_root = root / "util"
            util_root.mkdir()
            (util_root / "dnl-config.toml").write_text(
                '[scan]\ninclude = ["docs"]\nexclude = []\n',
                encoding="utf-8",
            )

            invocations = (
                (
                    SHIMS[0],
                    ("--root", str(tree_root), "--depth", "1", "--files", "--ascii"),
                ),
                (SHIMS[1], ("--root", str(query_root), "tags", "--format", "json")),
                (
                    SHIMS[2],
                    (
                        "--root",
                        str(qa_root),
                        "--include",
                        "docs",
                        "--fail-on",
                        "none",
                        "--report",
                        str(qa_root / "qa-report.md"),
                        "--json-summary",
                    ),
                ),
                (SHIMS[3], ("--root", str(util_root), "tag", "index", "check")),
            )

            for (legacy, canonical), args in invocations:
                with self.subTest(legacy=legacy):
                    self.assert_matches_canonical(
                        legacy,
                        canonical,
                        args,
                        cwd=cwd,
                    )

    def test_runpy_preserves_argv_cwd_stdin_stdout_stderr_and_exit(self) -> None:
        target_source = textwrap.dedent(
            """\
            import json
            import sys
            from pathlib import Path

            print(json.dumps({
                "argv": sys.argv,
                "cwd": str(Path.cwd()),
                "stdin": sys.stdin.read(),
                "path0": sys.path[0],
            }, ensure_ascii=False))
            print("target stderr", file=sys.stderr)
            raise SystemExit(7)
            """
        )

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            cwd = base / "outside"
            cwd.mkdir()
            for index, (legacy, canonical) in enumerate(SHIMS):
                with self.subTest(legacy=legacy):
                    synthetic_repo = base / f"repo-{index}"
                    (synthetic_repo / ".git").mkdir(parents=True)
                    legacy_script = synthetic_repo / legacy
                    canonical_script = synthetic_repo / canonical
                    legacy_script.parent.mkdir(parents=True)
                    canonical_script.parent.mkdir(parents=True)
                    shutil.copy2(REPO_ROOT / legacy, legacy_script)
                    canonical_script.write_text(target_source, encoding="utf-8")

                    completed = run_script(
                        legacy_script,
                        "alpha",
                        "café",
                        cwd=cwd,
                        input_text="stdin payload\n",
                    )

                    self.assertEqual(completed.returncode, 7)
                    payload = json.loads(completed.stdout)
                    self.assertEqual(
                        payload["argv"],
                        [str(canonical_script), "alpha", "café"],
                    )
                    self.assertEqual(Path(payload["cwd"]).resolve(), cwd.resolve())
                    self.assertEqual(payload["stdin"], "stdin payload\n")
                    self.assertEqual(payload["path0"], str(canonical_script.parent))
                    self.assertEqual(
                        completed.stderr,
                        (
                            f"{deprecation_warning(legacy, canonical)}\n"
                            "target stderr\n"
                        ),
                    )

    def test_missing_target_warns_then_returns_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            cwd = base / "outside"
            cwd.mkdir()
            for index, (legacy, canonical) in enumerate(SHIMS):
                with self.subTest(legacy=legacy):
                    synthetic_repo = base / f"repo-{index}"
                    (synthetic_repo / ".git").mkdir(parents=True)
                    legacy_script = synthetic_repo / legacy
                    legacy_script.parent.mkdir(parents=True)
                    shutil.copy2(REPO_ROOT / legacy, legacy_script)
                    missing_target = synthetic_repo / canonical

                    completed = run_script(legacy_script, "--help", cwd=cwd)

                    self.assertEqual(completed.returncode, 2)
                    self.assertEqual(completed.stdout, "")
                    self.assertEqual(
                        completed.stderr,
                        (
                            f"{deprecation_warning(legacy, canonical)}\n"
                            f"[error] {canonical} not found: {missing_target}\n"
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
