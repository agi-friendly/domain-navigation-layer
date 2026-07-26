---
name: "Multi-Agent Skill Guide"
status: "draft"
tags: ["guide-dnl"]
paths:
  "@skills-portal.md": "{@dnl-root}/.agents/skills/README.md"
  "@skill-source-migration.md": "{@dnl-root}/docs/skill-source-migration.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@dnl-query.md": "{@dnl-root}/.agents/skills/dnl-query/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
---

# Multi-Agent Skill Guide


This document keeps multiple AI agents consistent in how they activate skills and run shared DNL tooling.

## Core principles
- The canonical skill is always `.agents/skills/{skill-name}`.
- Each agent's `*/skills/{skill-name}/SKILL.md` is not a required structure but a routing wrapper that keeps only the tools it needs.
- Keep wrappers and canonical `SKILL.md` files short.
- Keep detailed portable tool instructions beside the executable under `scripts/dnl/{tool}.md`.
- When adding or renaming a skill, sync only the wrappers that are currently supported.
- Codex and the Antigravity/Gemini family reference `.agents/skills` directly, without repo-local wrappers.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, and `.windsurfrules` are not active surfaces today, so do not create new ones.
- Changing the canonical location of a skill is not an ordinary skill edit; follow `@skill-source-migration.md` instead.

## Common structure
```text
.agents/skills/
  <skill-name>/
    SKILL.md

scripts/dnl/
  <tool>.py
  <tool>.md

.claude/skills/<skill-name>/SKILL.md
.github/skills/<skill-name>/SKILL.md
.cursor/skills/<skill-name>/SKILL.md
```

## Skill execution flow (common to all AIs)
1. Read the root `AGENTS.md` first.
2. Read `README.md` and `docs/` only for public explanation, onboarding, or README/docs work.
3. If a wrapper `SKILL.md` is maintained for the current AI, use it only as a short router.
4. Read the canonical `.agents/skills/{skill}/SKILL.md`.
5. When needed, read only the referenced script-side guide, builder-local utility, or supporting file.

## Checklist for adding a new skill
1. Create `.agents/skills/{skill-name}/SKILL.md`.
2. Add an entry to the Skills list in `@skills-portal.md`.
3. If needed, create a `SKILL.md` with the same name at the supported wrapper paths below.
   - `.claude/skills/{skill-name}/SKILL.md`
   - `.github/skills/{skill-name}/SKILL.md`
   - `.cursor/skills/{skill-name}/SKILL.md`
4. Keep the wrapper content to the minimum instructions needed to route to the canonical skill.
5. Do not create repo-local files for Codex, Antigravity/Gemini, Kiro, or Windsurf.

## Checklist for editing an existing skill
1. Edit the canonical `.agents/skills/{skill-name}/SKILL.md` first.
2. Sync the wrapper metadata (`name`, `description`) only when needed.
3. If an implementation or detailed guide changed, update `scripts/dnl` and official command examples together.
4. If a skill path or name changed, update only the supported wrapper paths along with it.

## Recommended verification commands
Check structure:
```bash
python scripts/dnl/tree.py --root . --depth 3 --hidden --ascii
```

Check DNL link quality:
```bash
python scripts/dnl/qa.py --profile links --fail-on all
```

## Wrapper template
```markdown
---
name: <skill-name>
description: <trigger description>
---

read `AGENTS.md` of root directory and get the information about the project.
then, read `{@dnl-root}/.agents/skills/<skill-name>/SKILL.md` as the canonical skill source.
```
