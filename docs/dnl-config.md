# dnl-config.toml Guide

`dnl-config.toml` is the project map for DNL tooling.

It tells the tools which Markdown files belong to the DNL, which folders should be ignored, which path tokens are known, which QA profiles exist, and which tags are required for certain documents.

It does not define what DNL means. It does not force a folder hierarchy. It is the configuration surface that lets the same DNL tools work in many repository shapes.

## Who Uses This File

The current public tools use `dnl-config.toml` in these places:

| Tool | What it reads |
| --- | --- |
| `qa.py --profile full` | `scan.include`, `scan.exclude`, required tag rules |
| `qa.py --profile portal` | `profiles.portal`, `scan.exclude`, `portal.readme_dirs` |
| `qa.py --profile links` | `profiles.links`, `scan.exclude` |
| `qa.py --profile health` | generated link-index manifest only |
| `dnl_util.py tag add` | `scan.include`, `scan.exclude` |
| `dnl_util.py tag index build/check/update` | `scan.include`, `scan.exclude` |
| `dnl_util.py link index build/check` | `scan.include`, `scan.exclude`, `paths.internal`, `paths.external` |
| `dnl_query.py` | generated tag/link indexes, not `dnl-config.toml` directly |

The important pattern is:

```text
dnl-config.toml -> dnl-builder tools -> generated indexes -> dnl-query
```

## Starter Repository Note

This starter repository scans two roots by default:

```toml
[scan]
include = ["DNL-system", "DNL-example"]
```

`DNL-system/` is the operating layer. `DNL-example/` is the small working example route.

When adapting the starter to a real project, replace or rename `DNL-example/` with your chosen project knowledge root and update this config to match.

## Small DNL Starting Point

For a Small DNL inserted into one existing project, start with this shape:

```toml
[dnl]
version = "0.1"
name = "your-project-dnl"

[scan]
include = ["DNL-system", "DNL"]
exclude = [".git", "node_modules", ".repo-history", "target", "dist", "build"]

[paths.internal]
"dnl-root" = "."
"DNL-system" = "DNL-system"
"DNL" = "DNL"

[paths.external]

[profiles]
portal = [
  "DNL",
  "DNL-system/README.md",
  "AGENTS.md",
]
links = [
  "DNL",
  "DNL-system",
  "AGENTS.md",
]

[portal]
readme_dirs = [
  "maps",
  "domains",
  "runbooks",
  "future",
  "glossary",
]

[tags.required_by_filename]
"README.md" = ["portal-dnl"]

[tags.required_by_path]
"DNL-system/authoring/rules/*.md" = ["rule-dnl"]
"DNL/runbooks/*.md" = ["runbook-dnl"]
```

Then run:

```bash
python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all
```

If you have no `DNL/` folder yet, keep `include = ["DNL-system"]` until you create it.
If your `DNL/` folder still contains rough plain Markdown, add frontmatter before including it in the scan.

## `[dnl]`

This section names the DNL project.

```toml
[dnl]
version = "0.1"
name = "domain-navigation-layer"
```

Current fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `version` | string | DNL configuration version label. Current starter value is `"0.1"`. |
| `name` | string | Human-readable project name parsed by the config loader. |

If the section is missing, the tools use default values.

## `[scan]`

This is the most important section.

```toml
[scan]
include = ["DNL-system", "DNL"]
exclude = [".git", "node_modules", ".repo-history"]
```

`include` is the list of repository-relative files or folders that DNL tooling should scan.

Used by:

- full QA
- tag add
- tag index build/check/update
- link index build/check

`exclude` is a list of directory names to ignore anywhere under the included paths.

Important details:

- `include` can point to directories or Markdown files.
- Missing include paths are skipped.
- `exclude` matches directory names, not glob patterns.
- Hidden directories such as `.agents/` are not normal DNL search targets.
- `SKILL.md` files are excluded by policy even when they appear under an included folder.
- Root-level public docs such as `README.md` and `docs/` can stay outside `scan.include` if they are reader-facing docs rather than canonical DNL documents.
- Once a folder is in `scan.include`, its Markdown files are expected to follow DNL frontmatter and link rules.

For Small DNL, the key move is:

```toml
[scan]
include = ["DNL-system", "DNL"]
```

That tells the tools to validate both the operating rules and your project knowledge folder.

## `[paths.internal]`

Internal paths define logical variables for files and folders inside the same repository.

```toml
[paths.internal]
"dnl-root" = "."
"DNL-system" = "DNL-system"
"DNL" = "DNL"
```

These variables are used by DNL YAML frontmatter paths:

```yaml
paths:
  "@auth.md": "{@DNL}/domains/auth.md"
```

Current behavior:

- `{@dnl-root}` always resolves to the repository root.
- Internal targets are checked by the link index.
- If the resolved target does not exist, link health reports `target-not-found`.
- Internal path names are case-sensitive.

Use internal paths for stable DNL folders that may be referenced from many documents.

## `[paths.external]`

External paths declare logical variables for repositories or folders outside this DNL repository.

```toml
[paths.external]
"backend" = { required = false, validate = "if-defined" }
"frontend" = { required = false, validate = "if-defined" }
```

These variables let DNL documents refer to external workspaces:

```yaml
paths:
  "@backend-auth-service": "{@backend}/src/auth/AuthService.ts"
```

Current behavior:

- The link index classifies these targets as `external`.
- External targets are not checked on disk by the current public tooling.
- `required` and `validate` are parsed as metadata, but the current public implementation does not enforce local external path existence.
- Real machine-specific paths should usually live in local context such as `PATHS.md`, not in the public config.

Use external paths when a DNL needs to point across repositories.
For a Small DNL inside one repository, you can often leave this section empty.

## `[profiles]`

Profiles define named scan presets for QA.

```toml
[profiles]
portal = [
  "DNL",
  "DNL-system/README.md",
  "AGENTS.md",
]
links = [
  "DNL",
  "DNL-system",
  "AGENTS.md",
]
```

Current built-in profiles:

| Profile | Used by | Purpose |
| --- | --- | --- |
| `full` | `qa.py --profile full` | Uses `scan.include`; this profile is not configured under `[profiles]`. |
| `portal` | `qa.py --profile portal` | Focuses on entrypoint and router documents. |
| `links` | `qa.py --profile links` | Focuses on link-related QA over a configured subset. |
| `health` | `qa.py --profile health` | Reads generated link-index counts and reports them without failing. |

Important details:

- `[profiles]` entries can point to folders or Markdown files.
- If you define one profile, the other built-in profiles still keep their defaults.
- `profiles.portal` does not control full QA or index generation.
- `profiles.links` does not build the link index. It only changes the QA scan preset.

For Small DNL, `portal = ["DNL", "DNL-system/README.md", "AGENTS.md"]` is a good first setting.

## `[portal]`

This section controls which README directories count as portal README documents during portal QA.

```toml
[portal]
readme_dirs = [
  "maps",
  "domains",
  "runbooks",
]
```

Portal README documents are expected to declare navigation paths in YAML frontmatter.
If a portal README has no YAML `paths` declaration, portal QA reports it.

Current behavior:

- This setting only applies inside the `profiles.portal` scan surface.
- It does not add files to the scan by itself.
- It checks README files in directories with matching names.

For example, if `profiles.portal` includes `DNL` and `readme_dirs` includes `runbooks`, then `DNL/runbooks/README.md` is treated as a portal README.

## `[tags.required_by_filename]`

This section requires tags for files with a specific filename.

```toml
[tags.required_by_filename]
"README.md" = ["portal-dnl"]
```

Current behavior:

- QA applies the rule to scanned DNL documents.
- The rule is filename-based.
- It is commonly used to require `portal-dnl` on every scanned `README.md`.

This helps agents find router documents through tag search.

## `[tags.required_by_path]`

This section requires tags for files that match a repository-relative path pattern.

```toml
[tags.required_by_path]
"DNL-system/authoring/rules/*.md" = ["rule-dnl"]
"DNL/runbooks/*.md" = ["runbook-dnl"]
```

Current behavior:

- QA uses `fnmatch`-style path matching.
- Matching paths are repository-relative and normalized with `/`.
- Required tags from filename and path rules are combined.
- Duplicate required tags are de-duplicated.

Use this for folders where the document role is predictable.

## What This File Does Not Do

`dnl-config.toml` does not:

- create folders
- make an agent read documents automatically
- replace `AGENTS.md`
- replace local `PATHS.md`
- enforce the whole DNL hierarchy
- validate external repositories on disk in the current public tooling
- change the core YAML frontmatter schema

The schema rules still live in the DNL authoring rules and the tool code.

## Common Mistakes

### Adding a folder but forgetting `scan.include`

If you create `DNL/` but do not add it to `scan.include`, full QA and tag/link indexes will ignore it.

### Adding `paths.internal` without a real target

Internal paths are checked by link health. If `{@DNL}` points to `DNL` but that folder does not exist, related links can report `target-not-found`.

### Expecting `[portal]` to scan new folders

`portal.readme_dirs` only classifies README files inside the portal profile scan surface.
Add the folder to `profiles.portal` first.

### Treating external paths as local filesystem paths

External path variables are logical names. Keep machine-specific paths in local context, usually `PATHS.md`.

### Scanning public docs accidentally

Reader-facing docs can use normal Markdown links. Canonical DNL docs should use YAML `paths` and `@tokens`.

If you add `docs/` to `scan.include`, those docs become part of DNL QA rules.

## Verify The Config

Use these commands after changing `dnl-config.toml`:

```bash
python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all --json-summary
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all --json-summary
python3 .agents/skills/dnl-builder/dnl_util.py tag index check
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```

If the indexes are stale, rebuild them:

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py link index build
```

Then run the checks again.

## Read Next

- [Small DNL](small-dnl.md)
- [Repository layout](repository-layout.md)
- [Getting started](getting-started.md)
