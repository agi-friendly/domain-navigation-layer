---
name: "dnl-structure"
status: "draft"
tags: ["map-dnl", "reference-dnl", "dnl-builder", "rule-dnl"]
paths: {}
---

# dnl-structure

This document defines the default folder responsibilities for a public DNL repository.

## Default structure

```text
README.md                          # public landing page
docs/                              # public explanation and onboarding pages
  index.md                         # docs hub
  core-concept.md                  # conceptual overview
  getting-started.md               # first steps
  repository-layout.md             # folder map

DNL-system/                        # system, authoring, and workflow rules
  README.md                        # maintenance portal
  ai/
  authoring/
  workflow/
  boundaries/
  templates/

.agents/skills/                    # tool entrypoints used by agents
  dnl-builder/
  dnl-query/
  tree/

scripts/dnl/                       # official portable DNL executables and guides
  query.py
  query.md
  tree.py
  tree.md
  requirements.txt

tests/dnl/                         # portable tooling tests

.repo-history/                     # repository history and migration notes
```

## Optional domain layers

Some repositories also use a layered domain structure.
When they do, use placeholder names in examples:

```text
example-company/
  README.md
  glossary/
  maps/
  status/

sample-product/
  README.md
  projects/
    sample-project/
      README.md
```

## Responsibility split

- `README.md` gives the shortest public overview.
- `docs/` holds the public explanation and onboarding flow.
- `DNL-system/` holds the rules that keep the documentation layer coherent.
- `scripts/dnl/` holds portable DNL executables and detailed guides shared by people and agents.
- `.agents/skills/` holds thin agent behavior guides and compatibility shims, plus builder-specific maintenance that has not been extracted into a portable core.
- `tests/dnl/` holds portable DNL tooling tests.
- `.repo-history/` stores historical context separately from the main docs.
- Optional domain layers such as `example-company` and `sample-product` belong to the repository-specific knowledge tree, not the public landing page.

## Authoring rule

Documentation work should start from the repository landing page and docs index.
If the task is about maintaining DNL itself, read `DNL-system/README.md` first.
Only move into optional domain layers after the target layer is known.

The official query and tree commands use `scripts/dnl`.
Legacy executable paths under `.agents/skills/dnl-query` and `.agents/skills/tree` are compatibility shim surfaces only.
