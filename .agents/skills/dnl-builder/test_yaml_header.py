from __future__ import annotations

import unittest

from yaml_header import (
    extract_frontmatter,
    parse_dnl_header,
    parse_legacy_path_entries,
)


class DnlYamlHeaderTest(unittest.TestCase):
    def test_parse_name_and_paths_map(self) -> None:
        text = """---
name: "Workflow"
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
---

# Workflow
"""

        header = parse_dnl_header(text)

        self.assertEqual(header.name, "Workflow")
        self.assertEqual(
            header.paths,
            {
                "@workflow-root.md": "{@DNL-system}/workflow/README.md",
                "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md",
            },
        )
        self.assertEqual(header.errors, [])

    def test_parse_status_tags_and_description(self) -> None:
        text = """---
name: "Workflow"
status: "draft"
tags: ["portal-dnl", "workflow"]
description:
  - "이 문서는 DNL 작업 흐름을 설명한다."
  - "AI가 future 문서를 정본 DNL로 승격할 때 참고한다."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
---

# Workflow
"""

        header = parse_dnl_header(text)

        self.assertEqual(getattr(header, "status", None), "draft")
        self.assertEqual(getattr(header, "tags", None), ["portal-dnl", "workflow"])
        self.assertEqual(
            getattr(header, "description", None),
            [
                "이 문서는 DNL 작업 흐름을 설명한다.",
                "AI가 future 문서를 정본 DNL로 승격할 때 참고한다.",
            ],
        )
        self.assertEqual(header.errors, [])

    def test_report_invalid_yaml_frontmatter_rules(self) -> None:
        text = """---
name: "Workflow"
description:
  - "description은 status와 tags 뒤에 위치해야 한다."
status: "review"
tags: ["Portal-DNL", "bad tag", "portal-dnl", "portal-dnl"]
paths:
  "workflow-root.md": "{@DNL-system}/workflow/README.md"
---

# Workflow
"""

        header = parse_dnl_header(text)

        self.assertIn("status must be one of active, draft, deprecated on line 4", header.errors)
        self.assertIn("frontmatter field order must be name, status, tags, description, paths", header.errors)
        self.assertIn("tag must match ^[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?$ on line 5: Portal-DNL", header.errors)
        self.assertIn("tag must match ^[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?$ on line 5: bad tag", header.errors)
        self.assertIn("duplicate tag found on line 5: portal-dnl", header.errors)
        self.assertIn("paths key must start with @ on line 7: workflow-root.md", header.errors)

    def test_extract_frontmatter_returns_body_without_header(self) -> None:
        text = """---
name: "Workflow"
---

# Workflow
"""

        frontmatter, body = extract_frontmatter(text)

        self.assertEqual(frontmatter, 'name: "Workflow"')
        self.assertEqual(body, "\n# Workflow\n")

    def test_horizontal_rule_at_file_start_is_not_frontmatter(self) -> None:
        text = """---

# Document

---

content
"""

        frontmatter, body = extract_frontmatter(text)

        self.assertIsNone(frontmatter)
        self.assertEqual(body, text)

    def test_paths_list_is_reported_as_error(self) -> None:
        text = """---
name: "Workflow"
paths:
  - "@workflow-root.md: {@DNL-system}/workflow/README.md"
---
"""

        header = parse_dnl_header(text)

        self.assertEqual(header.paths, {})
        self.assertEqual(
            header.errors,
            ["paths must be a map of quoted token/path pairs; list item found on line 3"],
        )

    def test_empty_inline_paths_map_is_supported(self) -> None:
        text = """---
name: "Workflow"
paths: {}
---
"""

        header = parse_dnl_header(text)

        self.assertEqual(header.name, "Workflow")
        self.assertEqual(header.paths, {})
        self.assertEqual(header.errors, [])

    def test_parse_legacy_single_line_path_entries(self) -> None:
        lines = [
            "- [PATH] `@workflow-root.md` : {@DNL-system}/workflow/README.md",
            "- [PATH] `@future-to-dnl.md` : {@DNL-system}/workflow/future-to-dnl.md",
            "",
            "# Workflow",
        ]

        entries = parse_legacy_path_entries(lines)

        self.assertEqual(
            [(entry.token, entry.path, entry.line_index, entry.multiline) for entry in entries],
            [
                ("@workflow-root.md", "{@DNL-system}/workflow/README.md", 0, False),
                ("@future-to-dnl.md", "{@DNL-system}/workflow/future-to-dnl.md", 1, False),
            ],
        )

    def test_parse_legacy_multiline_path_entry_without_path(self) -> None:
        lines = [
            "- [PATH] `@sample-company`",
            "  - {@sample-company}",
            "---",
        ]

        entries = parse_legacy_path_entries(lines)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].token, "@sample-company")
        self.assertEqual(entries[0].path, "")
        self.assertTrue(entries[0].multiline)


if __name__ == "__main__":
    unittest.main()
