---
name: "Repository Layout"
status: "draft"
tags: ["reference-dnl"]
paths:
  "@docs-index.md": "{@dnl-root}/docs/index.md"
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@repo-README.md": "{@dnl-root}/README.md"
---

# Repository Layout

```text
.
├── README.md
├── AGENTS.md
├── docs/
│   ├── index.md
│   ├── core-concept.md
│   ├── getting-started.md
│   └── repository-layout.md
├── DNL-system/
│   └── README.md
├── .agents/
│   └── skills/
├── .github/
├── .claude/
├── .repo-history/
├── LICENSE
└── dnl-config.toml
```

## What the main files do

- `README.md` is the public landing page.
- `AGENTS.md` is the working contract for automated collaborators.
- `docs/` holds the public explanation of the project.
- `DNL-system/` holds maintenance and authoring guidance.
- `.repo-history/` is historical material and should stay out of the main documentation flow.
- `dnl-config.toml` defines the navigation and indexing surface.

The repo is intentionally small at the top level so readers do not have to guess where to start.
