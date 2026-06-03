---
name: "PATHS.md Guide"
status: "draft"
tags: ["guide-dnl", "reference-dnl"]
description:
  - "This document explains how PATHS.md maps DNL tokens to real filesystem locations."
paths:
  "@local-context.md": "{@DNL-system}/ai/local-context/README.md"
---

# PATHS.md Guide

`PATHS.md` defines the real filesystem paths for DNL tokens such as `{@example-company}` or `{@sample-project}`.

## Why it matters

- Without `PATHS.md`, tokenized paths cannot be resolved.
- Agents cannot reliably locate repository-specific projects or tools.
- Link navigation becomes incomplete because the target paths are unknown.

## How to respond when `PATHS.md` is missing

1. Explain that the file is required for path resolution.
2. Ask for the local paths that should be mapped.
3. Offer a small starter template instead of asking for every path at once.
4. Keep the tone calm and practical.

## Starter template

```markdown
# example-company
- {@example-company} :: C:/Users/{username}/work/example-company
- {@example-company.docs} ::

# sample-product
- {@sample-product} :: C:/Users/{username}/work/sample-product
- {@sample-project} :: C:/Users/{username}/work/sample-product/sample-project
```

## Formatting notes

- Use `{@token} :: actual/path` lines.
- Windows-style paths are fine.
- Empty values are acceptable when the path is not known yet.
- Keep the file small and easy to update later.

## Related docs

- `@local-context.md`
