---
name: "DNL example project"
status: "draft"
tags: ["portal-dnl", "example-dnl"]
description:
  - "This document is a small working example of a DNL route for one project."
  - "Use it to see how an agent can move from an entrypoint to a domain page, runbook, and source map."
paths:
  "@auth.md": "{@DNL-example}/domains/auth.md"
  "@login-callback.md": "{@DNL-example}/runbooks/login-callback.md"
  "@code-map.md": "{@DNL-example}/maps/code-map.md"
---

# DNL example project

This is a tiny example DNL for a fictional web project.

It is here to show the shape of a route. It is not a required folder name for your own project.

## First route

Use this route when an agent receives this question:

```text
"The login callback fails. Where should the agent start?"
```

Follow:

```text
@auth.md -> @login-callback.md -> @code-map.md
```

## What each document does

- `@auth.md`: explains the auth domain in project language
- `@login-callback.md`: lists the evidence to collect before editing code
- `@code-map.md`: points to likely source entrypoints

## Adapting this example

When you copy this pattern into a real project, choose the DNL root name that fits your repository.

After choosing the root name, update:

- `AGENTS.md` so agents start project navigation from that root
- `dnl-config.toml` so DNL tools scan that root
