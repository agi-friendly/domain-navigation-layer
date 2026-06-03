---
name: "Prompt Playbook (Intent Recognition Strategy)"
status: "draft"
tags: ["playbook-dnl"]
paths: {}
---

# Prompt Playbook (Intent Recognition Strategy)

This document explains how to turn an ambiguous prompt into a specific task in a layered DNL repository.

## Purpose

- Identify the target layer before searching broadly.
- Distinguish between documentation work, maintenance work, and project work.
- Ask a narrow follow-up question when the layer is unclear.

## Signal extraction

Look for these signals first:

### Repository signal

- The prompt mentions the repository itself, its landing page, or its docs index.

### System signal

- The prompt mentions DNL rules, authoring, workflow, or guardrails.

### Domain signal

- The prompt mentions a product, module, feature, screen, or project folder.

## Task classification

| Task type | Typical keywords | First place to look |
| --- | --- | --- |
| Bug analysis | broken, error, failing, regression | runbooks or troubleshooting docs |
| Exploration | where, structure, explain | docs/index.md |
| Feature | add, change, build | the specific project docs |
| Refactoring | clean up, split, simplify | the specific project docs |
| Test | reproduce, test case | test or runbook docs |
| Doc generation | write docs, README, guide | output-format.md |

## Ambiguity handling

If the prompt does not name a layer, ask one short question.

Examples:

- "Is this about the public docs, the system rules, or a specific project layer?"
- "Which folder or module should I treat as the target?"

## Routing examples

| Prompt shape | First target |
| --- | --- |
| "Explain the docs layout" | `docs/index.md` |
| "How do the rules work?" | `DNL-system/README.md` |
| "Where should I put project notes?" | `docs/` or the relevant project folder |
| "Write a DNL guide" | `DNL-system/authoring/README.md` |

## Forbidden reactions

- Do not answer with "not enough information" and stop there.
- Do not guess a layer when the prompt does not give one.
- Do not scan the whole repository first.

## Final principle

Filter signals, clarify context, then route the task.
