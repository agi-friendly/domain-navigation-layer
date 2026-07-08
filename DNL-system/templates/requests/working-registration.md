---
name: "working-registration - working bundle request template"
status: "draft"
tags: ["template-dnl", "workflow-dnl"]
description:
  - "This document is a request template for registering a new working bundle."
  - "It captures bundle Type, DNL Status, and promotion notes without turning rough work into canonical DNL."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
---

# working-registration - working bundle request template

Use this template when asking an agent to create or register a new bundle under `working/`.

`working/` is a human-first active work area.
It stores source material, handoff notes, and promotion candidates before reusable knowledge becomes canonical DNL.

---

## Copy-paste prompt

```text
Register a new working bundle.

Work name:
- Recommended folder name:
- Start date:
- Expected end:
- Bundle Type: domain-work / dnl-internal / recurring

Purpose:
- Why this work exists:
- What improves when it is done:
- What this work will not cover:

Initial scope:
- Related DNL area:
- Related source area:
- Related working/history/source material:

Recommended order:
- P0:
- P1:
- P2:

Checklist:
- Use [ ] / [x] task markers.
- Include the next recommended action so another agent can continue later.

DNL promotion:
- Start with DNL Status: not-ready.
- Mark reusable promotion candidates separately.
- If Type is recurring, add mission, cursor, and batch log sections.
```

---

## Agent instructions

- Read `@workflow-root.md` and `@working-authoring-rule.md` before writing the bundle.
- Create `working/{working-name}/README.md`.
- Keep the bundle README short enough for a human or agent to re-enter quickly.
- Start new bundles with `DNL Status: not-ready` unless the user explicitly says otherwise.
- If the bundle is `dnl-internal` or `recurring`, write an explicit `Type:` line near the top of the README.
- Add the bundle to the matching section of `working/README.md`.
- For `recurring`, include:
  - Mission
  - Cursor
  - Batch log
- Do not treat the working bundle as canonical DNL.
- Use `@working-to-dnl.md` before promoting reusable material.
- Use `@working-to-archive.md` before moving raw bundles out of active paths.

---

## Good request criteria

- The work name and rough schedule are clear.
- Bundle Type is selected.
- The reason for the work is stated in one or two sentences.
- Scope boundaries are explicit.
- DNL promotion candidates are separated from raw notes.
- Recurring work has a cursor strategy.
