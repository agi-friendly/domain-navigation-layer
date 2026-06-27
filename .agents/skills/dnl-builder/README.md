---
name: ".agents/skills/dnl-builder"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-util.py": "{@dnl-root}/.agents/skills/dnl-builder/dnl_util.py"
  "@dnl-config.toml": "{@dnl-root}/dnl-config.toml"
---

# .agents/skills/dnl-builder

This directory is the executable support surface for DNL document work.
The canonical rules live in `DNL-system/authoring` and `DNL-system/workflow`.
This skill routes agents there and provides QA/index utilities.

## Role

- Route DNL document work to canonical authoring rules
- Route working/promotion/archive work to workflow rules
- Run `@qa.py` for DNL document quality checks
- Run `@dnl-util.py` for bulk tag and index maintenance
- Provide a stable entrypoint for multiple agent environments

## Steward posture

Good DNL work is mostly route maintenance.

When a new canonical document is written, check that parent README files, maps, guides, and cross-links lead there.
Do not leave raw `working/` material looking like the current source of truth after promotion.

Keep portal documents light.
If a document is growing because it contains investigation notes, comparison tables, or decision background, split that material into load-on-demand documents.

Promoting `working/` material into DNL is a lifecycle change, not just a writing task.
Read `DNL-system/workflow/README.md` and `DNL-system/workflow/working-to-dnl.md` together with authoring rules.

## Recommended reading order

1. `DNL-system/authoring/README.md`
2. `DNL-system/authoring/rules/markdown-rule.md`
3. `DNL-system/authoring/rules/yaml-frontmatter-rule.md`
4. `DNL-system/authoring/rules/multi-dnl-authority.md`
5. `DNL-system/authoring/dnl-authoring-playbook.md`
6. `DNL-system/workflow/README.md`
7. If the work includes `working`, `working-to-dnl`, promotion, archive, or history cleanup: `DNL-system/workflow/working-to-dnl.md`
8. If archive movement is involved: `DNL-system/workflow/working-to-archive.md`
9. `.agents/skills/dnl-builder/README.md`

## Recommended routine

1. Decide whether the task is DNL document maintenance.
2. Read canonical rules first.
3. If working material is being promoted, apply the `working-to-dnl` checklist.
4. Decide the target document role: router, canonical guide, background, working source material, or archive.
5. Edit the target document.
6. Rewire parent README files, maps, guides, and cross-links.
7. Search semantic stale text: old paths, old priority wording, raw working bundles treated as current truth, or completion claims without navigation.
8. Run QA and inspect the report when needed.

## dnl-config.toml

`@dnl-config.toml` is the shared project map for dnl-builder tools.

- `qa.py --profile full` uses `scan.include` and `scan.exclude`.
- `qa.py --profile portal` uses `profiles.portal` and `portal.readme_dirs`.
- tag index commands use the configured scan surface.
- link index commands use the configured scan surface and path variables.
- required tag checks use `tags.required_by_filename` and `tags.required_by_path`.

`dnl-config.toml` does not define DNL policy.
YAML required fields, field order, allowed statuses, tag/token formats, hidden-directory behavior, and `SKILL.md` exclusion are defined by tool code and DNL-system authoring rules.

## QA

Common commands:

```bash
python3 .agents/skills/dnl-builder/qa.py
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all
python3 .agents/skills/dnl-builder/qa.py --profile links
python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary
```

Useful options:

```text
--fail-on none|low|med|high|all
--json-summary
```

Report path:

```text
.agents/skills/dnl-builder/reports/qa-report.md
```

The report directory is gitignored.

QA checks include:

- YAML frontmatter required fields
- YAML field order, status, tag, and path formats
- required tags from `dnl-config.toml`
- portal README path declarations
- `## HUMAN_LINKS` sections
- `- [HUMAN_LINK]` lines
- local Markdown file/folder links in canonical DNL docs
- deep relative links such as `../../`
- best-effort broken local links
- link-index health counts for unresolved, unused, and missing token candidates

## DNL utility

`@dnl-util.py` supports bulk maintenance.
It defaults to dry-run for write operations.

Examples:

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs --tag guide-dnl --recursive
python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs --tag guide-dnl --recursive --write
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py tag index check
python3 .agents/skills/dnl-builder/dnl_util.py tag index update --path docs/index.md
python3 .agents/skills/dnl-builder/dnl_util.py link index build
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```

Generated tag and link indexes are local build artifacts.
Do not commit `.agents/skills/dnl-query/tag-index/` or `.agents/skills/dnl-query/link-index/`.

## Link health workflow

```bash
python3 .agents/skills/dnl-builder/dnl_util.py link index build
python3 .agents/skills/dnl-builder/dnl_util.py link index check
python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary
python3 .agents/skills/dnl-query/dnl_query.py unresolved --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --format jsonl
```

`unresolved` and `missing-tokens` are often real route problems.
`unused` can be intentional in portal documents, so review before changing policy.
