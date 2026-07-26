---
name: dnl-query
description: Use when an agent needs to find DNL documents by metadata or link records without editing DNL content.
---

# DNL Query

Use this skill when you need to locate DNL documents quickly without scanning every Markdown file by hand.
The executable tool is `scripts/dnl/query.py`; the detailed guide is `scripts/dnl/query.md`.

## Common Commands

```bash
# List tags and counts.
python3 scripts/dnl/query.py tags

# List documents for a tag.
python3 scripts/dnl/query.py docs --tag glossary-dnl

# Print paths only for follow-up reading.
python3 scripts/dnl/query.py docs --tag rule-dnl --format paths

# Inspect one document's outbound links and backlinks.
python3 scripts/dnl/query.py deps --path DNL-system/README.md --format json
```

## Role Boundary

- Find DNL documents and link records: `scripts/dnl/query.py`
- Read the full query guide: `scripts/dnl/query.md`
- Inspect nearby directory structure after narrowing candidates: `scripts/dnl/tree.py`
- Build or refresh indexes, edit DNL, or run QA: `.agents/skills/dnl-builder`

The retained executable in this skill directory is a compatibility shim only.
