---
name: "DNL Query Tool"
status: "draft"
tags: ["guide-dnl"]
paths: {}
---

# DNL Query Tool

`scripts/dnl/query.py` is a read-only lookup tool for DNL documents and link records.
It reads generated local indexes so people and agents can narrow the documents to open instead of scanning large Markdown areas.

## Quick Start

```bash
# List tags and counts.
python3 scripts/dnl/query.py tags

# Find documents by tag and print paths only.
python3 scripts/dnl/query.py docs --tag glossary-dnl --format paths

# Find rule documents under one subtree.
python3 scripts/dnl/query.py docs --tag rule-dnl --under DNL-system --format paths

# Inspect outbound links and backlinks for one document.
python3 scripts/dnl/query.py deps --path DNL-system/README.md --format json

# Summarize unresolved internal path candidates.
python3 scripts/dnl/query.py unresolved-summary
```

## DNL Usage Pattern

1. Start from `AGENTS.md` and the repository's DNL routers.
2. Use `scripts/dnl/query.py` to narrow candidates by tag, name, status, path, or link record.
3. Use `scripts/dnl/tree.py` only after the candidate subtree is known.
4. Open the selected documents and verify source code when behavior details matter.

`query.py` does not edit DNL content and does not build indexes.

## Commands

### Tags and Documents

```bash
python3 scripts/dnl/query.py tags
python3 scripts/dnl/query.py tags --format json
python3 scripts/dnl/query.py docs --tag glossary-dnl
python3 scripts/dnl/query.py docs --tag glossary-dnl --format paths
python3 scripts/dnl/query.py docs --tag glossary-dnl --format jsonl
python3 scripts/dnl/query.py docs --tag glossary-dnl --tag reference-dnl
python3 scripts/dnl/query.py docs --tag rule-dnl --status draft
python3 scripts/dnl/query.py docs --tag rule-dnl --under DNL-system
python3 scripts/dnl/query.py docs --name "routing"
```

Multiple `--tag` filters use AND semantics.

### Links

```bash
# Outbound links declared by one document.
python3 scripts/dnl/query.py links --path docs/index.md

# Documents that reference one target.
python3 scripts/dnl/query.py backlinks --path DNL-system/README.md

# Outbound links and backlinks together.
python3 scripts/dnl/query.py deps --path DNL-system/README.md --format json
```

### Link Health Records

```bash
python3 scripts/dnl/query.py unresolved
python3 scripts/dnl/query.py unresolved-summary
python3 scripts/dnl/query.py unresolved-summary --under docs --depth 3
python3 scripts/dnl/query.py unused
python3 scripts/dnl/query.py missing-tokens
```

## Output Formats

- `text`: human-scannable rows
- `paths`: one path per line
- `jsonl`: one JSON object per line
- `json`: a JSON array or object, depending on the command

`deps --format json` returns a script-friendly dependency plan with outbound, backlink, and unresolved-outbound counts.

## Indexes

The default local tag and link index locations remain:

```text
.agents/skills/dnl-query/tag-index
.agents/skills/dnl-query/link-index
```

Indexes are generated artifacts and should not be committed.
Build or check them with the builder maintenance commands:

```bash
python3 scripts/dnl/dnl_util.py tag index build
python3 scripts/dnl/dnl_util.py tag index check
python3 scripts/dnl/dnl_util.py link index build
python3 scripts/dnl/dnl_util.py link index check
```

## Compatibility

The retained skill-side entrypoint remains a compatibility shim for older automation and agent memory.
New documentation should use `scripts/dnl/query.py`.
