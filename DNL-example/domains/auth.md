---
name: "Auth domain"
status: "draft"
tags: ["guide-dnl", "auth", "example-dnl"]
description:
  - "This document explains the auth domain in a small example project."
  - "Use it before jumping into login callback source code."
paths:
  "@login-callback.md": "{@DNL-example}/runbooks/login-callback.md"
  "@code-map.md": "{@DNL-example}/maps/code-map.md"
---

# Auth domain

Auth covers sign-in, provider callback handling, session creation, and logout.

The login callback is the boundary where the app receives an identity provider response and turns it into local session state.

## Route

For callback failures, use `@login-callback.md` before changing code.

Use `@code-map.md` only after collecting the evidence listed in the runbook.

## Useful questions

- Did the provider return an error?
- Did the callback URL match the registered redirect URI?
- Did the app create a session after the callback?
- Did the browser receive the expected cookie or redirect?
