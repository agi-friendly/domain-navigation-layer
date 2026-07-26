---
name: ".agents/skills/dnl-builder"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@tooling.md": "{@dnl-root}/scripts/dnl/README.md"
  "@qa.md": "{@dnl-root}/scripts/dnl/qa.md"
  "@dnl-util.md": "{@dnl-root}/scripts/dnl/dnl_util.md"
---

# .agents/skills/dnl-builder

This directory is a thin AI behavior and compatibility surface.

- Canonical authoring rules: `DNL-system/authoring/README.md`
- Canonical lifecycle rules: `DNL-system/workflow/README.md`
- Official tooling portal: `scripts/dnl/README.md`
- QA guide: `scripts/dnl/qa.md`
- Maintenance and move guide: `scripts/dnl/dnl_util.md`

## Compatibility

`.agents/skills/dnl-builder/qa.py` and
`.agents/skills/dnl-builder/dnl_util.py` are temporary compatibility shims.
They warn on stderr and delegate to the canonical scripts. New commands and
documentation must use `scripts/dnl`.

Generated QA reports remain under
`.agents/skills/dnl-builder/reports/qa-report.md` as ignored runtime state.
