---
name: "Document Selection Rules (3-Layer Routing Strategy)"
status: "draft"
tags: ["rule-dnl"]
paths:
  "@dnl-builder.md": "{@DNL-system}/authoring/README.md"
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
  "@future-to-archive.md": "{@DNL-system}/workflow/future-to-archive.md"
---

# Document Selection Rules (3-Layer Routing Strategy)

This document defines how an agent should choose the next document in a layered DNL repository.
The goal is to route from a small set of high-signal pages instead of scanning the entire tree.

## Core principles

- Start with the repository AI entrypoint and system portal.
- Load the system/authoring docs only when the task is about DNL maintenance.
- Load workflow docs when the prompt mentions `future`, promotion into DNL, archive, lifecycle, or history cleanup.
- Load public reader docs when the task is about README, docs, onboarding, or public explanation.
- Load deeper domain docs only after the target layer is known.
- Stop and ask a clarifying question when the layer is unclear.

## Routing order

### 1. AI entrypoint and system portal

1. `AGENTS.md`
2. `DNL-system/README.md`
3. `DNL-system/ai/README.md` when the task is about agent behavior

### 1A. Workflow / future / archive signal

When the prompt includes any of these signals, read workflow before opening lower-level domain docs:

- `workflow`
- `future`
- `archive`
- `history`
- `promote into DNL`
- `absorb future material`
- `move raw work bundle`

Read in this order:

1. `DNL-system/workflow/README.md`
2. `DNL-system/workflow/future-to-dnl.md` when promotion or absorption is involved
3. `DNL-system/workflow/future-to-archive.md` when archive movement is involved

This is a lifecycle question first. The target domain layer comes after the workflow rule is fixed.

### 2. Public docs when relevant

Use reader-facing public docs when the prompt is about repository presentation, onboarding, GitHub-facing documentation, or docs content:

- `README.md`
- `docs/index.md`

### 3. Layer discovery

If the repository has deeper domain layers, route by the strongest signal first:

- Product or domain name in the prompt
- File path already open in the editor
- Explicit module, feature, or screen name
- Bug, feature, refactor, or doc intent

### 4. Optional deeper layers

When a repository uses company/product/project layers, use placeholder names in examples:

- `example-company/README.md`
- `sample-product/README.md`
- `sample-project/README.md`

## Ambiguity handling

When the layer is unclear, ask one narrow question instead of searching broadly.

Example:

- "Is this about the public docs, the system rules, or a specific project layer?"

## Forbidden behavior

- Do not scan every file in the repository.
- Do not assume a missing path exists.
- Do not mix unrelated layers when one layer already answers the question.
- Do not treat `future` notes as canonical DNL until `@future-to-dnl.md` criteria are satisfied.

## Summary

Portal first. Layer down only when the prompt gives enough signal. Stop before recursion.
