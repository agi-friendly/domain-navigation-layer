---
name: "Before answering:"
paths:
  "@dnl-system.md": "{@dnl-root}/DNL-system/README.md"
  "@ai-context-loading.md": "{@dnl-root}/DNL-system/ai/context-loading.md"
  "@ai-doc-selection-rules.md": "{@dnl-root}/DNL-system/ai/doc-selection-rules.md"
  "@ai-local-context.md": "{@dnl-root}/DNL-system/ai/local-context/README.md"
  "@paths-md.md": "{@dnl-root}/DNL-system/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@dnl-root}/DNL-system/ai/local-context/current-user-md.md"
  "@dnl-example.md": "{@dnl-root}/DNL-example/README.md"
  "@skills-readme.md": "{@dnl-root}/.agents/skills/README.md"
  "@multi-agent-skill-guide.md": "{@dnl-root}/.agents/skills/multi-agent-skill-guide.md"
  "@dnl-tooling.md": "{@dnl-root}/scripts/dnl/README.md"
  "@dnl-query-tool.md": "{@dnl-root}/scripts/dnl/query.md"
  "@dnl-tree-tool.md": "{@dnl-root}/scripts/dnl/tree.md"
  "@dnl-qa-tool.md": "{@dnl-root}/scripts/dnl/qa.md"
  "@dnl-util-tool.md": "{@dnl-root}/scripts/dnl/dnl_util.md"
---

# Before answering:
- Treat this file as the AI entrypoint for the repository.
- Read and follow `@dnl-system.md` as the system portal.
- Use `@ai-context-loading.md` and `@ai-doc-selection-rules.md` to decide which documents to load next.
- `@ai-local-context.md` when you need repository-local path mapping or current-user handoff.
- `@paths-md.md` and `@current-user-md.md` if the task depends on local context details.
- If the task mentions a skill, use `.agents/skills/{skill}/SKILL.md` as the source of truth.
- Read `@skills-readme.md` and `@multi-agent-skill-guide.md` only when you need the shared skill catalog or wrapper-maintenance rules.
- Use `@dnl-tooling.md` as the portal for the official tree, query, QA, and maintenance executables under `scripts/dnl`.
- Treat retained executables under `.agents/skills/tree`, `.agents/skills/dnl-query`, and `.agents/skills/dnl-builder` as compatibility shims only.
- Generated tag/link indexes and QA reports remain ignored runtime artifacts under `.agents/skills`; runtime state does not define source ownership.
- If indexes are missing or stale, rebuild them with `scripts/dnl/dnl_util.py`; do not commit generated index files.

---

# Before answering:
- Treat this repository as a generic public Domain Navigation Layer project.
- Write public-facing documentation in English unless the user explicitly asks for another language.
- Do not assume any private company or product vocabulary is still valid here.
- Treat `README.md` and `docs/` as reader-facing public documentation. Load them when the task is about public explanation, onboarding, or README/docs content.
- Use `@dnl-example.md` only when the task is about examples, onboarding, or the starter route. Do not treat it as private project knowledge.
- Use `DNL-system/` for AI routing, maintenance rules, workflow guidance, templates, or repository-local context.
- When a task depends on repository structure, inspect the current tree or the relevant docs instead of assuming hidden files or legacy path maps.
- Keep changes small, readable, and aligned with the dominant style of the file you are editing.
- If you find stale or private-specific examples, report them before widening the scope.
