# Skill Source Migration Guide

This guide is for changing where the canonical skill source lives.

The starter uses:

```text
.agents/skills/
```

Your repository may already use another home, such as:

```text
.claude/skills/
.cursor/skills/
.github/skills/
```

That is fine. The important part is not the folder name. The important part is avoiding split-brain skill instructions.

Use this rule:

```text
Choose one canonical skill source.
Everything else is a wrapper, compatibility layer, archive, or removed legacy surface.
```

## Why This Exists

Skill migration is easy to underestimate.

If two folders both look like the source of truth, agents can load different instructions depending on the tool they are running in.

Example failure:

```text
.agents/skills/dnl-builder/SKILL.md says one thing.
.claude/skills/dnl-builder/SKILL.md says another thing.
AGENTS.md points to .agents.
Claude loads .claude first.
```

That is a split-brain skill source.

The migration goal is to end with one of these shapes:

```text
one canonical source + thin wrappers
```

or:

```text
one canonical source + no wrappers
```

## When To Use This Guide

Use this guide when:

- adding DNL to a repository that already has `.claude/skills`
- adding DNL to a repository that already has `.cursor/skills`
- moving this starter's `.agents/skills` into another tool-specific folder
- consolidating scattered skill folders into one canonical home
- renaming `SKILLS/` or another old skill folder
- removing duplicated wrapper folders
- changing the skill path in `AGENTS.md`

This is different from normal skill customization.

For normal skill contents, read [Skills customization guide](skills.md).
For changing the source location, use this guide.

## Decide The Canonical Home First

Before moving files, choose the target canonical home.

| Canonical home | Good fit |
| --- | --- |
| `.agents/skills/` | You want one tool-neutral source that multiple agents can wrap |
| `.claude/skills/` | The repository is Claude-first and you want Claude's folder to remain primary |
| `.cursor/skills/` | The repository is Cursor-first and Cursor should remain the primary skill surface |
| `.github/skills/` | The repository mainly uses GitHub Copilot or GitHub-native agents |
| another path | The repository already has a strong internal convention |

This starter prefers `.agents/skills/`, but that is a preference, not a lock-in.

The repository owner gets to choose.

## Inventory Current Skill Surfaces

First, list every skill-looking surface.

Useful commands:

```bash
find .agents .claude .cursor .github -path '*/skills/*/SKILL.md' -print 2>/dev/null | sort
find . -maxdepth 3 -type d \( -name skills -o -name SKILLS \) -print 2>/dev/null | sort
rg -n "canonical skill|canonical source|\\.agents/skills|\\.claude/skills|\\.cursor/skills|SKILLS/" AGENTS.md README.md docs DNL-system .agents .claude .cursor .github 2>/dev/null
```

Then classify each path:

| Classification | Meaning |
| --- | --- |
| canonical | the one true skill source |
| wrapper | short file that points to the canonical source |
| duplicate | copied full instructions that should be merged or removed |
| legacy | old path kept only for migration history or compatibility |
| unrelated | tool config or docs that are not skill sources |

Do not classify only by folder name. Open the files and check whether they contain full instructions or only route somewhere else.

## Migration Modes

### Mode A. Consolidate Into `.agents/skills`

Use this when you want the DNL starter shape:

```text
.agents/skills/        canonical
.claude/skills/        wrapper
.cursor/skills/        wrapper
.github/skills/        wrapper
```

High-level steps:

1. Copy or move full skill bodies into `.agents/skills/<skill-name>/`.
2. Convert tool-specific skill files into thin wrappers.
3. Update `AGENTS.md` so agents read `.agents/skills/{skill}/SKILL.md` as canonical.
4. Update public docs that describe the skill source.
5. Update scripts, tests, and generated index commands that reference old paths.
6. Search for old canonical paths.
7. Run verification.

### Mode B. Move `.agents/skills` Into A Tool-Specific Home

Use this when a repository is already strongly Claude-first, Cursor-first, or GitHub-first.

Example Claude-first result:

```text
.claude/skills/        canonical
.agents/skills/        wrapper or removed
.cursor/skills/        wrapper, if used
.github/skills/        wrapper, if used
```

High-level steps:

1. Move full skill bodies from `.agents/skills/<skill-name>/` to the chosen canonical folder.
2. Decide whether `.agents/skills` should become wrappers or be removed.
3. Update `AGENTS.md` with the new canonical path.
4. Update `docs/skills.md` so it no longer claims `.agents/skills` is canonical for this repository.
5. Update this guide's prompt or local migration notes if you keep them.
6. Update DNL authoring docs or tool docs that point to skill scripts.
7. Search for stale `.agents/skills` references.
8. Run verification.

### Mode C. Keep Existing Tool Skills And Skip `.agents/skills`

Use this when adding only the DNL concept to an existing repository and the team does not want another skill folder.

Result:

```text
.claude/skills/        canonical, for example
.agents/skills/        absent
```

High-level steps:

1. Do not copy `.agents/skills`.
2. Update `AGENTS.md` to point to the repository's real canonical skill home.
3. Update `docs/skills.md` or remove it if the repository does not need public skill guidance.
4. Make sure DNL QA commands still point to real scripts, if you keep DNL tooling.
5. Run verification against the actual folder structure.

## Side-Effect Surfaces

Skill source migration often touches more than the skill folder.

Check these surfaces:

| Surface | Why it matters |
| --- | --- |
| `AGENTS.md` | The AI entrypoint may name the canonical skill path |
| `docs/skills.md` | Public docs may explain the starter's skill convention |
| `docs/agents-md.md` | The AGENTS customization guide may include skill routing examples |
| `docs/repository-layout.md` | The repository layout may name `.agents/skills` as canonical |
| `DNL-system/authoring/` | Authoring docs may point to QA scripts such as `qa.py` or `dnl_util.py` |
| `DNL-system/ai/` | AI loading rules may mention the skill source |
| `.agents/skills/README.md` | Skill portal docs may name wrappers and canonical paths |
| `.agents/skills/multi-agent-skill-guide.md` | Multi-agent wrapper policy may need to change |
| `.claude/`, `.cursor/`, `.github/` | Wrapper files may need to be rewritten or removed |
| scripts and tests | Command paths may still call the old skill home |
| generated indexes | Tag or link indexes may contain old paths |

The authoring docs are easy to miss.

For example, DNL authoring portals should point to the portable runtime:

```text
scripts/dnl/qa.py
scripts/dnl/dnl_util.py
```

These runtime paths stay stable even if the canonical AI behavior guide moves to
`.claude/skills` or another agent-specific location.

## Wrapper Template

Use a wrapper only when the tool expects its own skill path.

```md
---
name: <skill-name>
description: <trigger description>
---

Read `AGENTS.md` first.
Then read `<canonical-skill-path>/<skill-name>/SKILL.md` as the canonical skill source.
```

The wrapper should not contain the full skill body unless the repository intentionally wants tool-specific divergence.

## Prompt: Consolidate To `.agents/skills`

You can ask an agent:

```text
We are consolidating skill sources into `.agents/skills`.

Before editing, read:
- AGENTS.md
- docs/skills.md
- docs/skill-source-migration.md
- .agents/skills/README.md, if it exists
- .agents/skills/multi-agent-skill-guide.md, if it exists

Task:
- Inventory `.agents/skills`, `.claude/skills`, `.cursor/skills`, `.github/skills`, and any `SKILLS/` folder.
- Classify each skill surface as canonical, wrapper, duplicate, legacy, or unrelated.
- Move full skill bodies into `.agents/skills/<skill-name>/`.
- Convert supported tool-specific skill files into thin wrappers.
- Update AGENTS.md, docs, DNL-system authoring docs, scripts, tests, and generated indexes that reference old skill paths.
- Search for stale old paths.
- Run verification.

Before writing, show a short dry-run plan and the files you expect to touch.
```

## Prompt: Move `.agents/skills` To Another Canonical Home

You can ask an agent:

```text
We are moving the canonical skill source away from `.agents/skills`.

Target canonical skill home:
<write target path, such as .claude/skills>

Before editing, read:
- AGENTS.md
- docs/skills.md
- docs/skill-source-migration.md
- .agents/skills/README.md, if it exists
- .agents/skills/multi-agent-skill-guide.md, if it exists
- the target skill folder, if it exists

Task:
- Inventory all skill surfaces.
- Classify each surface as canonical, wrapper, duplicate, legacy, or unrelated.
- Move or merge full skill bodies into the target canonical home.
- Decide whether `.agents/skills` becomes wrappers or is removed.
- Update AGENTS.md, docs, DNL-system authoring docs, scripts, tests, and generated indexes that reference old skill paths.
- Search for stale `.agents/skills` references.
- Run verification.

Before writing, show a short dry-run plan and the files you expect to touch.
```

## Verification

Run checks that match the repository's actual tooling.

For this starter, useful checks are:

```bash
git diff --check
python3 scripts/dnl/qa.py --profile full --fail-on all --json-summary
python3 scripts/dnl/dnl_util.py tag index check
python3 scripts/dnl/dnl_util.py link index check
python3 -m unittest discover -s tests/dnl -p 'test_*.py'
```

If your repository uses a different tooling layout, update these commands before running them.

Also search for stale paths:

```bash
rg -n "SKILLS/|\\.agents/skills|\\.claude/skills|\\.cursor/skills|\\.github/skills" AGENTS.md README.md docs DNL-system .agents .claude .cursor .github 2>/dev/null
```

Do not treat every match as a failure. Some matches may be examples, wrappers, or historical notes. The goal is to make the active canonical source unambiguous.

## Final State Checklist

Before finishing, confirm:

- Exactly one folder is described as the canonical skill source.
- Every supported wrapper points to that canonical source.
- No duplicate full skill body remains in a wrapper by accident.
- `AGENTS.md` names the correct canonical skill home.
- Public docs and AI docs do not disagree about the canonical home.
- DNL authoring docs still point to working QA and utility commands.
- Tests or QA commands use real paths.
- Generated indexes are updated when DNL paths changed.

If those are true, the migration is done.

## Read Next

- [Skills customization guide](skills.md)
- [AGENTS.md customization guide](agents-md.md)
- [DNL-system customization guide](dnl-system.md)
- [Repository layout](repository-layout.md)
