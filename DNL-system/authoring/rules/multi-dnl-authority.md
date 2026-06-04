---
name: "multi-dnl-authority"
status: "draft"
tags: ["rule-dnl", "dnl-builder"]
paths: {}
---

## DNL Authority & Override Rules

Some repositories use a strict hierarchical authority model for DNL documents.
All AI agents and humans must interpret documents according to the rules below, for the layers that actually exist in the repository.

### Authority Order (from highest to lowest, when present)
1. Shared layer DNL (`{@dnl-root}/docs/sample-dnl/README.md`)
2. Product-level DNL (`{@dnl-root}/docs/sample-dnl/sample-product/README.md`)
3. Project-level DNL (`{@dnl-root}/docs/sample-dnl/sample-product/sample-project/README.md`)

### Interpretation Rules
- Higher-level DNL documents define global concepts, policies, and constraints.
- Lower-level DNL documents MUST NOT contradict higher-level rules by default.
- If a lower-level DNL needs to diverge, it MUST explicitly declare an override.

If a repository only has some of these layers, the same rule still applies: the higher layer that exists wins over the lower layer that exists.

### Override Declaration Rule
- Any override must be explicitly stated using clear wording such as:
  - "Override:"
  - "Exception:"
  - "This rule intentionally overrides <higher-level scope>"

- Implicit or assumed overrides are NOT allowed.
- If no explicit override is declared, higher-level DNL rules always take precedence.

### Conflict Resolution
- In case of ambiguity or conflict:
  - Prefer the higher-level DNL.
  - If still unclear, treat the rule as undefined and request clarification.

These rules exist to prevent silent contradictions and to ensure consistent reasoning
across company, version, and project scopes.
