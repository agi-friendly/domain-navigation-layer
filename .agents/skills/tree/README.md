---
name: "DNL Tree Generator — Detailed Docs"
status: "draft"
tags: ["portal-dnl"]
paths: {}
---

# DNL Tree Generator — Detailed Docs

`.agents/skills/tree/tree.py` is a tree generator for DNL navigation.
It behaves the same on Windows/macOS/Linux and produces a lightweight tree/JSON output that respects `.gitignore`.

## Installation

Python 3.10+ recommended. Install dependencies once.

**Recommended (local install):**

```bash
# macOS/Linux
python3 -m pip install --upgrade --target .agents/skills/tree/.vendor -r .agents/skills/tree/requirements.txt

# Windows
python -m pip install --upgrade --target .agents/skills/tree/.vendor -r .agents/skills/tree/requirements.txt
```

`tree.py` auto-loads `.vendor` at runtime, so it works without any separate activation.

**Global install (optional):**

```bash
python3 -m pip install -r .agents/skills/tree/requirements.txt
```

Without `pathspec` it falls back to a simpler matching, so installing it is recommended when `.gitignore` accuracy matters.

## Options

| Option | Default | Description |
|------|--------|------|
| `--root PATH` | `.` | Path to start exploring from |
| `--files` | `False` | Include files as well |
| `--depth N` | `5` | Maximum depth (`-1` for unlimited) |
| `--hidden` | `False` | Include hidden files/folders |
| `--ignore PATTERN` | repeatable | Additional exclude pattern |
| `--no-gitignore` | `False` | Disable `.gitignore`-based exclusion |
| `--no-readme-title` | `False` | Disable README H1 extraction |
| `--json` | `False` | JSON-mode output |
| `--ascii` | `False` | Force tree lines to ASCII |
| `--absolute-path` | `False` | Output absolute paths |
| `--out FILE` | none | Save to a UTF-8 file |

## Output example (text)

```text
domain-navigation-layer/ [3 dirs, 0 files]
├── docs/ [0 dirs, 4 files]
│   ├── README.md [23 lines] # public landing page
│   └── core-concept.md [17 lines]
├── DNL-system/ [1 dirs, 0 files]
│   └── authoring/ [1 dirs, 2 files]
└── .agents/skills/ [1 dirs, 0 files]
    └── tree/ [0 dirs, 4 files]
```

## Output example (JSON)

```json
{
  "name": "domain-navigation-layer",
  "path": ".",
  "type": "dir",
  "children": [
    {
      "name": "README.md",
      "path": "README.md",
      "type": "file",
      "readme_title": "Domain Navigation Layer",
      "lines": 23,
      "size": 1024,
      "children": []
    }
  ],
  "num_dirs": 0,
  "num_files": 1
}
```

## DNL usage tips

Providing the tree output alongside the prompt lets the AI quickly route to only the documents it needs.

```bash
python3 .agents/skills/tree/tree.py --root docs --files --depth 3 > dnl-tree.txt
# Paste the tree into the prompt when you want the agent to pick the relevant docs quickly.
```

## Smoke test

```bash
python3 .agents/skills/tree/test_tree.py
```

## Windows encoding details

When PowerShell's default encoding is cp949, printing a tree that contains Korean or emoji raises an error:

```text
UnicodeEncodeError: 'cp949' codec can't encode character ...
```

**Recommended:** run with the `-X utf8` flag

```powershell
python -X utf8 .agents/skills/tree/tree.py --root docs --files --depth 3 --ascii
```

**Session-level alternative:**

```powershell
$env:PYTHONUTF8 = "1"
python .agents/skills/tree/tree.py --root docs --files --depth 3 --ascii
```

**If `Get-Content` is also garbled:**

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Raw -Encoding UTF8 "path\to\file"
```
