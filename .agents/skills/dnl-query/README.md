---
name: ".agents/skills/dnl-query"
status: "draft"
tags: ["portal-dnl", "dnl-query"]
paths:
  "@dnl-query.py": "{@dnl-root}/.agents/skills/dnl-query/dnl_query.py"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
  "@tag-index": "{@dnl-root}/.agents/skills/dnl-query/tag-index"
  "@link-index": "{@dnl-root}/.agents/skills/dnl-query/link-index"
---

# .agents/skills/dnl-query

`dnl-query` is a read-only skill for browsing DNL documents without editing them.
It reads the generated tag index to quickly find the DNL documents you need by tag, status, name, and path.

## Role

- Check the tag list and counts
- Query DNL documents with a specific tag
- Narrow document candidates by `status`, `name`, and path prefix
- Query outbound/inbound links from the link index
- Inspect unresolved internal path candidates
- Provide `paths`, `jsonl`, and `json` output that is easy for an AI to use in follow-up work

## Responsibility boundaries

- Find: `@dnl-query.py`
- View structure: `@tree.md`
- Author/maintain/validate/refresh index: `@dnl-builder.md`

`dnl-query` only reads the index.
Building a tag index, checking its freshness, or refreshing a single file is handled by `dnl-builder`'s `tag index` command.
Building a link index and checking its freshness is handled by `dnl-builder`'s `link index` command.

## Basic commands

```bash
# Tag list and counts
python3 .agents/skills/dnl-query/dnl_query.py tags

# Documents with a specific tag
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl

# Print paths only
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format paths

# JSONL for AI follow-up processing
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format jsonl

# Query outbound links declared by a document
python3 .agents/skills/dnl-query/dnl_query.py links --path docs/index.md

# Query source documents that reference a given document
python3 .agents/skills/dnl-query/dnl_query.py backlinks --path DNL-system/README.md

# Query unresolved internal target candidates
python3 .agents/skills/dnl-query/dnl_query.py unresolved

# Summarize unresolved candidates by source directory
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# Path tokens declared but never used in the body
python3 .agents/skills/dnl-query/dnl_query.py unused

# File/path-like token candidates in the body but missing from YAML paths
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens
```

## Filters

```bash
# Documents that have all of several tags
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --tag reference-dnl

# Status filter
python3 .agents/skills/dnl-query/dnl_query.py docs --tag rule-dnl --status draft

# Subpath filter
python3 .agents/skills/dnl-query/dnl_query.py docs --tag rule-dnl --under docs

# Partial name search
python3 .agents/skills/dnl-query/dnl_query.py docs --name "OIDC"

# Narrow the unresolved source scope
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary --under docs --depth 3
```

Filters combine as AND conditions.

## Recommended tags

When the AI is unsure which tag to start with, query by the criteria below first.
The full set of tags and counts in the current index is authoritatively given by `python3 .agents/skills/dnl-query/dnl_query.py tags`.

### Structure/navigation

| Tag | Look here first for |
| --- | --- |
| `portal-dnl` | README / entry points / child document routing |
| `map-dnl` | Maps linking modules, screens, packages, and source |
| `glossary-dnl` | Terms, abbreviations, screen names, common naming |
| `rule-dnl` | Authoring rules, decision rules, development rules |
| `template-dnl` | Request/output templates |

### Work type

| Tag | Look here first for |
| --- | --- |
| `guide-dnl` | How-to, authoring guides, integration guides |
| `playbook-dnl` | Procedures for repeated work |
| `runbook-dnl` | Operations / incident-response procedures |
| `reference-dnl` | Reference docs for quick lookups |
| `troubleshooting-dnl` | Problem solving, common mistakes, symptom-based responses |

### Topic/tech

| Tag | Look here first for |
| --- | --- |
| `auth` | Authentication, authorization, OIDC, JWT, sessions |
| `api` | API contracts, client/server integration |
| `sql` | DB, DDL, mappers, queries |
| `i18n` | Localization, message keys, paraglide |
| `svelte` | Svelte/SvelteKit rules and troubleshooting |
| `migration` | Version transitions, legacy-to-new, porting |
| `important` | Key documents the user or AI should check first |

### Module examples

Module tags can be reused freely.
Use them to quickly narrow down to documents for a specific business module.

```bash
python3 .agents/skills/dnl-query/dnl_query.py docs --tag guide-dnl --format paths
python3 .agents/skills/dnl-query/dnl_query.py docs --tag reference-dnl --format paths
python3 .agents/skills/dnl-query/dnl_query.py docs --tag portal-dnl --format paths
```

## Output formats

- `text`: `path | status | name`
- `paths`: one path per line
- `jsonl`: one JSON object per line
- `json`: a JSON array

## Link health query

For link health, find the most problematic areas with a summary first, then narrow down to detailed records.

```bash
# Unresolved counts per source directory
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# View a specific scope only
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary --under docs --depth 3

# Inspect detailed candidates
python3 .agents/skills/dnl-query/dnl_query.py unresolved --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --under docs --format jsonl
```

`unresolved` lists candidates whose target path does not resolve, `unused` lists token candidates declared in YAML `paths` but never used in the body,
and `missing-tokens` lists file/path-like token candidates in the body but missing from YAML `paths`.

## Index

The default index location is `@tag-index`.
The link query commands read `@link-index`.
Index files are local artifacts that are not committed to git.
If an index is missing or its freshness is in doubt, use the commands below.

```bash
# Rebuild the entire tag index
python3 .agents/skills/dnl-builder/dnl_util.py tag index build

# Check the tag index freshness
python3 .agents/skills/dnl-builder/dnl_util.py tag index check

# Rebuild the entire link index
python3 .agents/skills/dnl-builder/dnl_util.py link index build

# Check the link index freshness
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```
