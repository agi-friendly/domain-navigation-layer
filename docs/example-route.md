# Example Route

This example shows the smallest useful DNL move:

```text
entrypoint -> router -> domain page -> runbook or source path
```

Use it as a pattern, not a required folder hierarchy.

## Scenario

An agent receives this task:

```text
"The login callback fails. Where should the agent start?"
```

Without DNL, the agent may search the whole repository and guess which files matter.

With DNL, the agent follows a route.

## Minimal Files

For a Small DNL inside one project, the first route might use:

```text
AGENTS.md
DNL/README.md
DNL/maps/code-map.md
DNL/domains/auth.md
DNL/runbooks/login-callback.md
```

`PATHS.md` is optional when all source code lives in the same repository. Use it when a route needs local source paths outside the DNL repository.

## The Route

The route can be this small:

```text
AGENTS.md
  -> DNL/README.md
  -> DNL/domains/auth.md
  -> DNL/runbooks/login-callback.md
  -> DNL/maps/code-map.md
  -> source path or PATHS.md token
```

Each step has one job.

| Step | What it tells the agent |
| --- | --- |
| `AGENTS.md` | Start with the DNL before searching source code |
| `DNL/README.md` | This project has an `auth` domain and login runbooks |
| `DNL/domains/auth.md` | What "auth" means in this project and which flows matter |
| `DNL/runbooks/login-callback.md` | What evidence to collect before changing code |
| `DNL/maps/code-map.md` | Which source files or directories are good entrypoints |
| Source path or token | Where code inspection begins |

## Example Source Pointer

If the source lives in the same repository, the code map can point to a local source path:

```text
src/routes/auth/
src/services/session/
tests/auth/
```

If the source lives in another repository, keep the machine-specific path in `PATHS.md`:

```text
- {@webapp} :: /Users/you/work/platform-webapp
```

Then the DNL route can say:

```text
Inspect {@webapp}/src/routes/auth before changing callback logic.
```

## What To Avoid

- Do not document every module before the first route works.
- Do not invent source paths that have not been checked.
- Do not make DNL a second README for humans.
- Do not turn one routing question into a full company taxonomy.

The first route is successful when the next agent knows where to start and what evidence to collect.

## Read Next

- [Getting started](getting-started.md)
- [Small DNL](small-dnl.md)
- [Umbrella DNL](umbrella-dnl.md)
