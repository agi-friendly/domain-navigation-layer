# Repository Layout

This repository is a public starter for DNL. It is intentionally small at the top level.

```text
.
├── README.md
├── AGENTS.md
├── docs/
├── DNL-system/
├── .agents/
├── .claude/
├── .cursor/
├── .github/
├── .repo-history/
├── LICENSE
└── dnl-config.toml
```

## Main Entrypoints

- `README.md` is the public landing page for humans.
- `AGENTS.md` is the working contract for AI agents.
- `docs/` holds public explanation and onboarding pages.
- `DNL-system/` holds authoring, workflow, AI routing, templates, and boundaries.

## Agent Skill Surface

The canonical skill source is:

```text
.agents/skills/
```

Tool-specific folders such as `.claude/`, `.cursor/`, and `.github/` keep thin wrappers for environments that expect their own skill locations.

Those wrappers should route back to `.agents/skills` instead of duplicating the full instructions.

## DNL-system

`DNL-system/` is not the example domain knowledge tree. It is the rule layer that keeps a DNL coherent.

It contains:

- AI context loading rules
- authoring rules
- workflow lifecycle rules
- request and output templates
- safety boundaries

If you only want to try DNL in a small project, you can start without understanding every file here.

## Optional Knowledge Layers

Real DNL repositories may add their own knowledge tree.

Examples:

```text
DNL/
  README.md
  maps/
  domains/
  runbooks/
```

```text
products/
teams/
projects/
future/
```

These are not required folders. They are shapes you can choose when your work needs them.

## Configuration

`dnl-config.toml` defines the scan surface for DNL tooling.

In this public starter, it mostly points at `DNL-system/` because the example domain layers are intentionally not filled in yet.

When you add your own DNL tree, update the config so QA and index tools know what to scan.

Read the [dnl-config.toml guide](dnl-config.md) for the field-by-field behavior.

## Read Next

- [Getting started](getting-started.md)
- [dnl-config.toml guide](dnl-config.md)
- [Core concept](core-concept.md)
