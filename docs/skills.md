# Skills Customization Guide

`.agents/skills/` is the reusable agent behavior surface for a DNL repository.
Portable executables and their detailed guides live under `scripts/dnl/`.

If DNL gives an agent a map, skills tell the agent when and how to use repeatable workflows.
Scripts provide the shared executable surface for people and agents.

Use this rule:

```text
DNL-system defines the rules.
scripts/dnl provides portable executables and detailed guides.
.agents/skills provides agent behavior guides and compatibility shims.
```

## What Skills Are For

Use skills to trigger and guide work that an agent may need to repeat:

- writing or reviewing DNL documents
- running DNL QA
- querying generated indexes
- inspecting repository structure
- reading logs or generated reports
- building project-specific maps
- checking release, migration, or deployment steps

A skill should make a repeatable workflow easier to trigger, route, verify, and reuse across agent tools.

## Canonical Skill Source

In this starter, the canonical skill source is:

```text
.agents/skills/
```

Tool-specific folders can wrap that source:

```text
.claude/skills/
.cursor/skills/
.github/skills/
```

Those wrapper folders exist because different tools may expect different local paths.
The starter keeps wrappers thin and puts the canonical agent behavior in `.agents/skills/{skill-name}/SKILL.md`.
For portable DNL tools, `SKILL.md` routes to the executable and detailed guide under `scripts/dnl/`.

That keeps one source of truth:

```text
.agents/skills/dnl-builder/SKILL.md
  <- .claude/skills/dnl-builder/SKILL.md
  <- .cursor/skills/dnl-builder/SKILL.md
  <- .github/skills/dnl-builder/SKILL.md
```

You own your repository after copying or downloading this starter. You can use a different shape. This guide describes the starter's bias: one canonical skill, many thin wrappers when needed.

If your repository already treats another folder as the canonical skill source, read the [Skill source migration guide](skill-source-migration.md) before moving or deleting skill files.

## Starter Skills

The starter includes three useful skills:

| Skill | Purpose |
| --- | --- |
| `dnl-builder` | Routes agents to DNL authoring rules and the official QA/index/tag/move tools |
| `dnl-query` | Routes agents to the portable read-only query tool |
| `tree` | Routes agents to the portable scoped directory tree tool |

For a Small DNL, these are usually enough at first.

## How Skills Fit With DNL

Use these boundaries:

| Surface | Role |
| --- | --- |
| `AGENTS.md` | Tells the agent where to start |
| `DNL-system/` | Defines DNL operating and authoring rules |
| `DNL/`, `products/`, `projects/` | Stores project or domain knowledge |
| `scripts/dnl/` | Provides portable executables and detailed command guides |
| `.agents/skills/` | Provides thin behavior guides and compatibility shims |
| `tests/dnl/` | Verifies portable tree/query/QA/maintenance behavior and compatibility shims |
| `.claude/`, `.cursor/`, `.github/` | Optional wrappers for specific agent tools |

The same idea in one line:

```text
AGENTS.md routes. DNL-system governs. DNL explains. Skills guide. Scripts execute.
```

## When To Customize Skills

Customize `.agents/skills/` when repeated agent work needs a clearer tool or procedure.

Good reasons:

- Agents repeatedly run the wrong QA command.
- Agents need a standard trigger and boundary for inspecting a project tree.
- Agents need a script to generate or refresh a map.
- Agents need a domain-specific checklist before editing.
- Humans and agents keep repeating the same prompt or terminal sequence.
- A wrapper points to an old skill name or path.

If the problem is "the agent does not know where to start," update `AGENTS.md` or the DNL route first.
If the problem is "the agent knows where to start but keeps doing the work differently," a skill may help.

## What To Put In A Skill

A useful skill usually answers:

- When should the agent use this skill?
- What should the agent read first?
- Which command or script should it run?
- What inputs does it need?
- What output should it produce?
- What counts as verification?
- What should it do if the command fails?

The skill can include examples, templates, references, or agent-specific helpers.
Portable DNL commands shared with humans must live under `scripts/dnl/`.

Common shape:

```text
.agents/skills/<skill-name>/
  SKILL.md
  README.md
  scripts/
  examples/
  templates/
```

Keep `SKILL.md` focused on triggering and operating the skill. Put longer examples or implementation notes in supporting files.
When the workflow uses a portable DNL executable, put the detailed guide beside it under `scripts/dnl/`.

## Portable DNL Tool Pattern

Use this pattern for a command intended for people and agents:

```text
scripts/dnl/<tool>.py
scripts/dnl/<tool>.md
tests/dnl/test_<tool>.py
.agents/skills/<skill>/SKILL.md
```

The skill activates the behavior.
The script executes it.
The script-side guide owns options and examples.
The test belongs to the portable tooling surface.

## Gentle Placement Hints

Once you copy this starter, the repository is yours. These are not hard rules, just the DNL starter's default taste.

Skills are usually best for:

- repeatable behavior triggers
- routing to canonical rules or tools
- generated indexes
- verification routines
- reusable prompts with a clear trigger

Scripts are usually best for:

- portable commands used by people and agents
- command-line options and stable output formats
- cross-platform execution logic

DNL documents are usually best for:

- domain explanations
- project maps
- runbooks
- glossary entries
- current architecture or workflow knowledge

Local context files are usually best for:

- machine-specific paths
- current-user handoff
- private local notes

If a file starts explaining what the product is, it probably wants to be DNL knowledge.
If it starts explaining how to repeatedly do a task, it may want to be a skill.

## Add A New Skill

Start small.

1. Create `.agents/skills/<skill-name>/SKILL.md`.
2. Give it a short `name` and `description`.
3. Explain when to use it.
4. List the first files to read.
5. List the command or workflow.
6. Add verification.
7. Add wrappers only for the tools you actually use.

Example:

````md
---
name: release-checker
description: Check release readiness before a tagged deployment
---

# Release Checker

Use this when the user asks for release readiness or pre-tag validation.

Before answering:

1. Read `AGENTS.md`.
2. Read `DNL-system/README.md`.
3. Read `DNL/releases/README.md`.

Run:

```bash
./scripts/check-release.sh
```

Report:

- blocking issues
- warnings
- commands run
- files inspected
````

## Wrapper Pattern

If an agent tool needs its own skill folder, create a short wrapper that routes back to the canonical skill.

Example:

```md
---
name: release-checker
description: Check release readiness before a tagged deployment
---

Read `AGENTS.md` first.
Then read `.agents/skills/release-checker/SKILL.md` as the canonical skill source.
```

Prefer not to copy the full skill body into every wrapper unless you intentionally want each tool to diverge.

## Update An Existing Skill

Use this order:

1. Update `.agents/skills/<skill-name>/SKILL.md`.
2. Update `scripts/dnl` when the portable implementation or detailed guide changes.
3. Update `.agents/skills/README.md` if the skill list changed.
4. Update wrappers only if the name, description, or path changed.
5. Run the skill's own verification.
6. Run DNL QA and index checks if DNL docs or indexes changed.

For the starter DNL skills, useful checks include:

```bash
python3 scripts/dnl/qa.py --profile full --fail-on all --json-summary
python3 scripts/dnl/dnl_util.py tag index check
python3 scripts/dnl/dnl_util.py link index check
python3 -m unittest discover -s tests/dnl
```

If a generated index is stale, rebuild it:

```bash
python3 scripts/dnl/dnl_util.py tag index build
python3 scripts/dnl/dnl_util.py link index build
```

If the repository is changing where canonical skills live, use the [Skill source migration guide](skill-source-migration.md) instead of treating it as a normal skill edit.

## Small DNL Starting Point

For a Small DNL, keep the starter skills at first:

```text
.agents/skills/dnl-builder/
.agents/skills/dnl-query/
.agents/skills/tree/
scripts/dnl/
tests/dnl/
```

Then add a custom skill only after a real repeated workflow appears.

Possible Small DNL custom skills:

- `api-map-builder`: build or refresh API route maps
- `log-reader`: inspect local logs with project-specific conventions
- `release-checker`: validate release readiness
- `migration-reviewer`: inspect schema or migration changes
- `ui-route-map`: summarize frontend route structure

The useful test is:

```text
Would I ask an agent to do this workflow again next month?
```

If yes, a skill may be worth it.

## Prompt To Customize Skills

You can ask an agent:

```text
We are customizing the skill surface for this DNL repository.

Before editing, read:
- AGENTS.md
- docs/skills.md
- docs/agents-md.md
- docs/dnl-system.md
- .agents/skills/README.md
- .agents/skills/multi-agent-skill-guide.md

Goal:
Make repeatable agent workflows reusable without duplicating full instructions across tool-specific wrappers.

Preferences:
- Keep `.agents/skills` as the canonical skill source unless this repository chooses another convention.
- Keep wrappers thin.
- Put domain knowledge in DNL documents.
- Put repeatable commands, scripts, verification, and workflow triggers in skills.
- Update only wrappers for tools this repository actually supports.
- Verify paths and generated indexes after changes.
```

## Read Next

- [AGENTS.md customization guide](agents-md.md)
- [Skill source migration guide](skill-source-migration.md)
- [DNL-system customization guide](dnl-system.md)
- [Small DNL](small-dnl.md)
- [Repository layout](repository-layout.md)
