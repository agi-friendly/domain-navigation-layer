---
name: "DNL Tooling"
status: "draft"
tags: ["guide-dnl"]
paths: {}
---

# DNL Tooling

`scripts/dnl` is the official portable runtime and detailed-guide surface for
DNL tooling used by people and agents.

## Official tools

| Role | Executable | Guide |
| --- | --- | --- |
| Scoped tree view | [`scripts/dnl/tree.py`](tree.py) | [`scripts/dnl/tree.md`](tree.md) |
| Generated-index query | [`scripts/dnl/query.py`](query.py) | [`scripts/dnl/query.md`](query.md) |
| Repository QA | [`scripts/dnl/qa.py`](qa.py) | [`scripts/dnl/qa.md`](qa.md) |
| DNL maintenance | [`scripts/dnl/dnl_util.py`](dnl_util.py) | [`scripts/dnl/dnl_util.md`](dnl_util.md) |

`tree.py` and `query.py` are read-only. `qa.py` validates source without
editing it. `dnl_util.py` includes write-capable tag and move commands, so read
its safety guide before applying changes.

## Requirements

Python 3.11 or newer is required. `tree.py` can optionally use the dependency
listed in `scripts/dnl/requirements.txt` for complete `.gitignore` matching.

## Generated runtime state

Source ownership does not change the existing ignored runtime-state locations:

- tag and link indexes: `.agents/skills/dnl-query/{tag-index,link-index}/`
- QA report: `.agents/skills/dnl-builder/reports/qa-report.md`

## Compatibility

Retained executable paths under `.agents/skills` are temporary compatibility
shims for older automation and agent memory. They warn on stderr and delegate
to the canonical scripts. New documentation and commands must use
`scripts/dnl`.

## Windows UTF-8

Use Python UTF-8 mode when needed:

```powershell
python -X utf8 scripts/dnl/qa.py --help
```
