# Getting Started

The fastest way to start is to pick a shape.

Do not begin by copying every folder. Begin by deciding what the AI agent needs to navigate.

## Step 1. Pick Your Shape

Use Small DNL when the DNL lives inside one existing project repository.

Use Umbrella DNL when the DNL is a separate knowledge repository that routes across multiple repositories.

Other shapes are possible, but these two are the clearest starting points.

## Step 2. Keep Only What Helps

This repository is a starter kit.

You can clone it, download it as a zip, or copy only the files you need. Delete folders that do not match your workflow.

Read `DNL-example/` first if you want to see a tiny working route before adapting the starter.

For Small DNL, downloading a zip is often the easiest path because you are inserting DNL into an existing project repository.

The minimum operating surface is:

```text
AGENTS.md
dnl-config.toml
DNL-system/
.agents/skills/
```

Then add your project knowledge folder, such as `DNL/README.md`, first.

`DNL/` is only an example root name. If you choose a different name, update `AGENTS.md` and `dnl-config.toml` to match.

Read [dnl-config.toml guide](dnl-config.md) when you are ready to adjust scan paths, profiles, or required tags.
Read [AGENTS.md customization guide](agents-md.md) when you are ready to tune the AI entrypoint.
Read [DNL-system customization guide](dnl-system.md) before changing global DNL operating rules.
Read [Skills customization guide](skills.md) before adding or pruning reusable agent workflows.
Read [Skill source migration guide](skill-source-migration.md) if your repository already has `.claude/skills`, `.cursor/skills`, or another canonical skill home.

For an umbrella setup, you might keep:

```text
README.md
AGENTS.md
PATHS.md
DNL-system/
DNL-shared/
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
working/
.working-archive/
```

## Step 3. Write The First Route

Do not document everything.

Create one useful route for one real question:

```text
"The login callback fails. Where should the agent start?"
```

Then add just enough Markdown to route from the entrypoint to the relevant domain page, code map, or runbook.

For a concrete minimal walkthrough, read [Example Route](example-route.md).

## Step 4. Add Local Paths When Needed

If your DNL points to source repositories outside the DNL folder, add a local `PATHS.md`.

Example:

```text
- {@backend} :: /Users/you/work/my-backend
- {@frontend} :: /Users/you/work/my-frontend
```

`PATHS.md` is usually local and private. It lets the same DNL structure work across different machines.

## Step 5. Let The Structure Grow

Add folders only when repeated work proves they are useful.

Good first additions:

- `maps/`
- `domains/`
- `runbooks/`
- `working/`
- `.working-archive/`

Avoid building a large hierarchy before the first routing problem is clear.

## Read Next

- [dnl-config.toml guide](dnl-config.md)
- [Example Route](example-route.md)
- [AGENTS.md customization guide](agents-md.md)
- [DNL-system customization guide](dnl-system.md)
- [Skills customization guide](skills.md)
- [Skill source migration guide](skill-source-migration.md)
- [Small DNL](small-dnl.md)
- [Umbrella DNL](umbrella-dnl.md)
- [Core concept](core-concept.md)
