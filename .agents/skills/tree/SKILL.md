---
name: tree
description: Use when an agent needs a cross-platform directory tree view after narrowing the DNL search area.
---

# DNL Tree Tool

Use this skill when a candidate DNL area is already narrowed and you need a quick directory map.
The executable tool is `scripts/dnl/tree.py`; the detailed guide is `scripts/dnl/tree.md`.
The retained executable in this skill directory is a compatibility shim only.

## Common Commands

```bash
# Folder structure only.
python3 scripts/dnl/tree.py --root docs --depth 3 --ascii

# Include files and line counts.
python3 scripts/dnl/tree.py --root DNL-system --depth 2 --files --ascii

# JSON output for downstream scripts.
python3 scripts/dnl/tree.py --root docs --depth 3 --files --json
```

## Usage Boundary

- Narrow the search first with DNL routing or `dnl-query`.
- Run tree only inside the narrowed subtree.
- Use `--depth 3` to `--depth 5` for normal exploration.
- Do not start with broad repository-wide trees unless the user explicitly asks for a repository map.

Read `scripts/dnl/tree.md` for installation, options, output examples, and Windows UTF-8 notes.
