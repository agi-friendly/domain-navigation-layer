---
name: dnl-query
description: Read-only query skill for finding DNL documents fast by tag/name/status/path without editing them.
---

# DNL Query

Use `.agents/skills/dnl-query` when you only need to find DNL documents, not edit them.

## When to use

- Finding DNL documents by tag
- Narrowing documents by `name`, `status`, or path prefix
- Reading a generated index instead of scanning many Markdown files directly
- Quickly checking a document's outbound links, backlinks, and unresolved path candidates

## Basic usage

```bash
# Tag list and counts
python3 .agents/skills/dnl-query/dnl_query.py tags

# Documents with a specific tag
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl

# Print paths only
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format paths

# JSONL for AI follow-up processing
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format jsonl

# Outbound links declared by a document
python3 .agents/skills/dnl-query/dnl_query.py links --path docs/index.md

# Source documents that reference a given document
python3 .agents/skills/dnl-query/dnl_query.py backlinks --path DNL-system/README.md

# Unresolved internal target candidates
python3 .agents/skills/dnl-query/dnl_query.py unresolved

# Unresolved candidates summarized by source directory
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# Path tokens declared but never used in the body
python3 .agents/skills/dnl-query/dnl_query.py unused

# File/path-like token candidates in the body but missing from YAML paths
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens
```

## Link health query order

For a document-link health check, narrow the scope with a summary first, then look at detailed records.

```bash
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary
python3 .agents/skills/dnl-query/dnl_query.py unresolved --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --under docs --format jsonl
```

## Recommended tags

Start by narrowing candidates with the tags below.

- Structure/navigation: `portal-dnl`, `map-dnl`, `glossary-dnl`, `rule-dnl`
- Work type: `guide-dnl`, `playbook-dnl`, `runbook-dnl`, `reference-dnl`, `troubleshooting-dnl`
- Topic/tech: `auth`, `api`, `sql`, `i18n`, `svelte`, `migration`

For the full set of tags and counts in the current index, run `python3 .agents/skills/dnl-query/dnl_query.py tags`.

## Role boundaries

- Find: `.agents/skills/dnl-query/dnl_query.py`
- View structure: `.agents/skills/tree/tree.py`
- Author/maintain/validate: `.agents/skills/dnl-builder`

`dnl-query` only reads the index.
For building a tag index, checking its freshness, or refreshing a single file, use `.agents/skills/dnl-builder/dnl_util.py tag index ...`.
For building a link index or checking its freshness, use `.agents/skills/dnl-builder/dnl_util.py link index ...`.

## When the index is missing

The tag/link indexes are local artifacts that are not committed to git.
If an index is missing or its freshness is in doubt, build it with the commands below.

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py link index build
```
