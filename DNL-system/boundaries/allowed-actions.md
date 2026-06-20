---
name: "allowed-actions.md # 가능한 작업 범위(조사/설계/문서화/코드탐색 등)"
status: "draft"
tags: ["rule-dnl", "placeholder"]
paths: {}
---

# allowed-actions.md # 가능한 작업 범위(조사/설계/문서화/코드탐색 등)

## Intent
Define clear default actions so the agent can start with confidence and skip unnecessary confirmation loops.

## Allowed actions by default

- Confirm task scope and choose the right path of `DNL-system` before touching project data.
- Read repository files and use local context files (`PATHS.md`, `CURRENT_USER.md`, etc.) when they exist.
- Summarize known facts, assumptions, constraints, and uncertainties before proposing changes.
- Propose edits with file-level granularity and keep changes minimal and reviewable.
- Draft or revise DNL and documentation in the style requested by this repository.
- Run provided validation/check commands and report exact command results.
- Ask a concise clarification question only when required evidence is missing and work would otherwise be high risk.

## What is explicitly in scope

- Authoring or editing DNL files under `DNL-system/` and aligned docs.
- Producing design reviews, improvement plans, and PR descriptions from repository context.
- Suggesting safe next actions and fallback options when tradeoffs exist.

## Collaboration expectations

- Keep each suggestion actionable and maintainable for human reviewers.
- Avoid guessing missing repository structure; use concrete file paths and commands.
- Default to explicitness over style experiments: readable markdown, stable section order, consistent labels.
