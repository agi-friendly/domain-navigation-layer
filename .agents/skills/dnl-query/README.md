---
name: ".agents/skills/dnl-query"
status: "draft"
tags: ["portal-dnl", "dnl-query"]
paths:
  "@query.py": "{@dnl-root}/scripts/dnl/query.py"
  "@query.md": "{@dnl-root}/scripts/dnl/query.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
---

# .agents/skills/dnl-query

`dnl-query` is a read-only lookup behavior for agents.

- Run the official executable at `@query.py`.
- Read the full command and output guide at `@query.md`.
- Use `@dnl-builder.md` to build or refresh indexes, edit DNL, or run QA.

The retained `dnl_query.py` file in this directory is a compatibility shim only.
