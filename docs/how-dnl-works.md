# How DNL Works

DNL is a Markdown map with a small amount of structure around it.

The structure is not there to make Markdown complicated. It is there so an AI agent can move from a broad prompt to the right project knowledge and source path without guessing first.

## Route Flow

A typical DNL route looks like this:

```text
AGENTS.md
-> project DNL root
-> domain page or code map
-> runbook or source pointer
-> source path
```

Each step has one job:

| Surface | Job |
| --- | --- |
| `AGENTS.md` | Tell the agent where project navigation starts. |
| DNL root README | Route to the right domain, map, runbook, or working area. |
| Domain page | Explain project language and ownership. |
| Code map | Connect domain words to source files, modules, or repositories. |
| Runbook | Give a repeatable investigation path. |
| Source path | Tell the agent where code inspection should begin. |

This is why DNL should start small. One useful route is better than a large folder tree with no clear next step.

## YAML Frontmatter

Canonical DNL documents use YAML frontmatter to make routing machine-readable.

Common fields are:

| Field | Purpose |
| --- | --- |
| `name` | Human-readable document name. |
| `status` | Whether the document is active, draft, or deprecated. |
| `tags` | Search and filtering hints for agents and tools. |
| `paths` | Stable `@token` definitions for documents and source pointers. |

Example:

```yaml
---
name: "Auth domain"
status: "draft"
tags: ["auth", "guide-dnl"]
paths:
  "@login-callback.md": "{@DNL}/runbooks/login-callback.md"
  "@auth-service": "{@backend}/src/auth/AuthService.ts"
---
```

In the document body, the agent can follow `@login-callback.md` or inspect `@auth-service` without relying on a vague instruction like "look around the auth folder."

## Tags

Tags help agents find the right document without reading every Markdown file.

Examples:

- `portal-dnl`: router or entrypoint README
- `map-dnl`: code, module, screen, or source map
- `runbook-dnl`: repeatable investigation or operation path
- `rule-dnl`: authoring or operating rule
- domain tags such as `auth`, `i18n`, or `api`

Tags are not meant to repeat the folder name mechanically. They should help the next agent narrow the search.

## Path Tokens

The `paths` block gives a document stable names for the files or folders it needs.

DNL uses two token styles:

| Token style | Meaning |
| --- | --- |
| `@token` | A document-local pointer declared in YAML frontmatter. |
| `{@variable}` | A configured path variable such as `{@DNL}` or `{@backend}`. |

This keeps routes easier to rename. If a folder moves, the config or YAML path can be updated without rewriting every sentence that mentions the path.

Internal paths point inside the current repository. External paths point to another repository or workspace.

## dnl-config.toml

`dnl-config.toml` tells the tools what belongs to the DNL.

It can define:

- scan roots such as `DNL-system` and your project DNL root
- excluded folders
- internal path variables
- external path variables
- QA profiles
- required tags by filename or path pattern

The important flow is:

```text
dnl-config.toml
-> dnl-builder tools
-> generated tag and link indexes
-> dnl-query lookup
```

Generated index directories are local build artifacts. Rebuild them when they are missing or stale, but do not commit them.

For example, if you create `DNL/` but forget to add it to `scan.include`, full QA and generated indexes will not see it.

## Skills

`.agents/skills/` gives agents reusable workflows.

The starter includes:

| Skill | What it gives the agent |
| --- | --- |
| `dnl-builder` | DNL authoring rules, QA commands, and index maintenance. |
| `dnl-query` | Fast lookup through generated tag and link indexes. |
| `tree` | Scoped repository structure inspection without dumping the whole repo. |

In one line:

```text
AGENTS.md routes. DNL-system governs. DNL explains. Skills execute.
```

## Reliability Model

DNL does not make documentation automatically true.

It gives the repository a checkable navigation layer:

- `qa.py --profile full` checks the scanned DNL surface.
- `qa.py --profile portal` focuses on entrypoint and router documents.
- required tag rules catch missing document roles such as `portal-dnl` or `runbook-dnl`.
- link indexes record outbound links, backlinks, unresolved internal targets, unused path tokens, and missing token candidates.
- `dnl-query` can surface those index results without rereading every document.

Useful verification commands:

```bash
python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all --json-summary
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all --json-summary
python3 .agents/skills/dnl-builder/dnl_util.py tag index check
python3 .agents/skills/dnl-builder/dnl_util.py link index check
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary
```

If indexes are stale, rebuild them:

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py link index build
```

## What The Checks Do Not Prove

DNL checks are useful, but they are not magic.

They do not prove:

- that the source code still behaves the way the document says
- that a runbook is the best possible investigation path
- that external repositories exist on every machine
- that a deprecated idea has been removed from every old note

Agents should still inspect real source code before changing behavior.

The value of DNL is that the agent starts from a better route and can verify the route shape before it searches widely.

## Read Next

- [dnl-config.toml guide](dnl-config.md)
- [Skills customization guide](skills.md)
- [Example Route](example-route.md)
- [Getting started](getting-started.md)
