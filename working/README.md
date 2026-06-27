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

Add active bundles here:

```text
working/{working-name}/README.md
```

Each bundle can choose its own substructure.
Keep the first README short enough that another person or agent can understand the work quickly.

## DNL Status values

Use only these minimal promotion signals:

| Value | Meaning |
| --- | --- |
| `not-ready` | Do not promote yet. |
| `ready` | Review as a DNL promotion candidate. |
| `promoting` | Someone is currently promoting it into DNL. |
| `promoted` | DNL promotion and route rewiring are complete. |

`archived` is not a status value.
If a raw bundle has moved to `.working-archive/`, it is archived by location.

## Read the rules

- `DNL-system/workflow/working-authoring-rule.md`
- `DNL-system/workflow/working-to-dnl.md`
- `DNL-system/workflow/working-to-archive.md`
