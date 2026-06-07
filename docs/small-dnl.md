# Small DNL

Small DNL is the single-project shape.

Use it when you already have a project repository and want to add a small navigation layer inside it. The DNL does not replace your codebase, README, issue tracker, or existing docs. It gives an AI agent a short route before it starts searching.

Small DNL does not make the agent magically understand your project. It gives the agent a better first path.

## When To Use It

Use Small DNL when:

- one repository is the main working surface
- agents keep asking the same orientation questions
- the project README is useful for humans but too broad for agent routing
- important code, domains, and runbooks are scattered across the repo
- you want the smallest possible DNL before building a larger knowledge hub

If your DNL needs to route across many repositories, use Umbrella DNL instead.

## Prefer Download ZIP

For Small DNL, downloading this starter as a zip is often more convenient than `git clone`.

The reason is simple: you are not starting a new repository. You are inserting DNL into an existing one.

A practical flow:

1. Download this repository as a zip.
2. Copy only the files and folders that help your project.
3. Delete examples, wrappers, or docs that do not match your workflow.
4. Add your own `DNL/` knowledge folder.
5. Update `dnl-config.toml` so DNL tools know what to scan.

Cloning is still fine if you want to study or fork the starter. For project insertion, zip-and-copy is usually cleaner.

## Minimum Operating Surface

These four pieces give the agent the DNL entrypoint, rules, tools, and scan configuration.

```text
AGENTS.md
dnl-config.toml
DNL-system/
.agents/skills/
```

### 1. `dnl-config.toml`

This is where DNL tooling starts.

It defines the repository name, scan surface, path tokens, QA profiles, and tag requirements. If a future DNL UI exists, this file is a natural place for that UI to discover the DNL project.

For the full field-by-field reference, read the [dnl-config.toml guide](dnl-config.md).

For a Small DNL, make sure your project knowledge folder is included:

```toml
[scan]
include = ["DNL-system", "DNL"]
exclude = [".git", ".repo-history"]
```

That is the first config change most Small DNL projects need.

### 2. `DNL-system/`

This folder gives the agent the operating rules.

It contains guidance for context loading, document selection, authoring, workflow, templates, and boundaries. Keep project-specific knowledge out of `DNL-system/`. Use it for how the DNL works, not what your product does.

### 3. `.agents/skills/`

This folder gives the agent reusable tools.

The important starter skills are:

- `dnl-builder`: authoring and QA support for DNL documents
- `dnl-query`: fast lookup by tags and paths
- `tree`: small, scoped structure inspection

Tool-specific folders such as `.cursor/`, `.claude/`, or `.github/` can wrap these skills, but `.agents/skills/` should stay the canonical source.

### 4. `AGENTS.md`

This is the AI entrypoint.

When an agent opens your project, `AGENTS.md` should tell it where the DNL starts, which system docs matter, and how to route public docs versus project knowledge.

For the full template and customization rules, read the [AGENTS.md customization guide](agents-md.md).

For a Small DNL, the most important instruction is:

```text
Start project navigation from DNL/README.md.
Use DNL-system/ only for DNL operating rules and maintenance guidance.
```

## Suggested Project Shape

After the operating surface is in place, add your actual project knowledge.

```text
your-project/
  README.md
  AGENTS.md
  dnl-config.toml
  DNL-system/
  .agents/
    skills/
  DNL/
    README.md
    maps/
      code-map.md
    domains/
      README.md
    runbooks/
      README.md
```

The `DNL/` folder name is only a suggestion. You can rename it if your project has a better convention, but keep the entrypoint obvious.

## Start With One Route

Do not document everything first.

Pick one real question that an agent should be able to answer faster:

```text
The login callback fails. Where should the agent start?
```

Then create only the documents needed for that route:

```text
DNL/README.md
DNL/maps/code-map.md
DNL/domains/auth.md
DNL/runbooks/login-callback.md
```

That first route is more valuable than a large empty hierarchy.

## What Each First File Does

`DNL/README.md` is the project navigation portal.

It should answer:

- what this project is
- what the main domains are
- where code maps live
- where runbooks live
- where current work or future notes should go

`DNL/maps/code-map.md` connects domain words to code locations.

It should answer:

- where the main modules live
- which files are good entrypoints
- which generated, build, or vendor folders should be skipped

`DNL/domains/auth.md` explains one domain in project language.

It should answer:

- what the domain means in this project
- which workflows matter
- which code, APIs, screens, or tests are related

`DNL/runbooks/login-callback.md` gives one repeatable investigation path.

It should answer:

- what to inspect first
- which logs, commands, or files matter
- what evidence should be collected before changing code

## Agent Prompt Example

You can ask an agent to help create the first route:

```text
We are adding a Small DNL to this project.

Before writing, read AGENTS.md and DNL-system/authoring/README.md.

Create a first DNL route for this question:
"The login callback fails. Where should an agent start?"

Use this shape:
- DNL/README.md
- DNL/maps/code-map.md
- DNL/domains/auth.md
- DNL/runbooks/login-callback.md

Keep the documents short. Do not invent facts. If code evidence is missing, say what needs to be inspected.
```

## What Not To Do

- Do not copy every folder just because the starter includes it.
- Do not build a company/product/project hierarchy unless your project actually needs it.
- Do not put project-specific domain knowledge inside `DNL-system/`.
- Do not document every file before the first route works.
- Do not assume the agent will place new knowledge correctly without explicit routing.
- Do not overwrite your existing project README unless you really want DNL to become the public project entrypoint.

## When To Grow

Grow the DNL only when repeated work proves the need.

Good next additions:

- `DNL/future/` for rough design notes and not-yet-promoted knowledge
- `DNL/glossary/` for project-specific terms
- `DNL/screens/` when UI flows are important
- `DNL/apis/` when API contracts are central
- more runbooks for repeated failures

If the DNL starts routing across several repositories, split it into an Umbrella DNL.
