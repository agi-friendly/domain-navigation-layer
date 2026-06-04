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
---

# Document Selection Rules (3-Layer Routing Strategy)

This document defines how an agent should choose the next document in a layered DNL repository.
The goal is to route from a small set of high-signal pages instead of scanning the entire tree.

## Core principles

- Start with the repository landing page and docs index.
- Load the system/authoring docs only when the task is about DNL maintenance.
- Load deeper domain docs only after the target layer is known.
- Stop and ask a clarifying question when the layer is unclear.

## Routing order

### 1. Repository and docs

1. `README.md`
2. `docs/index.md`
3. `DNL-system/README.md` when the task is about rules or maintenance

### 2. Layer discovery

If the repository has deeper domain layers, route by the strongest signal first:

- Product or domain name in the prompt
- File path already open in the editor
- Explicit module, feature, or screen name
- Bug, feature, refactor, or doc intent

### 3. Optional deeper layers

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

## Summary

Portal first. Layer down only when the prompt gives enough signal. Stop before recursion.
