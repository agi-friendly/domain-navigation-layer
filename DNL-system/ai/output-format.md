---
name: "Output Format Rules (Standardized Response)"
status: "draft"
tags: ["rule-dnl"]
paths: {}
---

# Output Format Rules (Standardized Response)

This document defines the default shape of agent responses in this repository.
The goal is to make the target layer, evidence, and next action obvious.

## Global rules

- State the target context early.
- Name the repository layer you are using.
- Separate facts, hypotheses, and action items.
- Keep the response short enough that a human can scan it quickly.

## Bug / defect analysis

Use this structure when the task is about a bug or unexpected behavior:

1. Target context
2. Issue summary
3. Root-cause hypotheses
4. Impact scope
5. Action items
6. Referenced docs

Example context:

- Repository: `domain-navigation-layer`
- Docs: `docs/index.md`
- System: `DNL-system/ai/guardrails.md`
- Project: `sample-project/README.md`

## Code understanding

Use this structure when the task is about reading existing code:

1. Module overview
2. Core flow
3. Dependencies and constraints
4. Referenced docs

## Feature or refactoring proposal

Use this structure when the task is about changing behavior:

1. Objective
2. Targeted scope
3. Proposed changes
4. Risk assessment
5. Referenced docs

## Documentation generation

Use this structure when the task is about writing docs:

1. Document metadata
2. Content outline
3. Key terminology
4. Draft content

## Mandatory footer

End with a short references section that names the layer and the document used.

Example:

- [Repository] `README.md`
- [Docs] `docs/index.md`
- [System] `DNL-system/ai/guardrails.md`
- [Project] `sample-project/README.md`

## Final principle

Clear context, clear source.
