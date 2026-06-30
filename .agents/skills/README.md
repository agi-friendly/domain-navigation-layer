---
name: "Agents Skills Portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@multi-agent-skill-guide.md": "{@dnl-root}/.agents/skills/multi-agent-skill-guide.md"
  "@skill-source-migration.md": "{@dnl-root}/docs/skill-source-migration.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@dnl-query.md": "{@dnl-root}/.agents/skills/dnl-query/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
---

# Agents Skills Portal


## Purpose
- This directory is the source of truth for skills.
- Every AI ultimately reads `.agents/skills/{skill}/SKILL.md`.
- Each agent's `skills/*/SKILL.md` is a short routing wrapper kept only for tool compatibility.
- Codex and the Antigravity/Gemini family reference `.agents/skills` directly, without repo-local wrappers.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, and `.windsurfrules` are not active surfaces today, so do not create new ones.

## Common usage order
1. Read the root `AGENTS.md` first.
2. Read `README.md` and `docs/` only for public explanation, onboarding, or README/docs work.
3. If a wrapper file is maintained for the current AI (`<agent>/skills/{skill}/SKILL.md`), use it only as a short router.
4. Read the canonical skill document (`.agents/skills/{skill}/SKILL.md`) and load only the scripts/references you need.
5. Always run and edit scripts using paths relative to `.agents/skills/{skill}`.

## Multi-agent guide
- Detailed rules and checklists: `@multi-agent-skill-guide.md`
- Moving a skill's canonical location outside `.agents/skills`, or collecting it from another tool-specific folder: `@skill-source-migration.md`

## Skills
- `dnl-builder` (`@dnl-builder.md`)
  - Routes to the canonical DNL authoring/maintenance docs (`DNL-system/authoring`) and provides QA.
- `dnl-query` (`@dnl-query.md`)
  - Reads the generated tag index to query DNL documents by tag/name/status/path.
- `tree` (`@tree.md`)
  - Python-based tree structure analyzer (a replacement for Windows `tree`).
