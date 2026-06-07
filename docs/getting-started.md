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

For Small DNL, downloading a zip is often the easiest path because you are inserting DNL into an existing project repository.

The minimum operating surface is:

```text
AGENTS.md
dnl-config.toml
DNL-system/
.agents/skills/
```

Then add your project knowledge folder, usually `DNL/README.md` first.

Read [dnl-config.toml guide](dnl-config.md) when you are ready to adjust scan paths, profiles, or required tags.

For an umbrella setup, you might keep:

```text
README.md
AGENTS.md
PATHS.md
DNL-system/
products/
projects/
future/
```

## Step 3. Write The First Route

Do not document everything.

Create one useful route for one real question:

```text
"The login callback fails. Where should the agent start?"
```

Then add just enough Markdown to route from the entrypoint to the relevant domain page, code map, or runbook.

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
- `future/`

Avoid building a large hierarchy before the first routing problem is clear.

## Read Next

- [dnl-config.toml guide](dnl-config.md)
- [Small DNL](small-dnl.md)
- [Umbrella DNL](umbrella-dnl.md)
- [Core concept](core-concept.md)
