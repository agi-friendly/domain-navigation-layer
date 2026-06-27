---
name: "Context Loading Rules (3-Layer DNL)"
status: "draft"
tags: ["rule-dnl"]
paths:
  "@repo-AGENTS.md": "{@dnl-root}/AGENTS.md"
  "@dnl-system.md": "{@DNL-system}/README.md"
  "@local-context.md": "{@DNL-system}/ai/local-context/README.md"
  "@paths-md.md": "{@DNL-system}/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@DNL-system}/ai/local-context/current-user-md.md"
  "@dnl-builder.md": "{@DNL-system}/authoring/README.md"
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
---

# Context Loading Rules (3-Layer DNL)

This document explains how an agent should load context in a layered DNL repository.

Default flow:

1. Start from the repository `@repo-AGENTS.md`.
2. Read the system portal at `@dnl-system.md`.
3. Read repository-local context docs only when the task depends on path mapping or current-user handoff.
4. Load public reader docs only for public explanation, onboarding, or README/docs work.
5. Load deeper domain layers only after the target layer is known.

## Purpose

- Keep agents from loading everything at once.
- Prefer hierarchical navigation over random search.
- Keep public reader docs separate from AI operating docs.
- Make each opened document point to the next useful document.

## Required rules

- Do not read every document at once.
- Do not guess file paths that are not in the repository or local context.
- If the task is about DNL writing or cleanup, read the authoring docs first.
- If the task mentions `working`, DNL promotion, archive, lifecycle, or history cleanup, read workflow docs before opening target content.
- Treat `working/` as source material, not canonical DNL.
- If the task is about public-facing README/docs, load public docs for that task.
- If one layer answers the question, stop there.

## Recommended loading order

### AI entrypoint

- `@repo-AGENTS.md`

### System level

- `@dnl-system.md`
- `@dnl-builder.md`
- `@markdown-rule.md`
- `@yaml-frontmatter-rule.md`
- `@multi-dnl-authority.md`
- `@dnl-authoring-playbook.md`
- `@workflow-root.md` when the task involves working material, promotion, archive, lifecycle, or history
- `@working-authoring-rule.md` when creating, registering, or editing a working bundle
- `@working-to-dnl.md` when promoting or absorbing working material into canonical DNL
- `@working-to-archive.md` when deciding whether raw working bundles can move out of active paths

### Repository-local context

- `@local-context.md`
- `@paths-md.md`
- `@current-user-md.md`

### Optional domain layers

When a repository has deeper domain layers, use public-safe placeholder names in examples:

- `example-company`
- `sample-product`
- `sample-project`

## Output requirement

When summarizing work, list the documents actually read and label them by layer.

Example:

- [Entry] AGENTS.md
- [System] DNL-system/README.md
- [Docs] docs/index.md
- [Project] sample-project/README.md
