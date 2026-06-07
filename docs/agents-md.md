# AGENTS.md Customization Guide

`AGENTS.md` is the AI entrypoint for a DNL-enabled repository.

It is not the human README. It is not the whole knowledge base. Its job is to tell an AI agent where to start, which rules matter, and how to move from the repository root into the right DNL documents.

Think of it as the first router.

## What AGENTS.md Should Do

A good `AGENTS.md` should answer:

- What kind of repository is this?
- Where is the DNL system portal?
- Where is the project knowledge entrypoint?
- Which local context files may exist?
- Which skill directory is canonical?
- When should the agent read public docs?
- What should the agent avoid guessing?

It should not try to explain every domain, module, workflow, or code path.

## Where It Fits

Use these roles:

| File or folder | Role |
| --- | --- |
| `README.md` | Human-facing public entrypoint |
| `AGENTS.md` | AI-facing entrypoint and routing contract |
| `DNL-system/` | DNL operating rules, authoring rules, workflow, templates |
| `DNL/` | Project knowledge for a Small DNL |
| `products/`, `projects/`, `teams/` | Optional knowledge layers for larger DNL shapes |
| `.agents/skills/` | Canonical reusable skills and tools |
| `PATHS.md` | Optional local machine path mapping |
| `CURRENT_USER.md` | Optional current-user or current-work handoff |

The key boundary is simple:

```text
AGENTS.md says where to go.
DNL documents explain what is there.
Skills provide reusable tools.
```

## Minimum Small DNL Template

For a Small DNL inserted into one project repository, start with this:

```md
---
name: "Before answering:"
paths:
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@ai-context-loading.md": "{@dnl-root}/DNL-system/ai/context-loading.md"
  "@ai-doc-selection-rules.md": "{@dnl-root}/DNL-system/ai/doc-selection-rules.md"
  "@ai-local-context.md": "{@dnl-root}/DNL-system/ai/local-context/README.md"
  "@dnl.md": "{@dnl-root}/DNL/README.md"
  "@skills-readme.md": "{@dnl-root}/.agents/skills/README.md"
---

# Before answering:
- Treat this file as the AI entrypoint for the repository.
- Read and follow `@dnl-system.md` as the DNL system portal.
- Use `@ai-context-loading.md` and `@ai-doc-selection-rules.md` to decide what to load next.
- Start project/domain navigation from `@dnl.md`.
- Use `@ai-local-context.md` when the task depends on local path mapping or current-user handoff.
- If the task mentions a skill, use `.agents/skills/{skill}/SKILL.md` as the canonical source.
- Read `README.md` and `docs/` only when the task is about public explanation, onboarding, or docs content.

---

# Project routing:
- Do not scan the whole repository before checking the DNL route.
- Do not guess paths that are not in the repository or local context.
- Keep answers grounded in files actually read.
- If the target layer is unclear, ask one narrow clarifying question.
```

Then adjust only the parts that are true for your repository.
If `DNL/README.md` does not exist yet, create the project portal first or leave `@dnl.md` out until it exists.

## What To Customize First

### 1. Project Shape

Tell the agent which DNL shape it is entering.

For Small DNL:

```md
- Treat this repository as one project with an embedded Small DNL.
- Start project/domain navigation from `@dnl.md`.
```

For Umbrella DNL:

```md
- Treat this repository as an umbrella knowledge hub, not a source repository.
- Use `PATHS.md` for local repository mappings when needed.
- Route through products, projects, teams, or future notes only after the target layer is clear.
```

### 2. Path Tokens

Keep important entrypoints in the frontmatter `paths` map.

Good path tokens:

```yaml
paths:
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@dnl.md": "{@dnl-root}/DNL/README.md"
  "@paths-md.md": "{@dnl-root}/DNL-system/ai/local-context/paths-md.md"
```

Use path tokens for stable entrypoints. Do not fill `AGENTS.md` with every file in the project.

### 3. Loading Rules

Tell the agent how to load context.

Good rules:

```md
- Load the smallest document set that can answer the task.
- Load public docs only for public explanation, onboarding, or README/docs tasks.
- Load DNL authoring docs before changing DNL documents.
- Load local context docs only when the task depends on paths, current work, or user handoff.
```

Avoid vague rules such as:

```md
- Understand the whole project before answering.
```

That pushes the agent toward broad scanning.

### 4. Skill Routing

If this starter keeps `.agents/skills/`, tell the agent that this is the canonical skill surface.

```md
- If the task mentions a skill, use `.agents/skills/{skill}/SKILL.md` as the canonical source.
- Treat `.claude/`, `.cursor/`, and `.github/` skill files as thin wrappers when they exist.
```

Do not duplicate full skill instructions inside `AGENTS.md`.

If your repository chooses a different canonical skill home, update this section and read the [Skill source migration guide](skill-source-migration.md) before moving files.

### 5. Public Docs Boundary

Make the human/AI docs boundary explicit.

```md
- Treat `README.md` and `docs/` as reader-facing public documentation.
- Use `DNL-system/` for AI routing, maintenance rules, workflow guidance, templates, or repository-local context.
- Use `DNL/` for project-specific domain knowledge.
```

This keeps public onboarding from turning into hidden AI operating instructions.

## Optional Sections

Add these only when they are useful.

### Answer Style

Use this for repository-specific output expectations, not personal preference overload.

```md
# Answer style
- Be concise.
- Cite files you actually read.
- Separate findings, assumptions, and next steps.
```

### Coding Rules

Keep this short and repository-specific.

```md
# Coding rules
- Follow the dominant style of the file being edited.
- Keep changes scoped to the user request.
- Do not overwrite unrelated local changes.
```

### Verification Rules

List commands that are safe and meaningful for this repository.

```md
# Verification
- For DNL docs, run `python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all`.
- For link index changes, run `python3 .agents/skills/dnl-builder/dnl_util.py link index check`.
```

### Current Work

If current-work handoff matters, point to a local file instead of placing volatile state in `AGENTS.md`.

```md
- If `CURRENT_USER.md` exists, read it for current-user handoff.
- If `CURRENT_WORKING/` exists, use it only when the task asks about active work.
```

`CURRENT_USER.md` and `CURRENT_WORKING/` are often local or gitignored.

## Common Mistakes

### Turning AGENTS.md into the whole DNL

Keep `AGENTS.md` short. If a section starts explaining domain knowledge, move that content into `DNL/` and link to it.

### Forgetting the project knowledge entrypoint

An agent can read `DNL-system/` and still not know your product. For Small DNL, add a project entrypoint such as:

```yaml
paths:
  "@dnl.md": "{@dnl-root}/DNL/README.md"
```

### Pointing to missing files

Only route to files that exist or clearly explain that the file is optional/local.

### Mixing local machine paths into AGENTS.md

Keep machine-specific paths in `PATHS.md`. Keep `AGENTS.md` portable.

### Duplicating skill instructions

Route to `.agents/skills/{skill}/SKILL.md`. Do not copy the skill content into `AGENTS.md`.

### Asking the agent to read everything

Prefer routing rules over broad loading rules.

Good:

```md
- Load deeper domain docs only after the target layer is known.
```

Risky:

```md
- Read all docs before answering.
```

## Prompt To Customize AGENTS.md

You can ask an agent:

```text
We are adding DNL to this repository.

Before editing, read:
- AGENTS.md
- docs/agents-md.md
- docs/dnl-config.md
- docs/small-dnl.md

Customize AGENTS.md for a Small DNL.

Rules:
- Keep AGENTS.md short.
- Use YAML frontmatter paths for stable entrypoints.
- Route project/domain navigation to DNL/README.md.
- Route DNL operating rules to DNL-system/README.md.
- Route skills to .agents/skills/{skill}/SKILL.md.
- Do not add machine-specific paths.
- Do not invent project facts.
```

## Verify

After changing `AGENTS.md`, run:

```bash
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all --json-summary
python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all --json-summary
```

If the change adds or removes DNL `paths` declarations inside scanned documents, also check the link index:

```bash
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```

## Read Next

- [Small DNL](small-dnl.md)
- [dnl-config.toml guide](dnl-config.md)
- [Repository layout](repository-layout.md)
