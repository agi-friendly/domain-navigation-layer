# .repo-history Guide

This directory is the repository's internal history space.

Its purpose is to keep:

1. Repository structure and workflow changes separate from active DNL docs
2. Collaboration lessons and decision history
3. Project-specific history outside the active navigation layer

This directory is not a Company / Product / Project DNL.
It is not part of the default routing surface, and active docs should not link to it.

## Basic rules

1. Keep one history file per event.
2. Split events by incident or decision, not by commit size alone.
3. Capture facts, decisions, and useful context together.
4. Mark uncertain dates as estimates.
5. Do not route to this content from active DNL pages; use the catalog only.
6. Keep it out of the default reading path for agents.
7. Move anything that looks like an active rule into the appropriate DNL layer and mark the history entry as historical context only.

## Writing density and length

`.repo-history` is not a context-saving space that should be read on every task.
Its primary readers are humans and agents reconstructing a past decision later.

Therefore, do not shorten away useful background just to make entries look small.
Keep enough detail to reconstruct the reason behind the change, the alternatives considered, and the outcome.

When adding or expanding entries, follow these points:

1. Don't omit important background, decision process, failed alternatives, or emotional context just to stay brief.
2. Do not repeat only what changed; include why it changed.
3. Preserve names, tokens, paths, commits, and dates that matter for later search.
4. Mark uncertainty explicitly with `estimated`, `unverified`, or `memory-based`.
5. Never record secrets, credentials, personal sensitive data, or other information that should not be public.

## Recommended structure

```text
.repo-history/
  GUIDE.md
  templates/
    history-entry-template.md
  sample-repo/
    catalog.md
    2025/
      05/
      07/
      12/
    2026/
      01/
      04/
  sample-project/
    catalog.md
    2026/
      04/
        YYYY-MM-DD-topic.md
        topic-archive/
```

## File naming

- Exact date known: `YYYY-MM-DD-kebab-case.md`
- Month known: `YYYY-MM-kebab-case.md`
- Approximate date: use the closest month and mark it as estimated in the body.

## Must include

1. One-line summary
2. Why the change was needed
3. How it was operated at the time
4. What it means now
5. Relevant paths/commits/external repos if needed
6. Ambiguous names/structures and how to read them
7. Alternatives that were rejected and mistakes not to repeat

## Style rules

- Write for humans and future agents.
- Keep the record concrete, not essay-like.
- Favor reason over just listing what happened.
- Do not compress `.repo-history` entries into active-DNL style summaries.

## Search / navigation rules

- Exclude `.repo-history/` from default indexing when appropriate.
- Do not create default links to this area from active DNL docs.
- Treat the catalog as the entry point.

## History types

- Repository change history: `.repo-history/sample-repo/`
- Project-specific history excluded from the active DNL: `.repo-history/{sample-project}/`
- Larger domain or product history: keep it in a separate history space that is clearly marked as historical, not active navigation.

The important distinction is between repository-internal history and active DNL content.
