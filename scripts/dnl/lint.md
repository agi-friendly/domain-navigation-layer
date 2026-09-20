# Optional DNL Lint

`lint.py` is a read-only tool for manually finding documents worth reviewing
for a possible split. It is optional, is not an AI authoring requirement, and
does not replace or run repository QA. It changes no files and generates no
report unless you redirect stdout yourself.

## Usage

```bash
# Scan the configured DNL scope.
python3 scripts/dnl/lint.py

# Inspect one file or directory; multiple targets are supported.
python3 scripts/dnl/lint.py DNL-example/README.md
python3 scripts/dnl/lint.py DNL-system/authoring

# Change the inclusive warning threshold.
python3 scripts/dnl/lint.py --paths-threshold 25
```

Python 3.11+ is required; no additional dependencies are needed. On Windows,
use `python -X utf8` instead of `python3`.

## Scope and Results

- `--root` defaults to this script's repository, independently of the current
  working directory. Relative targets are resolved against that root.
- Without targets, the tool uses `scan.include` from `dnl-config.toml`.
- Configured `scan.exclude`, hidden directories, `SKILL.md`, and symlinks are
  excluded. Explicit targets replace the include scope, but retain exclusions.
  Overlapping targets are deduplicated; targets outside the root are rejected.
- The shared DNL frontmatter parser counts unique entries in the top-level
  `paths` map. A directory alias counts once, regardless of how many child files
  the body references. Body examples are not counted. Missing frontmatter or missing
  `paths` contributes zero entries; this tool is not a YAML completeness check.
- `paths >= 15` emits `WARNING` by default. Results are sorted by count
  descending, then path. This count is a review signal, not a token estimate
  or proof that a document should be split.
- Warnings exit with code **0**. Invalid arguments, missing targets, read errors,
  or frontmatter parsing errors exit with code **2**. Parsing errors are reported
  rather than treating a partial count as a clean result.

Use the findings to discuss document boundaries before restructuring. This tool
does not automatically split documents or modify routing.
