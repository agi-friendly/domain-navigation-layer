# Example Route

This page explains the route implemented in `DNL-example/`.

The smallest useful DNL move is:

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

With DNL, the agent follows the example route in `DNL-example/`.

## Minimal Files

The working example in this starter uses:

```text
AGENTS.md
DNL-example/README.md
DNL-example/maps/code-map.md
DNL-example/domains/auth.md
DNL-example/runbooks/login-callback.md
```

`DNL-example/` is an example root name, not a required folder name.

When adapting it to a real project, choose your own DNL root name and update `AGENTS.md` plus `dnl-config.toml` to match.

`PATHS.md` is optional when all source code lives in the same repository. Use it when a route needs local source paths outside the DNL repository.

## The Route

The route can be this small:

```text
AGENTS.md
  -> DNL-example/README.md
  -> DNL-example/domains/auth.md
  -> DNL-example/runbooks/login-callback.md
  -> DNL-example/maps/code-map.md
  -> source path or PATHS.md token
```

Each step has one job.

| Step | What it tells the agent |
| --- | --- |
| `AGENTS.md` | Start with the DNL before searching source code |
| `DNL-example/README.md` | The example has an `auth` domain and login runbook |
| `DNL-example/domains/auth.md` | What "auth" means in the example project and which flows matter |
| `DNL-example/runbooks/login-callback.md` | What evidence to collect before changing code |
| `DNL-example/maps/code-map.md` | Which source files or directories are good entrypoints |
| Source path or token | Where code inspection begins |

## Working Example Files

The starter includes these files:

- `DNL-example/README.md`
- `DNL-example/domains/auth.md`
- `DNL-example/runbooks/login-callback.md`
- `DNL-example/maps/code-map.md`

Keep your first real route about this small. Add detail only when repeated work proves it is useful.

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
