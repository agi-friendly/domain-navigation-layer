---
name: "CURRENT_USER.md Guide"
status: "draft"
tags: ["guide-dnl", "reference-dnl"]
description:
  - "This document explains how to draft or maintain CURRENT_USER.md for repository-local handoff context."
paths:
  "@local-context.md": "{@DNL-system}/ai/local-context/README.md"
---

# CURRENT_USER.md Guide

`CURRENT_USER.md` helps an AI quickly understand the user's current state and active work.

- It is optional, but recommended.

## If `CURRENT_USER.md` is missing

If it is missing, the AI has two options:

1. If the AI already understands the user's workflow, it can draft a starter version or ask the user to confirm it.
2. If the AI does not understand the workflow yet, it can ask the user whether they want the AI to draft `CURRENT_USER.md`.

## When responding to the user

- Be friendly and practical.
- If the user declines, do not keep pushing the file.
- Briefly explain that `CURRENT_USER.md` helps the AI stay aligned on current work and reference projects.
- Include a starter template.

## Starter template

```markdown
# Area of responsibility
- {email, board, auth, etc.}

# Current work
- {v8 board admin page scaffolding}

# Working project
- {@sample-project}

# Reference projects
- Sample API reference
  - {@sample-backend}/src/main/java/com/example/sample/module/controller/
- Sample UI reference
  - {@sample-design-system}/packages/sample-web-styles/src/lib/components/sample/manager
```

## Related docs

- `@local-context.md`
