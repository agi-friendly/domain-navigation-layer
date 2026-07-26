---
name: "DNL QA Tool"
status: "draft"
tags: ["guide-dnl"]
paths: {}
---

# DNL QA Tool

`scripts/dnl/qa.py` validates DNL frontmatter, structure, routing, and link
health without editing source documents.

## Quick start

```bash
python3 scripts/dnl/qa.py --profile portal --fail-on all
python3 scripts/dnl/qa.py --profile full --fail-on all
```

## Profiles

| Profile | Purpose |
| --- | --- |
| `portal` | Validate configured portal documents. |
| `full` | Validate the complete configured DNL scan. |
| `links` | Focus on link-related checks. |
| `health` | Report generated link-index health without source scanning. |

## Failure policy

`--fail-on all` fails on any finding. `low`, `med`, and `high` select the
minimum failing severity. `none` reports findings without a failing exit.

## Reports and machine-readable output

```bash
python3 scripts/dnl/qa.py --profile full \
  --report .agents/skills/dnl-builder/reports/qa-report.md
python3 scripts/dnl/qa.py --profile portal --fail-on all --json-summary
```

The default report is ignored runtime state. With `--json-summary`, JSON
replaces the normal short status summary on stdout.

## Windows UTF-8

```powershell
python -X utf8 scripts/dnl/qa.py --profile portal --fail-on all
```
