---
name: "workflow - work lifecycle portal"
status: "draft"
tags: ["portal-dnl", "workflow-dnl"]
description:
  - "This document is the source-of-truth portal for the working, DNL promotion, archive, and history lifecycle."
  - "Agents use it before promoting working material into canonical DNL or moving raw work bundles out of active paths."
paths:
  "@concepts.md": "{@DNL-system}/workflow/concepts.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
  "@repo-history-guide.md": "{@dnl-root}/.repo-history/GUIDE.md"
---

# workflow - work lifecycle portal

This directory defines how active work moves through a DNL repository over time.
The core idea is to separate active work, promoted knowledge, archived raw bundles, and repository history.

`working/` is the human-first active work area.
`DNL-system/workflow/` is the system layer that explains the `working -> DNL -> archive` lifecycle.

## What this portal covers

- How to treat `working/` as shared source material
- How to write lightweight working bundles without over-structuring them
- When to promote repeatable knowledge into canonical DNL
- When to move raw work bundles into `.working-archive/`
- How to keep repository history separate from archived raw bundles

## Quick entry points

- Definitions and roles: `@concepts.md`
- Rules for writing working bundles: `@working-authoring-rule.md`
- Promote repeatable material into DNL: `@working-to-dnl.md`
- Move raw bundles into archive storage: `@working-to-archive.md`
- Record repository-level history: `@repo-history-guide.md`

## Core principles

1. `working/` is a shared active work area, not canonical DNL.
2. A working bundle only needs `working/{working-name}/README.md` as its minimum rule.
3. `working/README.md` is a human-facing active work index.
4. DNL holds reusable, stable knowledge.
5. Raw working bundles should not stay in active portals forever after promotion.
6. `.working-archive/` stores raw bundles; history explains why important changes happened.
7. `archived` is not a `DNL Status` value. Archive state is represented by location.
8. Promoting working material into DNL requires both lifecycle rules from workflow and writing rules from authoring.

## Lifecycle summary

```text
working/
  -> promote reusable knowledge into DNL
  -> move completed raw bundles into .working-archive/
  -> keep repository history as a separate narrative when the event matters
```

## When to read this portal first

- When you are deciding where rough work belongs
- When you need to decide whether working material should become DNL
- When a prompt mentions working, promotion, archiving, or lifecycle rules
- When archive and history are being mixed together

## One-line summary

Keep active work, promoted knowledge, archived raw bundles, and repository history separate.
