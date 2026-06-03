---
name: "Core Concept"
status: "draft"
tags: ["guide-dnl", "reference-dnl"]
paths:
  "@docs-index.md": "{@dnl-root}/docs/index.md"
  "@repo-README.md": "{@dnl-root}/README.md"
---

# Core Concept

DNL is an information architecture pattern for navigation, not a content dump. It helps readers move from a short landing page to a focused topic page without guessing where the next answer lives.

## The shape

- `README.md` gives the shortest useful overview.
- `docs/index.md` routes readers to the right topic.
- Topic pages answer one question well.
- Maintenance guidance stays in `DNL-system/`.

## Writing principles

- Prefer small pages with one job.
- Link forward instead of repeating the same background in every file.
- Keep public documentation generic and free of private examples unless the task explicitly calls for them.
- Split a page once it starts acting like a table of contents for multiple unrelated topics.
