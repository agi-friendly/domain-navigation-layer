---
name: tree
description: python으로 트리 구조 분석 가이드 (Windows tree 명령어 대체)
---

# DNL Tree Generator

`.agents/skills/tree/tree.py` is a lightweight tree explorer for DNL navigation.
It prints directory and JSON views while respecting `.gitignore`.

## Common commands

> **Windows:** `python -X utf8 .agents/skills/tree/tree.py ...`
> **macOS/Linux:** `python3 .agents/skills/tree/tree.py ...`

```bash
# Folder structure only
python3 .agents/skills/tree/tree.py --root docs

# Include files
python3 .agents/skills/tree/tree.py --root docs --files

# Public docs exploration pattern
python3 .agents/skills/tree/tree.py --root docs --depth 3 --files --ascii
```

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

## Windows encoding note

If PowerShell garbles Korean or emoji text, always use `-X utf8`.

```powershell
python -X utf8 .agents/skills/tree/tree.py --root docs --files --depth 3 --ascii
```

## Details

See `.agents/skills/tree/README.md` for the full option list, output examples, and usage notes.
