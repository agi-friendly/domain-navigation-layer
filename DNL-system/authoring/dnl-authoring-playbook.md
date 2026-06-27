---
name: "DNL Authoring Playbook (for AI-assisted writing)"
status: "draft"
tags: ["playbook-dnl", "dnl-builder"]
paths:
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@working-authoring-rule.md": "{@DNL-system}/workflow/working-authoring-rule.md"
  "@working-to-dnl.md": "{@DNL-system}/workflow/working-to-dnl.md"
  "@working-to-archive.md": "{@DNL-system}/workflow/working-to-archive.md"
  "@dnl-builder-qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-builder/README.md": "{@DNL-system}/authoring/README.md"
---

# DNL Authoring Playbook (for AI-assisted writing)

This playbook guides AI-assisted DNL document changes.
It is exposed through the authoring portal and should be loaded only when DNL writing or maintenance is part of the task.

## 0. Before writing

Read:

1. `@markdown-rule.md`
2. `@yaml-frontmatter-rule.md`
3. `@multi-dnl-authority.md`
4. If the work includes `working`, promotion, archive, or history cleanup: read `@workflow-root.md`, then choose the specific rule:
   - `@working-authoring-rule.md` for creating, registering, or editing working bundles
   - `@working-to-dnl.md` for promotion or absorption into canonical DNL
   - `@working-to-archive.md` for archive movement decisions

## 0.5. DNL steward lens

An agent writing DNL is not only editing text.
It is maintaining a navigation layer that should help the next agent reach current truth with less context.

Core principles:

- DNL preserves context without putting all context into one document.
- README and portal documents should hold current truth, document roles, and next routes.
- Long investigations, old plans, comparisons, and decision background should move into load-on-demand documents when they are substantial.
- `working/` is source material. It is not canonical DNL.
- After promotion, active DNL should not treat `working/` as the priority source of truth.
- UI/interface documents should describe what that surface can prove.
- Implementation/domain documents should own processing rules, storage behavior, and source evidence.
- Avoid duplicating the same assertion across several files.

Promotion or maintenance is complete only when:

1. leaf documents reflect current evidence
2. parent README files route to the new canonical document
3. maps and guides agree with the promoted structure
4. `working/` is clearly either still active, ready for archive, or no longer a default route
5. document responsibilities are separated
6. YAML `paths` use logical `{@variable}/...` paths
7. QA and semantic stale checks both pass

## Semantic stale search

QA catches syntax and link problems.
Semantic stale search catches text that still points the reader in an old direction.

Search for:

- old paths that still look current
- priority wording such as "start from working" after promotion
- completion claims that have no parent route
- interface docs that claim implementation behavior they did not verify
- YAML `paths` values such as `README.md`, `../`, or `./` when a logical path should be used
- raw working bundles presented as canonical DNL

## 1. Writing principles

- The primary DNL reader is an AI agent.
- Canonical DNL documents must include YAML frontmatter with `name`, `status`, and `tags`.
- Use YAML `paths` and `@tokens` for canonical DNL navigation.
- Do not use local Markdown file/folder links in canonical DNL documents.
- New or meaningfully edited DNL documents should use `status: "draft"` unless the user explicitly says otherwise.
- README documents should include `portal-dnl`.
- Allowed exceptions for Markdown links are images, external web URLs, and fenced-code examples.
- `working/` is not canonical DNL and may use normal Markdown links for human-facing bundle navigation.

## 2. Layer scope

Use only the layers a repository actually has.

- System: DNL operating rules, AI rules, workflow, templates, boundaries
- Shared/team/company: common glossary, maps, gateways, status
- Product/domain: routing for a product family or broad domain area
- Project: implementation, module, screen, API, runbook, and source routes

If a lower layer must override a higher layer, it must explicitly declare the override.

## 3. Recommended workflow

1. Narrow the target layer.
2. If the task touches working lifecycle, choose the matching workflow rule first.
3. Decide the document role: router, canonical guide, background, working source material, or archive.
4. Search for stale paths or wording before editing.
5. Edit the target document.
6. Rewire parent README, maps, guides, and cross-links.
7. Read surrounding paragraphs to make sure the flow still makes sense.
8. Search semantic stale text again.
9. Run QA.
10. Keep one coherent task per commit.

## 4. Prompt template

```text
You are editing a public DNL repository.

Before writing, read:
- DNL-system/workflow/README.md
- DNL-system/workflow/working-authoring-rule.md (required when creating/editing working bundles)
- DNL-system/workflow/working-to-dnl.md (required when promoting/absorbing working material)
- DNL-system/authoring/dnl-authoring-playbook.md
- DNL-system/authoring/rules/markdown-rule.md
- DNL-system/authoring/rules/yaml-frontmatter-rule.md
- DNL-system/authoring/rules/multi-dnl-authority.md

Rules:
- No local Markdown file/folder links in canonical DNL docs.
- Every canonical DNL Markdown document must include YAML frontmatter `name`, `status`, and `tags`.
- New or meaningfully edited DNL docs should use status: "draft" unless the user explicitly says otherwise.
- README docs must include tag: `portal-dnl`.
- Use YAML frontmatter paths + @tokens for canonical navigation.
- Working bundles are source material, not canonical DNL.
- Keep working bundle rules lightweight: `working/{working-name}/README.md` is the minimum.
- Keep routers/README files light: current truth + next navigation only.
- Split heavy background, investigation notes, and decision history into load-on-demand docs.
- After promoting working material, rewire parent README/map/guide docs so active DNL no longer treats working as the priority path.
- Search semantic stale after edits: old paths, old priority wording, missing parent routing, and completion claims without navigation.
- After changes, run: python3 .agents/skills/dnl-builder/qa.py --profile portal

Task:
<write your task here>
```
