# DNL-system Customization Guide

`DNL-system/` is the operating layer for a DNL repository.

It should explain how agents load context, choose documents, write DNL docs, handle workflow state, use templates, and respect boundaries. It should not become the place where you store project facts.

Use this rule:

```text
DNL-system explains how the DNL works.
DNL or product/project layers explain what the project knows.
```

## What DNL-system Is For

Use `DNL-system/` for rules that should apply across the repository:

- AI context loading
- document selection
- output format expectations
- authoring rules
- YAML frontmatter rules
- path token rules
- workflow lifecycle rules
- prompt and output templates
- allowed and forbidden actions
- repository-local context guides

If a rule should guide every agent in the repository, it probably belongs in `DNL-system/`.

## What Not To Put Here

Do not put these in `DNL-system/`:

- product features
- module maps
- API details
- screen flows
- project-specific domain explanations
- current task notes
- local machine paths
- team-specific exceptions that only apply to one project

Those belong in the project DNL, an umbrella knowledge layer, `PATHS.md`, or a local/current-work file.

## Directory Roles

The public starter uses this shape:

```text
DNL-system/
  README.md
  ai/
  authoring/
  workflow/
  templates/
  boundaries/
```

| Directory | Role |
| --- | --- |
| `DNL-system/README.md` | System portal and next-route map |
| `DNL-system/ai/` | How agents load, select, and report context |
| `DNL-system/authoring/` | How DNL documents are written and validated |
| `DNL-system/workflow/` | How rough work becomes reusable knowledge or archive material |
| `DNL-system/templates/` | Reusable request and output templates |
| `DNL-system/boundaries/` | Allowed actions, forbidden actions, assumptions, and safety rules |

Keep this structure unless your repository has a clear reason to rename it.

## Small DNL Starting Point

For a Small DNL, keep `DNL-system/` mostly as-is at first.

The first useful customization is usually not rewriting system rules. It is making sure `AGENTS.md` routes agents into:

```text
AGENTS.md
  -> DNL-system/README.md
  -> DNL/README.md
```

Then update `dnl-config.toml` so the system layer and project knowledge layer are both scanned:

```toml
[scan]
include = ["DNL-system", "DNL"]
```

Only customize `DNL-system/` when repeated use shows that the default rule is too vague, too strict, or missing an important operating boundary.

## What To Customize First

### 1. `ai/`

Customize `DNL-system/ai/` when the agent needs clearer operating behavior.

Good reasons:

- The agent loads too much context.
- The agent skips the DNL route and searches randomly.
- The agent mixes public docs with AI operating docs.
- The agent answers without naming the layer or evidence it used.

Common files:

- `context-loading.md`: what to read first and when to stop
- `doc-selection-rules.md`: how to choose the next document
- `output-format.md`: how to structure answers
- `guardrails.md`: global safety behavior
- `prompt-playbook.md`: reusable prompting patterns
- `local-context/`: how to use local files such as `PATHS.md` or `CURRENT_USER.md`

Keep these rules general. If only one project needs an exception, write a project-level override instead.

### 2. `authoring/`

Customize `DNL-system/authoring/` when the way DNL documents are written needs to change.

Good reasons:

- You want stricter YAML frontmatter rules.
- You want different required tags.
- You need a new DNL writing playbook.
- You need a clear override rule for layered DNLs.

Be careful here. Authoring rules affect every scanned DNL document.

If you change authoring rules, also check:

- `dnl-config.toml`
- `.agents/skills/dnl-builder/qa.py`
- `.agents/skills/dnl-builder/dnl_util.py`
- generated tag/link indexes

Do not change authoring rules just to fix one awkward document. Fix the document first.

### 3. `workflow/`

Customize `DNL-system/workflow/` when your repository needs a clearer lifecycle.

Good reasons:

- You use `future/` for rough design notes.
- You need rules for promoting notes into stable DNL docs.
- You need archive rules.
- You need repository history separate from public docs.

The useful question is:

```text
Is this note active work, reusable knowledge, archived material, or repository history?
```

If the answer is unclear often, improve workflow docs.

### 4. `templates/`

Customize `DNL-system/templates/` when repeated prompts or outputs should become standard.

Good reasons:

- You repeatedly ask agents to create DNL docs.
- You want a standard review format.
- You want a safer request format for doc promotion.
- You want humans and agents to use the same input shape.

Templates should be short. A template should reduce ambiguity, not become a policy essay.

### 5. `boundaries/`

Customize `DNL-system/boundaries/` when agents need clearer safety limits.

Good reasons:

- Some actions should always be allowed.
- Some actions should always require confirmation.
- Some assumptions should be stated before work starts.
- Agents are repeatedly making the same risky guess.

Boundary docs should be explicit and boring.

Good:

```md
- Do not invent file paths that are not present in the repository or local context.
```

Risky:

```md
- Be careful with paths.
```

## Project-Specific Overrides

Do not edit global `DNL-system/` rules for one project-specific exception.

Use a project-level override pattern:

```text
DNL/
  ai/
    README.md
    overrides.md
```

The project `ai/README.md` can say:

```md
The global AI rules live in DNL-system/ai.
This project only adds the overrides in overrides.md.
```

The override file should be explicit:

```md
Override:
For this project only, load DNL/apis/README.md before DNL/screens/README.md when the task is about API-driven screens.
```

If there is no explicit override, global `DNL-system/` rules win.

## Safe Customization Order

Use this order:

1. Customize `AGENTS.md` so the agent reaches `DNL-system/README.md`.
2. Customize `dnl-config.toml` so the right folders are scanned.
3. Add your project knowledge layer, such as `DNL/README.md`.
4. Use the default `DNL-system/` rules for a while.
5. Add project-level overrides for one-off exceptions.
6. Change global `DNL-system/` rules only when the rule should apply everywhere.

This order keeps the system reusable.

## How To Prune The Starter

You can delete parts you do not use, but keep the routing coherent.

For a minimal Small DNL, keep:

```text
DNL-system/README.md
DNL-system/ai/context-loading.md
DNL-system/ai/doc-selection-rules.md
DNL-system/authoring/README.md
DNL-system/authoring/rules/
DNL-system/authoring/dnl-authoring-playbook.md
```

Recommended to keep:

```text
DNL-system/workflow/
DNL-system/templates/
DNL-system/boundaries/
```

If you delete a folder, also update:

- `DNL-system/README.md`
- `AGENTS.md`
- `dnl-config.toml`
- generated link index

Do not leave a portal pointing at a deleted document.

## Common Mistakes

### Putting project knowledge into DNL-system

Move project facts into `DNL/`, `products/`, `projects/`, or another knowledge layer.

### Rewriting global rules too early

Use the default rules first. Change global rules only after real usage exposes a repeatable problem.

### Copying DNL-system into every project

If one umbrella DNL routes many projects, keep one system layer and add project-level overrides where needed.

### Deleting a folder without rewiring the portal

Every deleted route needs a parent route update.

### Making hidden local files public

Do not put machine-specific paths or current-user handoff into public `DNL-system/` docs.
Use `PATHS.md`, `CURRENT_USER.md`, or another local context file.

## Prompt To Customize DNL-system

You can ask an agent:

```text
We are customizing DNL-system for this repository.

Before editing, read:
- AGENTS.md
- docs/dnl-system.md
- docs/agents-md.md
- docs/dnl-config.md
- DNL-system/README.md
- DNL-system/authoring/README.md

Goal:
Make DNL-system fit this repository without adding project-specific domain knowledge to it.

Rules:
- Keep DNL-system as the global operating layer.
- Put project facts in DNL/ or the appropriate knowledge layer.
- Use project-level overrides for one-project exceptions.
- Update DNL-system/README.md when routes change.
- Update dnl-config.toml if scan scope changes.
- Rebuild/check link index when DNL paths change.
```

## Verify

After changing `DNL-system/`, run:

```bash
python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all --json-summary
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all --json-summary
python3 .agents/skills/dnl-builder/dnl_util.py tag index check
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```

If an index is stale, rebuild it:

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py link index build
```

Then run the checks again.

## Read Next

- [AGENTS.md customization guide](agents-md.md)
- [dnl-config.toml guide](dnl-config.md)
- [Small DNL](small-dnl.md)
- [Repository layout](repository-layout.md)
