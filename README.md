# Domain Navigation Layer

AI agents do not need another note app.
They need a map they can follow.

Domain Navigation Layer (DNL) is a filesystem-native context layer for AI agents. It turns plain Markdown files into a navigable map of domain knowledge, runbooks, code maps, repository paths, and working context.

This repository is intentionally generic. It does not assume a specific company, product line, or private codebase.

## Why not just Notion or Obsidian?

Notion is great for human-facing workspaces.
Obsidian is great for personal Markdown knowledge bases.

DNL is designed for a different job: AI context loading.

- Plain files, versioned with Git
- Works across macOS, Windows, and Linux because the source of truth is the filesystem
- No vendor workspace or built-in AI subscription required
- YAML path tokens keep long and repeated paths short
- `PATHS.md` can map documentation tokens to real local repositories
- One AI session can route across backend, frontend, operations, and docs when the context layer points to all of them

## Tiny example

```text
"Mail backup download fails. Find the cause."
```

Without a context layer, an agent has to guess:

- What is "mail backup"?
- Which screen or feature owns it?
- Which repository has the backend?
- Which frontend route opens it?
- Where are the logs, storage rules, and runbooks?

With DNL, a real workspace can route the agent through a small chain instead of a full document dump:

```text
README.md
-> docs/index.md
-> sample-product/README.md
-> sample-product/domains/mail/README.md
-> sample-product/domains/mail/runbooks/backup-download.md
-> PATHS.md for real local repository paths
```

The goal is simple: make the context you already know available to the AI, one useful step at a time.

## Start here

- [Documentation index](docs/index.md)
- [Core concept](docs/core-concept.md)
- [Getting started](docs/getting-started.md)
- [Repository layout](docs/repository-layout.md)

## What lives where

- `README.md` gives the public overview.
- `docs/` holds the user-facing explanation and onboarding pages.
- `DNL-system/` holds maintenance guidance for people and agents working on the layer.
- `AGENTS.md` contains repo-specific instructions for automated collaborators.

If you're an automated agent, read `AGENTS.md` before making changes.

Keep the root README short. Put deeper explanations in `docs/`.
