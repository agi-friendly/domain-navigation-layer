---
name: "Example code map"
status: "draft"
tags: ["map-dnl", "auth", "example-dnl"]
description:
  - "This document maps the example auth route to likely source entrypoints."
  - "The paths are illustrative and should be replaced with real project paths when adapting the example."
paths:
  "@auth.md": "{@DNL-example}/domains/auth.md"
  "@login-callback.md": "{@DNL-example}/runbooks/login-callback.md"
---

# Example code map

Use this after reading `@auth.md` and `@login-callback.md`.

## Likely source entrypoints

These are example source paths for a small web app:

```text
src/routes/auth/
src/services/session/
tests/auth/
```

Replace them with real paths from your project before relying on the route.

## How to use this map

Start with the route handler, then inspect session creation, then check tests or fixtures.

Do not search the whole repository until these entrypoints have been checked.
