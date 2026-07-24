# Repository Layout

This repository is a public starter for DNL. It is intentionally small at the top level.

```text
.
├── README.md
├── AGENTS.md
├── docs/
├── DNL-example/
├── DNL-system/
├── working/
├── .working-archive/
├── .agents/
├── scripts/
├── tests/
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
- `DNL-example/` holds a tiny working example route.
- `DNL-system/` holds authoring, workflow, AI routing, templates, and boundaries.
- `working/` holds shared active source material before DNL promotion.
- `.working-archive/` stores completed raw work bundles outside active routes.

Read the [AGENTS.md customization guide](agents-md.md) before adapting the AI entrypoint for your own repository.

## Tooling Surfaces

The canonical agent behavior source is:

```text
.agents/skills/
```

Tool-specific folders such as `.claude/`, `.cursor/`, and `.github/` keep thin wrappers for environments that expect their own skill locations.

Those wrappers should route back to `.agents/skills` instead of duplicating the full instructions.

Portable DNL executables and their detailed guides live here:

```text
scripts/dnl/
  query.py
  query.md
  tree.py
  tree.md
  requirements.txt
```

Portable tests live under `tests/dnl/`.
The retained `tree.py` and `dnl_query.py` files under `.agents/skills` are compatibility shims, not the official executable surface.
Builder-specific QA, index, tag, and document-move maintenance remains under `.agents/skills/dnl-builder`.

Read the [Skills customization guide](skills.md) before adding new skills or changing wrapper behavior.
If you want a different canonical skill home, read the [Skill source migration guide](skill-source-migration.md) before moving files.

## DNL-system

`DNL-system/` is not the example domain knowledge tree. It is the rule layer that keeps a DNL coherent.

It contains:

- AI context loading rules
- authoring rules
- workflow lifecycle rules
- request and output templates
- safety boundaries

If you only want to try DNL in a small project, you can start without understanding every file here.

Read the [DNL-system customization guide](dnl-system.md) before changing or pruning this layer.

## Example Knowledge Layer

`DNL-example/` is the small example included in this starter.

It exists so first-time visitors can see a working route without treating `DNL/` as a required folder name.

## Optional Knowledge Layers

Real DNL repositories may add their own knowledge tree.

Examples:

```text
your-dnl-root/
  README.md
  maps/
  domains/
  runbooks/
```

```text
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
      DNL-api-server/
working/
.working-archive/
```

These are not required folders. They are shapes you can choose when your work needs them.

## Configuration

`dnl-config.toml` defines the scan surface for DNL tooling.

In this public starter, it points at `DNL-system/` and `DNL-example/`.

When you add your own DNL tree, update the config so QA and index tools know what to scan.

Read the [dnl-config.toml guide](dnl-config.md) for the field-by-field behavior.

## Read Next

- [Getting started](getting-started.md)
- [AGENTS.md customization guide](agents-md.md)
- [DNL-system customization guide](dnl-system.md)
- [Skills customization guide](skills.md)
- [Skill source migration guide](skill-source-migration.md)
- [dnl-config.toml guide](dnl-config.md)
- [Core concept](core-concept.md)
