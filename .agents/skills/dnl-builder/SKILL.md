---
name: dnl-builder
description: Use when creating, editing, restructuring, promoting, or validating canonical DNL documents and routes.
---

# DNL Builder

Use this skill as an AI behavior router for DNL authoring and maintenance.
Canonical rules belong to `DNL-system`; portable runtime and detailed command
guides belong to `scripts/dnl`.

## Required reading

1. `DNL-system/authoring/README.md`
2. `DNL-system/authoring/rules/markdown-rule.md`
3. `DNL-system/authoring/rules/yaml-frontmatter-rule.md`
4. `DNL-system/authoring/rules/multi-dnl-authority.md`
5. `DNL-system/authoring/dnl-authoring-playbook.md`
6. Read `DNL-system/workflow/README.md` and its routed lifecycle rule when the
   work touches `working`, promotion, or archive.

## Behavior

- Maintain the navigation layer, not only the edited leaf document.
- Rewire parent portals, maps, guides, and cross-links when canonical truth
  moves.
- Keep portals concise and move substantial background to load-on-demand
  documents.
- Treat `working/` as source material, not canonical DNL.
- Search for semantic stale routes and wording after structural changes.
- Inspect a dry run before using `--write`.

## Official tools

Read `scripts/dnl/README.md` for the tooling portal and these detailed guides:

- QA: `scripts/dnl/qa.md`
- Maintenance and safe moves: `scripts/dnl/dnl_util.md`

Common commands:

```bash
python3 scripts/dnl/qa.py --profile portal --fail-on all
python3 scripts/dnl/qa.py --profile full --fail-on all
python3 scripts/dnl/dnl_util.py tag index check
python3 scripts/dnl/dnl_util.py link index check
```

For a one-document move:

```bash
python3 scripts/dnl/dnl_util.py mv --path docs/old.md --to docs/reference
python3 scripts/dnl/dnl_util.py mv --path docs/old.md --to docs/reference --write
```

The move command does not rename files or create directories. Resolve local
Markdown and image links manually before using it.

## Compatibility

Executables retained in this skill directory are deprecated compatibility
shims. Do not use them in new commands, documentation, or automation.
