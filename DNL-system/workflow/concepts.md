---
name: "workflow concepts"
status: "draft"
tags: ["reference-dnl", "workflow-dnl"]
description:
  - "This document defines the boundaries between working, DNL, archive, history, and local current-work files."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
  "@repo-history-guide.md": "{@dnl-root}/.repo-history/GUIDE.md"
---

# workflow concepts

This document fixes the main terms used by the DNL workflow layer.

## `working/`

`working/` is the shared active work area.

Use it for source material that is useful to humans and agents while work is still forming:

- investigation notes
- design drafts
- decision logs
- AI collaboration notes
- rough implementation plans
- promotion candidates that are not canonical DNL yet

Minimum rule:

```text
working/{working-name}/README.md
```

The bundle can have any substructure underneath that README.

Summary:

- **shared active work area**
- **source material**
- **human-first**

## `DNL`

DNL is the canonical navigation layer.

Use it for reusable, maintained knowledge:

- terms
- portals
- rules
- maps
- runbooks
- guides
- playbooks

Working material becomes DNL only after it is promoted through `@working-to-dnl.md`.

Summary:

- **promoted knowledge**
- **AI-first**
- **validated and routable**

## `.working-archive/`

`.working-archive/` stores raw working bundles after their active role is finished.

Use it when:

- the reusable parts have been promoted into DNL
- active routes no longer treat the bundle as current truth
- the raw material still has reference value

Do not use archive as a default starting point for agents.

Summary:

- **archived raw bundle**
- **reference-only**

## `history`

History explains why a structure, decision, or repository behavior changed.

History is not the same as archive:

- archive keeps raw bundles
- history interprets important events

Use history for repository-level meaning, not for entire source-material folders.

Summary:

- **interpreted history**
- **decision narrative**

## `.repo-history/`

`.repo-history/` is repository-operating history.

Use it for:

- why a workflow concept was introduced
- why a repository structure changed
- what long-lived operating lesson remains

Do not use it for:

- raw design folders
- task bundles
- project implementation drafts

## `CURRENT_WORKING/`

`CURRENT_WORKING/` is an optional local, usually gitignored workspace.

Use it for private or temporary current-work material that should not be shared yet.

If a work bundle should be shared with future agents or teammates, move the useful active material into `working/`.

## Decision rule

Use this quick placement check:

| Question | Put it in |
| --- | --- |
| Is this active source material shared by humans and agents? | `working/` |
| Is this reusable knowledge that should guide future agents? | DNL |
| Is this raw material whose active role is done? | `.working-archive/` |
| Is this the meaning of a repository-level change? | history / `.repo-history/` |
| Is this private or temporary local work? | `CURRENT_WORKING/` |
