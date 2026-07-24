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
- This directory is the source of truth for agent behavior guides.
- Every AI ultimately reads `.agents/skills/{skill}/SKILL.md`.
- Each agent's `skills/*/SKILL.md` is a short routing wrapper kept only for tool compatibility.
- Portable DNL executables and their detailed guides live in `scripts/dnl`.
- Codex and the Antigravity/Gemini family reference `.agents/skills` directly, without repo-local wrappers.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, and `.windsurfrules` are not active surfaces today, so do not create new ones.

## Common usage order
1. Read the root `AGENTS.md` first.
2. Read `README.md` and `docs/` only for public explanation, onboarding, or README/docs work.
3. If a wrapper file is maintained for the current AI (`<agent>/skills/{skill}/SKILL.md`), use it only as a short router.
4. Read the canonical skill document (`.agents/skills/{skill}/SKILL.md`) and load only the referenced guide, tool, or supporting file you need.
5. Run portable DNL executables from `scripts/dnl`; use builder-local scripts only for builder-specific maintenance.

## Portable tooling rule

- `DNL-system/`: canonical DNL rules, authoring guidance, and workflow.
- `scripts/dnl/{tool}.py`: official portable executable for people and agents.
- `scripts/dnl/{tool}.md`: detailed options, examples, and troubleshooting.
- `.agents/skills/{skill}/SKILL.md`: thin agent activation and behavior guide.
- Retained `tree.py` and `dnl_query.py` files under `.agents/skills`: compatibility shims only.
- `tests/dnl/`: portable tooling tests.

## Multi-agent guide
- Detailed rules and checklists: `@multi-agent-skill-guide.md`
- Moving a skill's canonical location outside `.agents/skills`, or collecting it from another tool-specific folder: `@skill-source-migration.md`

## Skills
- `dnl-builder` (`@dnl-builder.md`)
  - Routes to canonical authoring/workflow docs and provides builder-specific QA, index, tag, and move maintenance.
- `dnl-query` (`@dnl-query.md`)
  - Routes agents to the official read-only query tool at `scripts/dnl/query.py`.
- `tree` (`@tree.md`)
  - Routes agents to the official scoped tree tool at `scripts/dnl/tree.py`.
