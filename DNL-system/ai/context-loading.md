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
---

# Context Loading Rules (3-Layer DNL)

This document explains how an agent should load context in a layered DNL repository.
The default flow is:

1. Start from the repository `@repo-AGENTS.md`.
2. Read the system/maintenance portal at `@dnl-system.md`.
3. Read repository-local context docs when the task depends on path mappings or current-user handoff.
4. Load public reader docs only when the task asks about public explanation, onboarding, or README/docs content.
5. Load company, product, or project docs only after the target layer is known.

## Purpose

- Keep the agent from loading too much at once.
- Force hierarchical navigation instead of random search.
- Keep reader-facing public docs separate from AI operating docs.
- Make the next document obvious before opening the current one.

## Required rules

- Do not read every document at once.
- Do not guess file paths that are not in the repo or `PATHS.md`.
- If the task is about DNL writing or cleanup, read the system authoring docs first.
- If the task is about public-facing README/docs, load the public docs for that task.
- If the task is about a specific layer, stop at the first layer that answers the question.

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

### Repository-local context

- `@local-context.md`
- `@paths-md.md`
- `@current-user-md.md`

### Optional domain layers

When a repository has deeper domain layers, use placeholder names such as `example-company`, `sample-product`, and `sample-project` in examples.

## Output requirement

When you summarize your work, list the documents you actually read and label them by layer.

Example:

- [Entry] AGENTS.md
- [System] DNL-system/README.md
- [Docs] docs/index.md
- [Project] sample-project/README.md
