---
name: "ai - AI operating portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@context-loading.md": "context-loading.md"
  "@doc-selection-rules.md": "doc-selection-rules.md"
  "@output-format.md": "output-format.md"
  "@guardrails.md": "guardrails.md"
  "@prompt-playbook.md": "prompt-playbook.md"
  "@local-context.md": "{@DNL-system}/ai/local-context/README.md"
  "@paths-md.md": "{@DNL-system}/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@DNL-system}/ai/local-context/current-user-md.md"
  "@dnl-builder.md": "{@DNL-system}/authoring/README.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
---

# ai - AI operating portal

This directory holds operating rules for AI agents using a DNL repository.

## Recommended reading order

1. `@context-loading.md` - how to load only the needed context
2. `@doc-selection-rules.md` - how to choose the next document
3. `@output-format.md` - how to report findings and evidence
4. `@guardrails.md` - global safety boundaries

## Repository-local context

Repository-local path and user handoff notes live under `ai/local-context/`.

- `@local-context.md`
- `@paths-md.md`
- `@current-user-md.md`

## DNL authoring route

When the prompt is about DNL writing or cleanup, route through authoring before editing target documents.

Signals include:

- DNL improvement
- documentation
- README cleanup
- YAML `paths`
- `@tokens`
- local Markdown link cleanup
- route improvement
- `dnl-builder`
- `working`, `working-to-dnl`, promotion, archive, or history cleanup

Read in this order:

1. `@dnl-builder.md`
2. `@markdown-rule.md`
3. `@yaml-frontmatter-rule.md`
4. `@multi-dnl-authority.md`
5. `@dnl-authoring-playbook.md`
6. If the work includes working lifecycle decisions, read `@workflow-root.md`, then choose the specific rule:
   - creating, registering, or editing a working bundle: `@working-authoring-rule.md`
   - promoting or absorbing working material into canonical DNL: `@working-to-dnl.md`
   - moving completed raw bundles out of active paths: `@working-to-archive.md`
7. The document that will actually be changed

Purpose: do not treat DNL maintenance as ordinary source search. First fix the authoring rules, authority model, and lifecycle boundary.

## Project-level AI overrides

A project DNL may add an `ai/` directory, but global rules still live here.

Use this pattern:

1. Project `ai/README.md` states that the global source of truth is `DNL-system/ai`.
2. Project `ai/overrides.md` contains only project-specific additions or exceptions.
3. Every exception must be explicit.

Example:

```md
Override:
For this project only, load DNL/apis/README.md before DNL/screens/README.md when the task is about API-driven screens.
```

If no explicit override exists, the DNL-system rule wins.
