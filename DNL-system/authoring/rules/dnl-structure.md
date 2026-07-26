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
  README.md
  dnl_config.py
  dnl_util.py
  dnl_util.md
  dnl_util_core/
  qa.py
  qa.md
  query.py
  query.md
  tree.py
  tree.md
  yaml_header.py
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
- `.agents/skills/` holds thin agent behavior guides and compatibility shims.
- `tests/dnl/` holds portable DNL tooling tests.
- `.repo-history/` stores historical context separately from the main docs.
- Optional domain layers such as `example-company` and `sample-product` belong to the repository-specific knowledge tree, not the public landing page.

The portable tooling boundary is:

- `scripts/dnl/tree.py` with `scripts/dnl/tree.md`
- `scripts/dnl/query.py` with `scripts/dnl/query.md`
- `scripts/dnl/qa.py` with `scripts/dnl/qa.md`
- `scripts/dnl/dnl_util.py` with `scripts/dnl/dnl_util.md`
- shared maintenance internals in `scripts/dnl/dnl_config.py`,
  `scripts/dnl/yaml_header.py`, and `scripts/dnl/dnl_util_core/`
- portable verification in `tests/dnl/`

## Authoring rule

Documentation work should start from the repository landing page and docs index.
If the task is about maintaining DNL itself, read `DNL-system/README.md` first.
Only move into optional domain layers after the target layer is known.

The official tree, query, QA, and maintenance commands use `scripts/dnl`.
Legacy executable paths under `.agents/skills` are compatibility shim surfaces only.
Generated indexes and QA reports may remain under ignored `.agents/skills`
runtime paths; generated-state location is independent of source ownership.
