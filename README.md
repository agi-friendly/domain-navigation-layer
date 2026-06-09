# Domain Navigation Layer

AI-first navigation for connected Markdown knowledge.

AI agents do not need another note app.
They need a map they can follow.

Domain Navigation Layer (DNL) is a filesystem-native context layer for AI agents. It turns plain Markdown files into a navigable map of domain knowledge, code paths, runbooks, repository links, working notes, and handoff context.

DNL is not a required folder hierarchy. It is a way to connect Markdown so an AI agent can move through your knowledge one useful step at a time.

## Why DNL Exists

Most AI sessions start too blind.

The agent sees a repository, a prompt, and maybe a README. Then it has to guess:

- Which feature owns this problem?
- Which document explains the domain?
- Which repository has the backend?
- Which repository has the UI?
- Which files are current truth, and which are old notes?
- Where should new investigation or design work be stored?

DNL gives the agent a route before it searches everything.

It is designed for AI-first context loading, but it stays useful for humans because the source of truth is just Markdown and local files.

## Core Idea

DNL is connected Markdown.

At its smallest, it can be a few files:

```text
README.md
DNL/
  README.md
  maps/
  domains/
  runbooks/
```

At its largest, it can be an umbrella knowledge repository that routes across many projects:

```text
README.md
PATHS.md
DNL-system/
DNL-Company/
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
      DNL-api-server/
future/
```

The important part is not the exact folder names. The important part is that each document tells the next reader or agent where to go next.

## Not Another Obsidian

Obsidian is great for personal Markdown knowledge bases.
Notion is great for human-facing workspaces.

DNL is for a different job:

- AI agents loading context from a filesystem
- Repository-aware routing
- Project and domain maps
- Stable handoff notes
- Runbooks and code pointers
- Local path mapping through `PATHS.md`
- Work lifecycle from rough notes to reusable knowledge

A useful shorthand:

```text
Obsidian helps humans think through linked notes.
DNL helps AI agents navigate linked project knowledge.
```

## Bring Your Own Agent

DNL does not require a DNL-specific AI subscription. Bring any agent that can read and write local files.

The DNL is the map. The agent is your choice.

## Two Ways To Start

Start with one of these shapes. They are intentionally opposite.

### 1. Small DNL

Use this when you already have one project repository and want to add a small navigation layer inside it.

Example use:

```text
your-project/
  README.md
  AGENTS.md
  DNL/
    README.md
    maps/
    domains/
    runbooks/
```

This is the lightweight mode. You add only enough Markdown for an AI agent to stop guessing:

- what the project does
- which modules exist
- where important code lives
- how to investigate common failures
- what the current working context is

Read more: [Small DNL](docs/small-dnl.md)

### 2. Umbrella DNL

Use this when the DNL repository is not a code repository. It is a separate knowledge repository that routes across many real repositories.

Example use:

```text
workspace-dnl/
  README.md
  AGENTS.md
  PATHS.md
  DNL-system/
  DNL-Company/
  products/
    DNL-product-platform/
      projects/
        DNL-webapp/
        DNL-api-server/
  future/
```

This is the orchestration mode. An agent opens the DNL repository first, then uses the DNL to find the right product, project, domain, runbook, and local source path.

`PATHS.md` can map source tokens such as `{@webapp}`, `{@api-server}`, or `{@docs-site}` to real local repositories on your machine.

Read more: [Umbrella DNL](docs/umbrella-dnl.md)

## Other Possible Shapes

Small DNL and Umbrella DNL are only starting points.

You can also build:

- Team DNL: team conventions, recurring workflows, onboarding, runbooks
- Company DNL: shared glossary, products, teams, systems, architecture maps
- Personal DNL: private working memory, experiments, reading notes, agent handoffs

The hierarchy is yours. DNL does not prescribe it.

## Download, Delete, Rename

You do not have to use this repository exactly as it is.

You can:

- clone it
- download it as a zip
- copy only one folder
- delete the parts you do not need
- rename folders
- start from a blank `DNL/README.md`
- keep only the AI instructions and authoring rules

This repository is a starter kit, not a framework lock-in.

## Repository Entrypoints

- `README.md` is the public entrypoint for humans.
- `AGENTS.md` is the entrypoint for AI agents.
- `docs/` holds public explanation and onboarding pages.
- `DNL-system/` holds maintenance, authoring, workflow, and AI routing rules.
- `.agents/skills/` holds reusable skill entrypoints for agents.

If you are an automated agent, read `AGENTS.md` before making changes.

## Read Next

- [Documentation index](docs/index.md)
- [Core concept](docs/core-concept.md)
- [Getting started](docs/getting-started.md)
- [dnl-config.toml guide](docs/dnl-config.md)
- [AGENTS.md customization guide](docs/agents-md.md)
- [DNL-system customization guide](docs/dnl-system.md)
- [Skills customization guide](docs/skills.md)
- [Skill source migration guide](docs/skill-source-migration.md)
- [Repository layout](docs/repository-layout.md)
