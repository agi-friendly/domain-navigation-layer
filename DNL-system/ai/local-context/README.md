---
name: "Local Context Portal"
status: "draft"
tags: ["portal-dnl"]
description:
  - "This document points to repository-local context guides for path mapping and current-user handoff."
paths:
  "@paths-md.md": "{@DNL-system}/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@DNL-system}/ai/local-context/current-user-md.md"
---

# Local Context Portal

This portal groups repository-local context documents that help an agent work against the current checkout without guessing paths or user state.

These guides live under `DNL-system` so they can be managed as normal DNL documents.

## Read first

- `@paths-md.md` - how to define and maintain `PATHS.md`
- `@current-user-md.md` - how to draft or maintain `CURRENT_USER.md`

## When to use these docs

- Use them when a task depends on repository-local paths or the user's current assignment.
- Keep them separate from `.agents/skills`, which remain tool/runtime surface.
