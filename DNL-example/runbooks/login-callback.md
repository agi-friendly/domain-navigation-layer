---
name: "Login callback runbook"
status: "draft"
tags: ["runbook-dnl", "auth", "example-dnl"]
description:
  - "This document gives a short investigation path for login callback failures."
  - "Use it to collect evidence before changing source code."
paths:
  "@auth.md": "{@DNL-example}/domains/auth.md"
  "@code-map.md": "{@DNL-example}/maps/code-map.md"
---

# Login callback runbook

Use this when a login callback fails or returns an unexpected session state.

## Collect first

Before changing code, collect:

- callback URL and query parameters
- provider error message, if any
- server log lines for the callback request
- session or cookie state after redirect
- expected redirect target and actual redirect target

## Then inspect

After collecting evidence, inspect the source entrypoints in `@code-map.md`.

If the route handler is not enough, trace where session state is created and where callback errors are normalized.

## Stop condition

Stop expanding the investigation when you can name the failing boundary:

- provider response
- callback route
- session creation
- cookie or redirect handling
- test fixture or local setup
