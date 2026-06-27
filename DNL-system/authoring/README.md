---
name: "DNL authoring portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@rules/README.md": "{@DNL-system}/authoring/rules/README.md"
  "@rules/markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@rules/yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@rules/multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
  "@dnl-config.toml": "{@dnl-root}/dnl-config.toml"
  "@qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-util.py": "{@dnl-root}/.agents/skills/dnl-builder/dnl_util.py"
---

# DNL authoring portal

This directory is the source of truth for writing and maintaining canonical DNL documents.

Use `DNL-system/ai` for how agents load context.
Use this directory for how DNL documents are written, validated, and kept coherent.

## Recommended reading order

1. Writing rules: `@rules/README.md` -> `@rules/markdown-rule.md` -> `@rules/yaml-frontmatter-rule.md`
2. Authority and overrides: `@rules/multi-dnl-authority.md`
3. Practical writing flow: `@dnl-authoring-playbook.md`
4. If the work includes `working/` material, DNL promotion, archive, or history decisions: `@workflow-root.md` -> `@working-to-dnl.md` -> when needed `@working-to-archive.md`

## Steward lens

A DNL author is responsible for navigation quality, not only local wording.

Good DNL work:

- keeps README and portal documents light
- puts current truth and next routes in default documents
- moves long background, comparisons, and decision history into load-on-demand documents
- does not present `working/` source material as canonical DNL
- rewires parent routes after promotion
- checks semantic stale text after QA passes

Authoring rules define the shape of canonical DNL documents.
Workflow rules define the lifecycle of source material moving through `working -> DNL -> archive`.

Both are required when promoting working material.

## Recommended routine

1. Decide the target layer: System, shared/team, product/domain, or project.
2. If the task promotes or archives working material, apply `@working-to-dnl.md` first.
3. Decide the document role: router, canonical guide, background note, working source material, or archive.
4. Edit the document according to authoring rules.
5. Rewire parent README, maps, guides, and cross-links.
6. Search for semantic stale text: old paths, old priority wording, raw working references treated as current truth, or completion claims without navigation.
7. Run QA:
   - `python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all`
   - `python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all`
   - `python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary`

## dnl-config.toml boundary

`@dnl-config.toml` is the shared project map used by DNL tooling.

It controls:

- scan roots
- excluded folders
- path variables
- QA profiles
- required tag rules

It does not define DNL policy.

YAML required fields, field order, allowed statuses, tag/token formats, hidden-directory behavior, and `SKILL.md` exclusion are defined by tool code and `@rules/yaml-frontmatter-rule.md`.

## Utilities

- `@dnl-util.py`: utility entrypoint for bulk DNL maintenance
- Add a tag, dry-run:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs/sample-dnl/sample-module --tag sample-module --recursive`
- Add a tag, write:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs/sample-dnl/sample-module --tag sample-module --recursive --write`
- Rebuild tag index:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index build`
- Check tag index freshness:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index check`
- Rebuild link index:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index build`
- Check link index freshness:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index check`
- Update one tag-index file:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index update --path docs/sample-dnl/sample-module/README.md`

## Link health routine

Link health is an observation signal before it is a hard gate.

Use this flow:

1. Rebuild link index.
   - `python3 .agents/skills/dnl-builder/dnl_util.py link index build`
2. Check index freshness.
   - `python3 .agents/skills/dnl-builder/dnl_util.py link index check`
3. Read the health summary.
   - `python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary`
4. Narrow suspicious areas.
   - `python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary`
5. Inspect detailed candidates.
   - `python3 .agents/skills/dnl-query/dnl_query.py unresolved --format jsonl`
   - `python3 .agents/skills/dnl-query/dnl_query.py unused --format jsonl`
   - `python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --format jsonl`

Currently `unresolved`, `unused`, and `missing-tokens` are health signals.
Review them before deciding whether a policy change or document cleanup is needed.
