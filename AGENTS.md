---
name: "Before answering:"
paths:
  "@repo-README.md": "{@dnl-root}/README.md"
  "@docs-index.md": "{@dnl-root}/docs/index.md"
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@ai-local-context.md": "{@dnl-root}/DNL-system/ai/local-context/README.md"
  "@paths-md.md": "{@dnl-root}/DNL-system/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@dnl-root}/DNL-system/ai/local-context/current-user-md.md"
---

# Before answering:
- Read and follow the documents below as authoritative context.
- `@repo-README.md`
- `@docs-index.md`
- `@dnl-system.md`
- `@ai-local-context.md` when you need repository-local path mapping or current-user handoff.
- `@paths-md.md` and `@current-user-md.md` if the task depends on local context details.

---

# Before answering:
- Treat this repository as a generic public Domain Navigation Layer project.
- Write public-facing documentation in English unless the user explicitly asks for another language.
- Do not assume any private company or product vocabulary is still valid here.
- Prefer the public docs first; use `DNL-system/` when you need maintenance rules, workflow guidance, templates, or repository-local context.
- When a task depends on repository structure, inspect the current tree or the relevant docs instead of assuming hidden files or legacy path maps.
- Keep changes small, readable, and aligned with the dominant style of the file you are editing.
- If you find stale or private-specific examples, report them before widening the scope.
