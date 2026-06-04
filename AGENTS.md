---
name: "Before answering:"
paths:
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@ai-context-loading.md": "{@dnl-root}/DNL-system/ai/context-loading.md"
  "@ai-doc-selection-rules.md": "{@dnl-root}/DNL-system/ai/doc-selection-rules.md"
  "@ai-local-context.md": "{@dnl-root}/DNL-system/ai/local-context/README.md"
  "@paths-md.md": "{@dnl-root}/DNL-system/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@dnl-root}/DNL-system/ai/local-context/current-user-md.md"
---

# Before answering:
- Treat this file as the AI entrypoint for the repository.
- Read and follow `@dnl-system.md` as the system portal.
- Use `@ai-context-loading.md` and `@ai-doc-selection-rules.md` to decide which documents to load next.
- `@ai-local-context.md` when you need repository-local path mapping or current-user handoff.
- `@paths-md.md` and `@current-user-md.md` if the task depends on local context details.

---

# Before answering:
- Treat this repository as a generic public Domain Navigation Layer project.
- Write public-facing documentation in English unless the user explicitly asks for another language.
- Do not assume any private company or product vocabulary is still valid here.
- Treat `README.md` and `docs/` as reader-facing public documentation. Load them when the task is about public explanation, onboarding, or README/docs content.
- Use `DNL-system/` for AI routing, maintenance rules, workflow guidance, templates, or repository-local context.
- When a task depends on repository structure, inspect the current tree or the relevant docs instead of assuming hidden files or legacy path maps.
- Keep changes small, readable, and aligned with the dominant style of the file you are editing.
- If you find stale or private-specific examples, report them before widening the scope.
