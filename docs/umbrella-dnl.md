# Umbrella DNL

Umbrella DNL is the multi-repository shape.

Use it when the DNL repository is not the source repository itself. It is a separate knowledge hub that routes agents across products, projects, source repositories, working notes, and local paths.

Small DNL helps one repository stop feeling blind.
Umbrella DNL helps a whole workspace stop feeling scattered.

## When To Use It

Use Umbrella DNL when:

- one product is made from several repositories
- one company or team works across many projects
- the important context is spread across backend, frontend, database, docs, and operations repos
- the same agent needs to move between product knowledge and source code
- source repositories have useful docs, but no single cross-repository map
- you want a durable AI-first knowledge hub outside the code repositories

Umbrella DNL is often the better long-term shape when your real work crosses repository boundaries.

## Small DNL vs Umbrella DNL

| Shape | Where it lives | Best for |
| --- | --- | --- |
| Small DNL | inside one existing project repository | one repo, one first route, small adoption |
| Umbrella DNL | in a separate knowledge repository | many repos, product ecosystems, cross-project routing |

Small DNL is the fastest way to begin.
Umbrella DNL is the strongest shape when the agent must understand a workspace, not only one repository.

## Core Contract

An Umbrella DNL has two kinds of paths:

```text
DNL document paths
source repository paths
```

DNL document paths live inside the Umbrella DNL repository.
Source repository paths usually live outside it and are mapped through `PATHS.md`.

The agent starts in the Umbrella DNL, then follows the route:

```text
AGENTS.md
  -> DNL-system/README.md
  -> DNL-Company/README.md
  -> products/DNL-product-*/README.md
  -> products/DNL-product-*/projects/DNL-*/README.md
  -> PATHS.md token
  -> real source repository
```

The exact folders are yours. The route is the important part.

## Recommended Structure

Start with a small but explicit shape:

```text
workspace-dnl/
  README.md
  AGENTS.md
  PATHS.md
  dnl-config.toml
  DNL-system/
  DNL-Company/
  products/
    DNL-product-platform/
      README.md
      maps/
      infra/
      data/
      ddl/
      projects/
        DNL-webapp/
          README.md
        DNL-api-server/
          README.md
  future/
```

You do not need every folder on day one.

A good first Umbrella DNL can be only:

```text
workspace-dnl/
  README.md
  AGENTS.md
  PATHS.md
  dnl-config.toml
  DNL-system/
  DNL-Company/
  products/
    DNL-product-platform/
      README.md
      projects/
        DNL-webapp/
          README.md
```

The first useful route matters more than a complete hierarchy.

## Recommended Naming Pattern

For Umbrella DNL, use `DNL-` prefixes for DNL document layers.

Recommended:

```text
DNL-Company/
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
      DNL-api-server/
```

The prefix is a signal:

```text
DNL-* means "this is a DNL document layer inside the Umbrella DNL."
No DNL prefix usually means "this may be a real source repository token."
```

This is especially useful in path tokens.

Example:

```text
{@DNL-webapp} -> products/DNL-product-platform/projects/DNL-webapp
{@webapp}     -> /Users/you/work/webapp
```

The first token points to DNL knowledge.
The second token points to source code.

That distinction helps both humans and agents.

## Product-Level DNL

The product layer is not only a folder between company and project.

It is the place for ecosystem knowledge that is too specific for company-level docs and too broad for one project.

Good product-level documents:

- product overview
- project roles and boundaries
- cross-project dependency map
- shared architecture notes
- common infrastructure
- deployment topology
- database and DDL references
- shared glossary
- version policy
- migration plans
- product-level runbooks
- future design notes

Example:

```text
products/
  DNL-product-platform/
    README.md
    maps/
      project-map.md
      dependency-map.md
    infra/
      environments.md
      deployment.md
    data/
      database-map.md
    ddl/
      README.md
    projects/
      DNL-webapp/
      DNL-api-server/
```

If a fact explains how several projects work together, the product layer is often the right home.

## Project-Level DNL

Project DNLs explain one source repository or one deployable unit.

Good project-level documents:

- project overview
- source map
- module map
- domain map
- API map
- screen map
- runbooks
- coding rules
- testing notes
- local build notes

Example:

```text
products/
  DNL-product-platform/
    projects/
      DNL-webapp/
        README.md
        maps/
          source-map.md
        domains/
          auth.md
        runbooks/
          login-callback.md
```

The project DNL should not copy every source file.
It should tell the agent where to start and what to inspect next.

## PATHS.md

`PATHS.md` maps DNL tokens to real local paths.

It is usually local, private, and gitignored.

Example:

```text
- {@webapp} :: /Users/you/work/platform-webapp
- {@api-server} :: /Users/you/work/platform-api-server
- {@database-repo} :: /Users/you/work/platform-database
```

The same Umbrella DNL can work on different machines because each person can keep their own `PATHS.md`.

Use `PATHS.md` for:

- external source repositories
- local worktrees
- private checkout paths
- machine-specific folders
- temporary investigation roots

Do not put private absolute paths into public DNL docs.

## DNL Tokens vs Source Tokens

Use different token names for DNL docs and source repos.

Recommended:

```text
{@DNL-product-platform} -> products/DNL-product-platform
{@DNL-webapp}           -> products/DNL-product-platform/projects/DNL-webapp
{@webapp}               -> /Users/you/work/platform-webapp
```

Then DNL documents can say:

```text
Start at {@DNL-webapp}/README.md.
When code evidence is needed, inspect {@webapp}/src.
```

This keeps the route clear:

```text
DNL first, source code second.
```

## dnl-config.toml Starting Point

For an Umbrella DNL, include the DNL knowledge layers:

```toml
[scan]
include = ["DNL-system", "DNL-Company", "products"]
exclude = [".git", ".repo-history", "CURRENT_WORKING"]

[paths.internal]
"dnl-root" = "."
"DNL-system" = "DNL-system"
"DNL-Company" = "DNL-Company"
"DNL-product-platform" = "products/DNL-product-platform"
"DNL-webapp" = "products/DNL-product-platform/projects/DNL-webapp"
"DNL-api-server" = "products/DNL-product-platform/projects/DNL-api-server"

[paths.external]
"webapp" = { required = false, validate = "if-defined" }
"api-server" = { required = false, validate = "if-defined" }
```

Use `paths.internal` for DNL folders in the Umbrella DNL repository.
Use `paths.external` and `PATHS.md` for source repositories outside it.

For the field-by-field reference, read the [dnl-config.toml guide](dnl-config.md).

## Worktrees

Worktrees can work well with Umbrella DNL, but they are an advanced local detail.

Keep the public DNL route stable first.
Then add local tokens when worktrees matter.

Example `PATHS.md`:

```text
- {@webapp} :: /Users/you/work/platform-webapp
- {@webapp-auth-fix} :: /Users/you/work/platform-webapp.worktrees/auth-fix
- {@api-server} :: /Users/you/work/platform-api-server
```

Use worktree tokens when the task depends on a specific checkout.
Do not make every branch part of the public DNL structure.

## First Route Example

Start with one real cross-repository question:

```text
"The login callback fails. Which repositories and documents should the agent inspect first?"
```

A first Umbrella route might be:

```text
DNL-Company/README.md
  -> products/DNL-product-platform/README.md
  -> products/DNL-product-platform/projects/DNL-webapp/README.md
  -> products/DNL-product-platform/projects/DNL-api-server/README.md
  -> PATHS.md tokens: {@webapp}, {@api-server}
```

Write only enough Markdown to answer that route.

Do not begin by documenting every project.

## What Goes Where

Use this as a placement guide:

| Layer | Put here |
| --- | --- |
| `DNL-system/` | DNL operating rules, AI loading, authoring, workflow, templates |
| `DNL-Company/` | company-wide glossary, product map, team map, cross-product entrypoints |
| `DNL-product-*` | product ecosystem, shared architecture, infra, DDL, project boundaries |
| `DNL-project-*` or `DNL-<repo>` | one repository or deployable unit |
| `future/` | rough ideas, investigation notes, not-yet-promoted design work |
| `PATHS.md` | local machine paths and source repository mappings |

The names can change. The responsibility boundaries matter more than the exact folder names.

## Prompt To Create An Umbrella DNL

You can ask an agent:

```text
We are creating an Umbrella DNL for a multi-repository workspace.

Before writing, read:
- AGENTS.md
- docs/umbrella-dnl.md
- docs/dnl-config.md
- docs/agents-md.md
- DNL-system/authoring/README.md

Goal:
Create the first useful route for this workspace.

Use this convention:
- DNL document layers use the `DNL-` prefix.
- Product-level DNL folders use `DNL-product-*`.
- Project-level DNL folders use `DNL-*`.
- Source repository tokens do not use the `DNL-` prefix.
- Real local source paths belong in PATHS.md, not public docs.

Start with one real question:
<write the first routing question here>

Do not document everything.
Do not invent source paths.
If a repository path is missing, say which PATHS.md token is needed.
```

## Common Mistakes

### Starting With Every Repository

Start with one route. Add projects as repeated work proves they need a stable DNL entrypoint.

### Mixing DNL Paths And Source Paths

Use `DNL-` prefixes for DNL document layers and non-prefixed tokens for source repos.

### Making Product DNL Empty Forever

The product layer is where cross-project knowledge belongs. If several projects share infrastructure, DDL, deployment rules, or glossary terms, product-level DNL is a good home.

### Putting Local Paths In Public Docs

Use `PATHS.md` for machine-specific paths.

### Treating Future As Current Truth

Use `future/` for rough work. When it becomes stable knowledge, promote it into the appropriate company, product, or project DNL route.

## Read Next

- [Getting started](getting-started.md)
- [Small DNL](small-dnl.md)
- [AGENTS.md customization guide](agents-md.md)
- [dnl-config.toml guide](dnl-config.md)
- [DNL-system customization guide](dnl-system.md)
