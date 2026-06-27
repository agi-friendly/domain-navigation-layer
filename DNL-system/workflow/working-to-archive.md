---
name: "working -> archive guide"
status: "draft"
tags: ["guide-dnl", "workflow-dnl"]
description:
  - "This document explains when a working bundle can move out of active paths and into raw archive storage."
  - "Use it after DNL promotion and route rewiring are complete."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@concepts.md": "{@DNL-system}/workflow/concepts.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@repo-history-guide.md": "{@dnl-root}/.repo-history/GUIDE.md"
---

# working -> archive guide

This document explains when to move a raw working bundle into `.working-archive/`.

Archive movement is not cleanup for its own sake.
It protects active navigation by separating current routes from completed source material.

## Purpose

Move completed raw bundles into archive to:

- keep `working/` focused on active or promotion-ready work
- reduce noise in default agent navigation
- preserve useful source material without presenting it as current truth
- separate raw evidence from interpreted history

## When to archive

Archive a working bundle when all of these are true:

1. reusable content has been promoted into DNL
2. active routes no longer treat the bundle as canonical or current truth
3. the bundle is no longer active
4. the bundle README has `DNL Status: promoted`
5. the raw material has reference value

## When not to archive yet

Do not archive when:

- `DNL Status` is `not-ready`, `ready`, or `promoting`
- an active route still points to the bundle as a default starting point
- promotion is incomplete
- another human or agent still needs the bundle in active work
- the bundle should be deleted instead of preserved

## After archive movement

After moving a bundle:

- treat archive as reference-only
- do not link archive as a default active route
- do not describe archived raw material as canonical DNL
- keep or write a separate history document only when the event itself matters
- use `.working-archive/` location as the archived signal

## Recommended archive path

Use a date and bundle name:

```text
.working-archive/
  2026/
    06/
      example-working-bundle/
```

The exact layout can vary, but active `working/` and archived raw bundles should be visually distinct.

## Archive vs history

Archive stores raw material.
History explains meaning.

```text
raw bundle       -> .working-archive/
event narrative  -> history / .repo-history/
canonical route  -> DNL
```

Do not use history as a raw file dump.
Do not use archive as the explanation of why a repository changed.

## Move checklist

- Is the canonical DNL already written?
- Are active routes rewired away from the raw bundle?
- Is the bundle status `promoted`?
- Does the archive location clearly signal reference-only material?
- Is the bundle removed from the active part of `working/README.md`?
- Is a history note needed for the decision or structure change?

## Practical rule

Prefer move over copy.

WHY: keeping the same raw bundle in active and archived locations makes both look current. Move only after routes are rewired.

## One-line summary

Archive movement keeps active work visible while preserving completed raw material outside the default route.
