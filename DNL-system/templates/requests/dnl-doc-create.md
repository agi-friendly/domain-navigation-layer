---
name: "DNL Document Creation Request Template"
status: "draft"
tags: ["template-dnl", "dnl-builder"]
paths:
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@qa.py": "{@dnl-root}/scripts/dnl/qa.py"
---

# DNL Document Creation Request Template

> Copy this template when you want to ask an AI to create a new DNL document or substantially revise an existing one.

---

## 1) Target (required)
- Product: e.g. `sample-product`
- Project DNL: e.g. `{@sample-project}` or `{@dnl-root}/docs/sample-dnl`
- Module/Domain: e.g. `sample-module`

---

## 2) Purpose (required)
- What question or task should this document help solve?
  - Example: "mail compose screen bug investigation", "mailbox concept summary"

---

## 3) Output type
- [ ] Portal (README)
- [ ] Guide
- [ ] Troubleshooting (Runbook)
- [ ] File map (file-structure)

---

## 4) Writing rules (required)
- YAML frontmatter must include `name`, `status`, and `tags`
- New documents must use `status: draft`
- `README.md` documents must include the `portal-dnl` tag
- Choose 1-3 tags that match the document type; use `tags: []` if nothing fits
- Do not use normal markdown links to local files or folders
- Declare only the paths you actually need in the YAML `paths` block
- Use `@tokens` or `{@variable}` references for navigation
- Do not add `HUMAN_LINK`, `HUMAN_LINKS`, or clickable local-link exceptions
- Follow `@markdown-rule.md`, `@yaml-frontmatter-rule.md`, and `@dnl-authoring-playbook.md`

---

## 5) Information to include
- [ ] A clear "where to go next" hint for the request type
- [ ] Key terms or glossary entries
- [ ] Real paths/files when possible, preferably via YAML paths or `@tokens`
- [ ] Update date or status, if useful

---

## 6) Verification
- After writing, run: `python3 scripts/dnl/qa.py --profile portal --fail-on all`
- Fix any violations before handing it off
