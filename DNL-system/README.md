---
name: "DNL system portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@docs-index.md": "{@dnl-root}/docs/index.md"
  "@docs-core-concept.md": "{@dnl-root}/docs/core-concept.md"
  "@docs-getting-started.md": "{@dnl-root}/docs/getting-started.md"
  "@docs-dnl-config.md": "{@dnl-root}/docs/dnl-config.md"
  "@docs-agents-md.md": "{@dnl-root}/docs/agents-md.md"
  "@docs-dnl-system.md": "{@dnl-root}/docs/dnl-system.md"
  "@docs-skills.md": "{@dnl-root}/docs/skills.md"
  "@docs-skill-source-migration.md": "{@dnl-root}/docs/skill-source-migration.md"
  "@docs-repository-layout.md": "{@dnl-root}/docs/repository-layout.md"
  "@dnl-tooling.md": "{@dnl-root}/scripts/dnl/README.md"
  "@dnl-query-tool.md": "{@dnl-root}/scripts/dnl/query.md"
  "@dnl-tree-tool.md": "{@dnl-root}/scripts/dnl/tree.md"
  "@dnl-qa-tool.md": "{@dnl-root}/scripts/dnl/qa.md"
  "@dnl-util-tool.md": "{@dnl-root}/scripts/dnl/dnl_util.md"
  "@ai/README.md": "{@DNL-system}/ai/README.md"
  "@authoring/README.md": "{@DNL-system}/authoring/README.md"
  "@workflow/README.md": "{@DNL-system}/workflow/README.md"
  "@templates/README.md": "{@DNL-system}/templates/README.md"
  "@boundaries/README.md": "{@DNL-system}/boundaries/README.md"
---

# DNL system portal

This directory holds the maintenance guidance that keeps the documentation layer coherent.

## AI operating docs

- Agent behavior and document selection: `@ai/README.md`
- Writing and review rules: `@authoring/README.md`
- Lifecycle and archival flow: `@workflow/README.md`
- Reusable request and output templates: `@templates/README.md`
- Safety boundaries: `@boundaries/README.md`

## Portable tooling

- Tooling portal: `@dnl-tooling.md`
- Query generated DNL indexes: `@dnl-query-tool.md`
- Inspect a scoped directory tree: `@dnl-tree-tool.md`
- Validate DNL structure and routes: `@dnl-qa-tool.md`
- Maintain indexes, tags, and safe document moves: `@dnl-util-tool.md`

`DNL-system` defines the rules.
`scripts/dnl` is the official executable and detailed-guide surface for people and agents.
`.agents/skills` provides thin agent behavior guides and compatibility shims.
Generated indexes and QA reports remain under ignored `.agents/skills` runtime paths for compatibility; those paths do not own the implementation.

## Public reader docs

- Public overview: `@docs-index.md`
- Core concept: `@docs-core-concept.md`
- Getting started: `@docs-getting-started.md`
- Configuration guide: `@docs-dnl-config.md`
- AI entrypoint guide: `@docs-agents-md.md`
- DNL-system customization guide: `@docs-dnl-system.md`
- Skills customization guide: `@docs-skills.md`
- Skill source migration guide: `@docs-skill-source-migration.md`
- Repository layout: `@docs-repository-layout.md`

Historical material is kept separate and should be reviewed carefully before it is made public.
