---
name: "DNL Tree Tool"
status: "draft"
tags: ["guide-dnl"]
paths: {}
---

# DNL Tree Tool

`scripts/dnl/tree.py` is a cross-platform directory tree helper for DNL navigation.
It produces compact text or JSON output, respects `.gitignore`, and extracts README titles so agents can scan a scoped map quickly.

## Installation

Python 3.10+ is recommended.
Install the optional dependency when accurate `.gitignore` matching matters.

Local install:

```bash
python3 -m pip install --upgrade --target scripts/dnl/.vendor -r scripts/dnl/requirements.txt
```

Global install:

```bash
python3 -m pip install --upgrade -r scripts/dnl/requirements.txt
```

The script auto-loads `scripts/dnl/.vendor`, `scripts/dnl/.deps`, and `scripts/dnl/vendor` when those directories exist.
Without `pathspec`, it uses a simpler fallback matcher and prints a warning.

## Quick Start

```bash
# Folder structure only.
python3 scripts/dnl/tree.py --root docs --depth 3 --ascii

# Include files, line counts, and README titles.
python3 scripts/dnl/tree.py --root docs --depth 3 --files --ascii

# JSON output for downstream scripts.
python3 scripts/dnl/tree.py --root docs --depth 3 --files --json

# Write UTF-8 output to a file.
python3 scripts/dnl/tree.py --root docs --depth 3 --files --ascii --out dnl-tree.txt
```

## DNL Usage Pattern

1. Start from the repository entrypoint and DNL routers.
2. Use `scripts/dnl/query.py` to narrow documents by metadata or link records when indexes are available.
3. Run `scripts/dnl/tree.py` only inside the narrowed subtree.
4. Open the selected portal, glossary, concept, rule, or runbook documents to confirm meaning.

Avoid broad root scans such as `--root .` unless the user explicitly asks for a repository-level map.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `--root PATH` | `.` | Directory to explore. |
| `--files` | `False` | Include files in the output. |
| `--depth N` | `5` | Maximum visible depth. Use `-1` for unlimited depth. |
| `--hidden` | `False` | Include hidden files and directories. |
| `--ignore PATTERN` | repeatable | Add an ignore pattern. |
| `--no-gitignore` | `False` | Disable `.gitignore`-based ignores. |
| `--no-readme-title` | `False` | Disable README H1/frontmatter title extraction. |
| `--json` | `False` | Print JSON instead of text. |
| `--ascii` | `False` | Force ASCII tree characters. |
| `--absolute-path` | `False` | Emit absolute paths. |
| `--out FILE` | none | Write output to a UTF-8 file. |

## Text Output Example

```text
docs/ [2 dirs, 3 files] # Documentation Portal
|-- concepts/ [0 dirs, 2 files]
|   |-- dnl.md [42 lines] # DNL Concept
|   `-- routing.md [31 lines] # Routing
|-- guides/ [0 dirs, 1 files]
|   `-- quick-start.md [28 lines] # Quick Start
`-- README.md [20 lines] # Documentation Portal
```

## Windows UTF-8

If PowerShell uses a legacy code page, enable Python UTF-8 mode:

```powershell
python -X utf8 scripts/dnl/tree.py --root docs --depth 3 --files --ascii
```

## Verification

```bash
python3 -m unittest discover -s tests/dnl
python3 scripts/dnl/tree.py --root DNL-system --depth 1 --files --ascii
```
