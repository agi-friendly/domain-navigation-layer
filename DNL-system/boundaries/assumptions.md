---
name: "assumptions.md # (선택) 기본 가정(접근권한/환경/로그 위치 등) + 모르면 질문 규칙"
status: "draft"
tags: ["rule-dnl", "placeholder"]
paths: {}
---

# assumptions.md # (선택) 기본 가정(접근권한/환경/로그 위치 등) + 모르면 질문 규칙

## Intent
Make assumptions explicit so one person and one AI can continue work without hidden context debt.

## Default assumptions

- The repository paths referenced in this project are valid unless explicitly missing during a check.
- Public-facing documentation work should not require external credentials or private environment access.
- Local context files may exist and can be authoritative for path mappings and current-user handoff.
- Validation commands are expected to run from the repository root unless a skill/doc says otherwise.
- Existing markdown frontmatter and index format are preserved unless the request asks for structure migration.

## Missing evidence rule

When a required fact is missing:

- Stop and state what is missing in one line.
- Propose a low-risk alternative or explicitly ask for the missing value.
- Do not invent file content, environment paths, or command outputs.

## Scope of assumptions

- These assumptions apply to routine documentation, template, and boundary updates.
- For code migrations, security-sensitive changes, or operations tasks, capture fresh assumptions from task-specific docs before execution.
