# Domain Navigation Layer

AI-first navigation for connected Markdown knowledge.

AI agents do not need another note app.
They need a map they can follow.

Domain Navigation Layer (DNL) is a lightweight, filesystem-native context layer for AI agents. It connects Markdown entrypoints, routes, runbooks, local path tokens, and source pointers so an agent can load project knowledge intentionally instead of searching blindly.

DNL is not a required folder hierarchy. It is a way to connect Markdown so an AI agent can move through your knowledge one useful step at a time.

## Who This Is For

DNL is for people who use AI agents on real projects and keep watching the agent lose time on orientation.

Use it when:

- a repository README is useful for humans but too broad for agent routing
- domain knowledge, code maps, runbooks, and handoff notes are scattered
- the same investigation starts with the same "where should I look?" question
- work spans several repositories and the agent needs a stable route between them
- you want Markdown and Git, not another hosted knowledge product

If your main problem is personal note-taking, a wiki UI, or visual brainstorming, DNL is probably not the first tool to reach for.

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

## Quick Start

For one existing project repository, start small.

1. Read the working example in `DNL-example/`.
2. Download this repository as a zip or copy only the pieces you need.
3. Copy the minimum operating surface into your target repo:

```text
AGENTS.md
dnl-config.toml
DNL-system/
.agents/skills/
```

If you want the active work lifecycle, also create:

```text
working/
.working-archive/
```

4. Choose a project knowledge root name and create the first route there.

```text
your-dnl-root/README.md
your-dnl-root/maps/code-map.md
your-dnl-root/domains/auth.md
your-dnl-root/runbooks/login-callback.md
```

`DNL-example/` is the example in this starter. Your project can use `DNL/`, `project-dnl/`, `docs/agent-routes/`, or any other clear name.

5. Update `AGENTS.md` so agents start project navigation from your chosen root.

```text
Start project navigation from your-dnl-root/README.md.
Use DNL-system/ only for DNL operating rules and maintenance guidance.
```

6. Update `dnl-config.toml` so DNL tools scan your chosen root.

```toml
[scan]
include = ["DNL-system", "your-dnl-root"]

[paths.internal]
"dnl-root" = "."
"DNL-system" = "DNL-system"
"your-dnl-root" = "your-dnl-root"
```

7. Pick one real routing question:

```text
"The login callback fails. Where should the agent start?"
```

8. Point your AI agent at `AGENTS.md` and tell it to follow the DNL route before searching source code.

Expand only when repeated context-loading pain proves another route is useful.

See the minimal route walkthrough: [Example Route](docs/example-route.md).

## Small DNL Or Umbrella DNL

Start with the shape that matches where your knowledge lives.

| Shape | Where it lives | Use it when |
| --- | --- | --- |
| Small DNL | inside one existing project repository | one repo is the main working surface |
| Umbrella DNL | in a separate knowledge repository | work crosses many repos, products, or domains |

Small DNL is the fastest way to begin. Add one project route root, such as `DNL/README.md`, and grow from there.

Umbrella DNL is for cross-repository work. The agent starts in the DNL repository, follows product or project routes, then uses `PATHS.md` tokens to reach real source repositories.

Read more:

- [Small DNL](docs/small-dnl.md)
- [Umbrella DNL](docs/umbrella-dnl.md)

## What DNL Is Not

DNL is not:

- a note-taking app
- a replacement for Obsidian or Notion
- a strict documentation hierarchy
- a vector database
- a magic memory system
- a general personal knowledge base with AI branding

DNL is:

- a navigation layer
- a Markdown-based context map
- a way to make AI agents less blind inside real projects

## Core Idea

DNL is connected Markdown for AI navigation.

At its smallest, it can be a few files:

```text
README.md
your-dnl-root/
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
DNL-shared/
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
      DNL-api-server/
working/
.working-archive/
```

The important part is not the exact folder names. The important part is that each document tells the next reader or agent where to go next.

## How DNL Works

DNL works by combining a small routing contract with lightweight validation:

- `AGENTS.md` tells the agent where to start.
- DNL route documents point to the next useful context.
- YAML `paths` define stable `@tokens` for documents and source pointers.
- `dnl-config.toml` tells tools what to scan and which tags are required.
- `.agents/skills/` gives agents reusable QA, query, and tree-inspection workflows.
- `qa.py` and generated indexes help catch missing frontmatter, stale scan config, and unresolved internal paths.
- `working/` keeps active source material separate from canonical DNL until it is promoted.

Read the mechanics and reliability model: [How DNL Works](docs/how-dnl-works.md).

## Not Another Note App

Obsidian is great for personal Markdown knowledge bases.
Notion is great for human-facing workspaces.

DNL is for a different job:

- AI agents loading context from a filesystem
- Repository-aware routing
- Project and domain maps
- Stable handoff notes
- Runbooks and code pointers
- Local path mapping through `PATHS.md`
- Work lifecycle from `working/` source material to reusable DNL knowledge

A useful shorthand:

```text
Obsidian helps humans think through linked notes.
DNL helps AI agents navigate linked project knowledge.
```

## Bring Your Own Agent

DNL does not require a DNL-specific AI subscription. Bring any agent that can read and write local files.

The DNL is the map. The agent is your choice.

## Other Possible Shapes

Small DNL and Umbrella DNL are only starting points.

You can also build:

- Team DNL: team conventions, recurring workflows, onboarding, runbooks
- Shared DNL: shared glossary, products, teams, systems, architecture maps
- Personal DNL: local agent handoff routes, active project maps, investigation logs

The hierarchy is yours. DNL does not prescribe it.

## Download, Delete, Rename

You do not have to use this repository exactly as it is.

You can:

- clone it
- download it as a zip
- copy only one folder
- delete the parts you do not need
- rename folders
- start from a blank project DNL root
- keep only the AI instructions and authoring rules

This repository is a starter kit, not a framework lock-in.

## Repository Entrypoints

If you are new here:

- Start with `README.md` for the 60-second overview.
- Read `docs/getting-started.md` when you want to try DNL in a project.
- Read `DNL-example/README.md` or `docs/example-route.md` to see the smallest useful route.
- Read `docs/how-dnl-works.md` when you want the mechanics, tags, skills, and validation model.
- Read `docs/small-dnl.md` if you are adding DNL inside one repo.
- Read `docs/umbrella-dnl.md` if you are building a cross-repository knowledge hub.

If you are an AI agent or maintaining this repository:

- `AGENTS.md` is the agent entrypoint and routing contract.
- `DNL-system/` holds maintenance, authoring, workflow, and AI routing rules.
- `working/` is the optional shared active work area.
- `.working-archive/` stores completed raw work bundles outside active routes.
- `.agents/skills/` holds reusable skill entrypoints for agents.

If you are an automated agent, read `AGENTS.md` before making changes.

## Read Next

- [Documentation index](docs/index.md)
- [Core concept](docs/core-concept.md)
- [Getting started](docs/getting-started.md)
- [How DNL Works](docs/how-dnl-works.md)
- [Example DNL](DNL-example/README.md)
- [Example Route](docs/example-route.md)
- [dnl-config.toml guide](docs/dnl-config.md)
- [AGENTS.md customization guide](docs/agents-md.md)
- [DNL-system customization guide](docs/dnl-system.md)
- [Skills customization guide](docs/skills.md)
- [Skill source migration guide](docs/skill-source-migration.md)
- [Repository layout](docs/repository-layout.md)
