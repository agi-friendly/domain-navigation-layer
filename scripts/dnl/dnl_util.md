---
name: "DNL Maintenance Utility"
status: "draft"
tags: ["guide-dnl"]
paths: {}
---

# DNL Maintenance Utility

`scripts/dnl/dnl_util.py` owns write-capable DNL maintenance and generated
tag/link index commands.

## Safety model

`tag add` and `mv` are dry-run operations for source documents unless
`--write` is present. Index `build` and `update` commands immediately refresh
ignored generated state and do not accept `--write`.

## Tag editing

```bash
python3 scripts/dnl/dnl_util.py tag add \
  --dir docs --tag guide-dnl --recursive
python3 scripts/dnl/dnl_util.py tag add \
  --dir docs --tag guide-dnl --recursive --write
```

## Tag and link indexes

```bash
python3 scripts/dnl/dnl_util.py tag index build
python3 scripts/dnl/dnl_util.py tag index check
python3 scripts/dnl/dnl_util.py tag index update --path docs/index.md
python3 scripts/dnl/dnl_util.py link index build
python3 scripts/dnl/dnl_util.py link index check
```

Indexes remain under
`.agents/skills/dnl-query/{tag-index,link-index}/` as ignored runtime state.

## Moving one DNL document

```bash
python3 scripts/dnl/dnl_util.py mv \
  --path docs/old.md --to docs/reference
python3 scripts/dnl/dnl_util.py mv \
  --path docs/old.md --to docs/reference --write
```

`mv` accepts one Markdown file and an existing destination directory. It does
not rename files or create directories. It rebuilds the link index before
planning, rewrites YAML `paths` backlinks when writing, and refreshes link and
tag indexes after the move.

The command refuses an automatic move when local Markdown or image links make
asset handling unsafe. Move those assets and update their references manually
before using `mv`.

## Applying a dry run

For `tag add` and `mv`, first run without `--write` and inspect every planned
source document and backlink update. Repeat the same command with `--write`
only when the plan is correct.

## Windows UTF-8

```powershell
python -X utf8 scripts/dnl/dnl_util.py tag index check
```
