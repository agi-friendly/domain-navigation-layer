---
name: dnl-builder
description: Route DNL document work through DNL-system authoring/workflow rules, then run QA.
---

# DNL Builder

This skill is not only a wrapper around `.agents/skills/dnl-builder/qa.py`.
It is a bridge that sends agents to the canonical DNL-system authoring and workflow rules before they edit DNL documents.

## Steward posture

Act as a steward of the whole navigation layer, not only as the editor of one file.

- Check whether parent README files, maps, and guides route to the new canonical document.
- Keep portal documents light: current truth and next routes only.
- Move long background, investigations, and decision notes into load-on-demand documents when needed.
- Treat `working/` as source material, not canonical DNL.
- After promotion, active DNL should not treat raw working bundles as the priority path.
- If the task includes `working`, promotion, archive, or history cleanup, read workflow docs as well as authoring docs and choose the matching lifecycle rule.
- Do not stop at green QA. Search semantic stale text such as old paths, old priority wording, or missing parent routes.

## Use this skill first when

- creating a DNL document
- editing or refactoring a DNL document
- changing README routing
- editing YAML frontmatter, `paths`, or `@tokens`
- removing local Markdown file links or `HUMAN_LINK` patterns from canonical DNL docs
- checking DNL document quality after edits

## Required reading order

1. `DNL-system/authoring/README.md`
2. `DNL-system/authoring/rules/markdown-rule.md`
3. `DNL-system/authoring/rules/yaml-frontmatter-rule.md`
4. `DNL-system/authoring/rules/multi-dnl-authority.md`
5. `DNL-system/authoring/dnl-authoring-playbook.md`
6. `DNL-system/workflow/README.md`
7. If the work creates, registers, or edits a working bundle: `DNL-system/workflow/working-authoring-rule.md`
8. If the work promotes or absorbs working material into canonical DNL: `DNL-system/workflow/working-to-dnl.md`
9. If archive movement is involved: `DNL-system/workflow/working-to-archive.md`
10. When needed: `.agents/skills/dnl-builder/README.md`

## Basic workflow

1. Read canonical authoring and workflow rules.
2. Narrow the target layer and document role.
3. If promoting working material, apply the `working-to-dnl` checklist first.
4. Edit the target DNL document.
5. Rewire parent README, maps, guides, and cross-links.
6. Search for semantic stale text.
7. Run QA.

## QA commands

macOS/Linux:

```bash
python3 .agents/skills/dnl-builder/qa.py
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all
```

Windows:

```bash
python -X utf8 .agents/skills/dnl-builder/qa.py
```

Report path:

```text
.agents/skills/dnl-builder/reports/qa-report.md
```

The report directory is gitignored.

## Common utilities

```bash
# Dry-run one-document DNL markdown move
python3 .agents/skills/dnl-builder/dnl_util.py mv --path docs/old.md --to docs/reference

# Move the file and rewrite backlink YAML paths
python3 .agents/skills/dnl-builder/dnl_util.py mv --path docs/old.md --to docs/reference --write
```

`mv` supports one `.md` file at a time.
`--to` must be an existing DNL directory.
Directory creation and rename targets are not supported.
The command accepts repo-relative paths and `[paths.internal]` token paths.
It rejects sources with local Markdown links or images because asset movement is not automated.

## More details

- Workflow and quality guide: `.agents/skills/dnl-builder/README.md`
- Canonical writing rules: `DNL-system/authoring/`
