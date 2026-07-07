# Working

This folder is the shared active work area for a DNL repository.

Use it for rough source material that humans and agents are still shaping:

- investigation notes
- design drafts
- decision logs
- AI collaboration notes
- promotion candidates that are not canonical DNL yet

`working/` is not canonical DNL. It is source material.
Reusable knowledge should be promoted into DNL through the workflow rules in `DNL-system/workflow/`.

## Active work index

Group active bundles by lifecycle Type.
Add each bundle under the matching heading:

```text
working/{working-name}/README.md
```

## Domain Work (`domain-work`)

Use this section for work where the real subject lives in an external product, domain, project, source repository, or documentation area.
The working bundle preserves source material until reusable knowledge is promoted.

- None by default.

## DNL Internal Work (`dnl-internal`)

Use this section for work where the task itself changes this DNL repository.
The output is usually a DNL-system, authoring, workflow, template, or DNL document change.

- None by default.

## Recurring Work (`recurring`)

Use this section for work that repeats over time.
Recurring bundles review source changes in batches, promote useful findings, record the cursor, and then return to `not-ready` for the next run.

- None by default.

Each bundle can choose its own substructure.
Keep the first README short enough that another person or agent can understand the work quickly.

## Bundle Type

Use these Type values:

| Type | Meaning |
| --- | --- |
| `domain-work` | Source material for work whose subject is outside the DNL repository. |
| `dnl-internal` | Work whose output is a DNL repository change. |
| `recurring` | Repeated batch work that keeps a cursor and batch log. |

If Type is omitted, read the bundle as `domain-work`.
Write `Type:` explicitly for `dnl-internal` and `recurring`.

## DNL Status values

Use only these minimal promotion signals:

| Value | Meaning |
| --- | --- |
| `not-ready` | Do not promote yet. |
| `ready` | Review as a DNL promotion candidate. |
| `promoting` | Someone is currently promoting it into DNL. |
| `promoted` | DNL promotion and route rewiring are complete. |

For `recurring`, `DNL Status` describes the current batch.
After a normal recurring batch, record the cursor and batch log, then return the bundle to `not-ready`.
Use `promoted` only when the recurring mission itself has retired.

`archived` is not a status value.
If a raw bundle has moved to `.working-archive/`, it is archived by location.

## Read the rules

- `DNL-system/workflow/working-authoring-rule.md`
- `DNL-system/workflow/working-to-dnl.md`
- `DNL-system/workflow/working-to-archive.md`
