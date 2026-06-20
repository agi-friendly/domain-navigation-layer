---
name: "forbidden-actions.md # 금지/주의 작업(임의 정책 변경, 확정 단정, 접근 가정 등)"
status: "draft"
tags: ["rule-dnl", "placeholder"]
paths: {}
---

# forbidden-actions.md # 금지/주의 작업(임의 정책 변경, 확정 단정, 접근 가정 등)

## Intent
Prevent common failure modes from drifting into unsafe automation or unreviewable changes.

## Strictly forbidden

- Do not modify paths, files, or behavior without a concrete file target.
- Do not claim a behavior is confirmed without checking local evidence.
- Do not change `DNL-system` rules to fit a single repository exception.
- Do not move or delete docs just to satisfy formatting consistency.
- Do not include private/company-specific terminology in public-facing starter docs unless explicitly requested.
- Do not assume runtime state, credentials, network access, or machine-specific paths.

## High-risk actions (confirm first)

- Making security-related policy changes.
- Rewriting multiple boundary/template files at once without a migration plan.
- Replacing a working template structure with a deeply customized one.
- Running destructive git operations (`git reset`, `git clean`) as part of routine documentation work.

## Language rule

- Keep assertions to verified facts.
- Use "I don’t know" / "need confirmation" when evidence is missing.
