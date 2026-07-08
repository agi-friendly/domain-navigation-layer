---
name: "working -> DNL promotion guide"
status: "draft"
tags: ["guide-dnl", "workflow-dnl"]
description:
  - "This document explains when and how working material becomes canonical DNL."
  - "It keeps main routers focused on current truth and moves background or raw source material out of default routes."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@concepts.md": "{@DNL-system}/workflow/concepts.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@doc-selection-rules.md": "{@DNL-system}/ai/doc-selection-rules.md"
---

# working -> DNL promotion guide

This document explains how to promote material from `working/` into canonical DNL.

Promotion is not copying a working README into a DNL folder.
Promotion means extracting the reusable knowledge, verifying it against current evidence, and rewiring active routes so future agents can find the canonical document without reading the raw bundle.

## Quick checklist for agents

If a task mentions `working-to-dnl`, promotion, absorption, or turning working material into maintained DNL:

1. Read `@workflow-root.md` and this document together with authoring rules.
2. Treat `working/` as source material, not current truth.
3. Do not promote bundles with `DNL Status: not-ready`.
4. Treat `DNL Status: ready` as a promotion candidate, not automatic approval.
5. If promotion starts, set `DNL Status: promoting` to reduce duplicate work.
6. Promote only what is verified against current source, runtime behavior, or current DNL.
7. Keep main README/portal documents focused on current truth and next routes.
8. Move background, historical drift, and working-vs-current comparison into load-on-demand docs when needed.
9. Rewire parent README, maps, guides, and cross-links to point at the new canonical DNL.
10. After rewiring, decide whether the raw working bundle should move to `.working-archive/` using `@working-to-archive.md`.

If the task is only creating, registering, or editing a working bundle, use `@working-authoring-rule.md` instead of this promotion checklist.

## When to promote

Treat a working bundle as a DNL promotion candidate when:

1. `DNL Status` is `ready`
2. the material is useful beyond one conversation or one person
3. another agent or teammate can reuse it
4. it can become a rule, guide, portal, map, glossary entry, or runbook
5. it is worth maintaining as current knowledge

## When not to promote yet

Do not promote when:

- `DNL Status` is `not-ready`
- the material is still mostly exploration notes
- the useful scope is too local or temporary
- the correct DNL layer is unclear
- another worker already has the bundle in `promoting`
- the current source or current docs have not been checked

## Promotion process

### 1. Check and lock the status

- If status is `not-ready`, stop.
- If status is `ready`, change it to `promoting` before editing canonical DNL.
- If status is already `promoting`, identify the current promoter.
- If status is `promoted`, do not promote again. Check only for missing routes or stale references.

WHY: `working/` can be shared by several humans and agents. A tiny status signal prevents duplicate promotion and half-applied route changes.

### 2. Classify the material

Decide what the reusable part is:

- rule
- playbook
- portal
- glossary
- map
- runbook
- project-specific guide

The document role determines where the promoted DNL should live.

### 3. Choose the DNL layer

Use the smallest layer that owns the rule:

- System layer
  - DNL operating rules, authoring rules, workflow, templates, boundaries
- Shared or company/team layer
  - terms, maps, conventions, or routes that apply across several projects
- Product or domain layer
  - knowledge shared by a product family or domain area
- Project layer
  - implementation-facing knowledge for one source repository or deployable unit

If layers conflict, follow `@multi-dnl-authority.md`.

### 4. Verify before extraction

`working/` was written during work. It may be stale.

Before writing canonical DNL:

- inspect current source code, current runtime behavior, current docs, or other authoritative evidence
- preserve only verified knowledge as current truth
- mark gaps or background differences separately

Do not copy:

- conversational phrasing
- personal context
- stale TODOs
- every failed attempt
- unverified claims

Extract:

- reusable decisions
- current rules
- stable routes
- terminology
- source boundaries
- repeatable investigation paths

### 5. Write canonical DNL

Canonical DNL documents should follow authoring rules:

- README files stay light and route to the next useful documents.
- YAML frontmatter declares `name`, `status`, and `tags`.
- Navigation uses YAML `paths` plus `@tokens`.
- Local Markdown file links are not used in canonical DNL documents.
- Background and decision details are split only when they are substantial enough to read on demand.

### 6. Rewire references

Promotion is incomplete until active routes point to the new canonical document.

Check:

- parent README files
- maps
- runbooks
- guides
- AGENTS.md routing if the entrypoint changed
- workflow references
- any old text that still treats `working/` as current truth

Do not archive the raw bundle before this rewiring is done.

### 7. Finish the status

After promotion and rewiring:

- set the bundle `DNL Status` to `promoted`
- remove or demote it from the active `working/README.md` index when appropriate
- decide whether to move it into `.working-archive/`

Exception: if the bundle has `Type: recurring`, ordinary batch promotion does not set the whole bundle to `promoted`.
Record the cursor and batch log, then return the bundle to `not-ready`.
Use `promoted` only when the recurring mission itself has retired.

## Good promotion result

A good promotion means:

- future agents do not need to read the raw working bundle by default
- current routes lead to canonical DNL
- the promoted knowledge is understandable without the original conversation
- old working paths are not presented as current truth
- the raw bundle can be archived without breaking active navigation

## Checklist

- Was the bundle `ready` before promotion?
- Was it marked `promoting` while promotion was active?
- Is the promoted content reusable beyond one task?
- Is the target layer clear?
- Does the promoted document avoid contradicting higher-level DNL?
- Was current evidence checked?
- Did the author avoid copying raw working text verbatim?
- Are README/portal documents still light?
- Are parent routes rewired?
- Is the raw bundle no longer needed as a default starting point?
- Was the bundle set to `promoted` after route rewiring?

## One-line summary

Promotion is the act of turning reusable source material into maintained DNL, then rewiring routes so the raw bundle can leave the active path.
