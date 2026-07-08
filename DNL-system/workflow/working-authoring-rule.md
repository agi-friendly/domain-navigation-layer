---
name: "working authoring rule"
status: "draft"
tags: ["rule-dnl", "workflow-dnl"]
description:
  - "This document explains how to write lightweight working bundles as structured source material."
  - "It pairs with the working-to-dnl rule, which explains how reusable knowledge is promoted into canonical DNL."
  - "It defines how bundle Type changes the meaning of DNL Status for domain-work, dnl-internal, and recurring work."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@concepts.md": "{@DNL-system}/workflow/concepts.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
---

# working authoring rule

This document explains how to write material under `working/`.

`working/` is intentionally simple. It should be easy for a human to create a bundle and easy for an agent to understand what that bundle is for.

## Minimum structure

Every shared working bundle should have one README:

```text
working/{working-name}/README.md
```

The bundle can contain any other files or folders that help the work.
Do not force a deep taxonomy before the work is mature.

## `working/README.md`

The root `working/README.md` is a human-facing active work index.

It should answer:

- what bundles are currently active
- which bundles are ready for DNL promotion
- which bundle someone should open first
- which lifecycle Type each bundle belongs to

Unlike canonical DNL documents, `working/README.md` may use normal Markdown links to local working bundles.

WHY: `working/` is a human-first work area. Clickable local links are useful here, and the folder is not the canonical DNL navigation surface.

Group the index by bundle Type:

- `domain-work`
- `dnl-internal`
- `recurring`

WHY: Type changes how `DNL Status` should be read. Grouping the index by Type helps humans and agents interpret the same status words without guessing.

## Working bundle README

A working bundle README should stay short.

Recommended fields:

```md
# <working name>

- Schedule: 2026-06-27 ~
- Type: domain-work
- DNL Status: not-ready
- Owner: optional

## Purpose

Why this work exists.

## Current Summary

What is known right now.

## Working Material

Where the raw notes, drafts, screenshots, plans, or evidence live.

## Promotion Notes

What might eventually become canonical DNL.
```

If `Type` is omitted, read the bundle as `domain-work`.
Always write `Type:` explicitly for `dnl-internal` and `recurring` bundles.

## `DNL Status`

`DNL Status` is a minimal promotion signal, not a project-management state machine.

Allowed values:

| Value | Meaning |
| --- | --- |
| `not-ready` | Do not promote this bundle yet. |
| `ready` | Review this bundle as a DNL promotion candidate. |
| `promoting` | Someone is currently promoting it into DNL. |
| `promoted` | Required DNL promotion and route rewiring are complete. |

Do not use `archived` as a status.
Once a bundle moves to `.working-archive/`, its archived state is represented by location.

## Bundle Type

`Type` describes the lifecycle shape of the working bundle.

| Type | Meaning |
| --- | --- |
| `domain-work` | Work happens in an external product, domain, project, or source area. The bundle preserves source material until reusable knowledge is promoted. |
| `dnl-internal` | The work itself changes this DNL repository. The implementation output is already a DNL-system or DNL document change. |
| `recurring` | The bundle repeats over time, usually by reviewing source changes in batches and promoting useful findings into DNL. |

Status flow by Type:

```text
domain-work:   not-ready -> ready -> promoting -> promoted -> archive
dnl-internal:  not-ready -> (ready) -> promoting -> promoted -> archive
recurring:     not-ready -> (ready) -> promoting -> cursor update -> not-ready -> repeat
                                                    mission retired -> promoted -> archive
```

## `dnl-internal` status interpretation

For `dnl-internal`, `DNL Status` tracks whether the planned DNL change itself is being applied.

- `not-ready`: planning or design is still in progress
- `ready`: the plan is ready for someone else to execute
- `promoting`: canonical DNL files are being edited
- `promoted`: the planned DNL change is applied and no active route treats the bundle as unfinished source material

`ready` can be skipped when the same person or agent moves directly from planning to implementation.
Use `ready` when another worker should take over.

## `recurring` status interpretation

For `recurring`, `DNL Status` describes the current batch, not the whole mission.

- `not-ready`: waiting for the next run, or collecting and reviewing the current batch
- `ready`: the current batch has promotion candidates and is ready for handoff
- `promoting`: the current batch is being promoted into canonical DNL
- `promoted`: the recurring mission itself has retired; no future run is expected

Do not leave a recurring bundle as `promoted` after an ordinary batch.
After each batch, record the cursor and batch log, then return the bundle to `not-ready`.

WHY: If ordinary recurring batches use `promoted`, archive rules may incorrectly treat a live recurring mission as finished. Reserving `promoted` for mission retirement keeps the existing archive rule meaningful.

Recurring bundle READMEs should also include:

- Mission: what is being reviewed repeatedly
- Cursor: the last reviewed source position, commit, timestamp, issue number, or other stable checkpoint
- Batch log: run date, reviewed range, promoted results, deferred results, and next cursor

## Skipping `ready`

`ready` means "another promoter can take over."

- `domain-work` should normally use `ready` because the author and promoter are often different people
- `dnl-internal` may skip `ready` when the same worker immediately applies the DNL change
- `recurring` may skip `ready` when the same worker collects and promotes the batch in one flow
- use `ready` whenever handoff is expected

WHY: `ready` is a handoff signal, not a progress percentage.

## What to capture

Capture structured source material that a later human or agent can reuse:

- decisions and rejected alternatives
- blockers and how they were resolved
- AI collaboration patterns and how outputs were verified
- user intent changes that matter to the work
- evidence, commands, screenshots, source paths, or open questions

Mark uncertain claims as `UNVERIFIED`.

## What not to capture

Do not store:

- secrets, tokens, credentials, or personal data
- unrelated chat
- throwaway TODO lists that belong in an issue tracker
- claims that were never checked
- private machine paths that should live in local context

## Relationship to DNL authoring rules

Canonical DNL documents must follow YAML frontmatter and `@token` navigation rules.

`working/` is different:

- it is source material, not canonical DNL
- it can use normal Markdown links for local working navigation
- it should still be readable and structured
- promotion into DNL must go through `@working-to-dnl.md`

## Lifecycle position

```text
author   -> write structured source material in working/      (this document)
promote  -> extract reusable knowledge into canonical DNL      (@working-to-dnl.md)
archive  -> move completed raw bundles to .working-archive/    (@working-to-archive.md)
```

## Checklist

- Does the bundle have `working/{working-name}/README.md`?
- Is the bundle Type clear, especially for `dnl-internal` or `recurring`?
- Is the `DNL Status` one of `not-ready`, `ready`, `promoting`, or `promoted`?
- If the bundle is recurring, does the README include mission, cursor, and batch log fields?
- Can another human or agent understand why the bundle exists?
- Is the bundle structured enough to promote later without reading every raw note?
- Are secrets and private local paths excluded?
- Is it clear which parts are evidence and which parts are still `UNVERIFIED`?

## One-line summary

`working/` should preserve active source material without turning rough work into canonical DNL too early.
