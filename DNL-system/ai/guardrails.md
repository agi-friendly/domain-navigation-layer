---
name: "AI Guardrails (Global Safety Rules)"
status: "draft"
tags: ["rule-dnl"]
paths: {}
---

# AI Guardrails (Global Safety Rules)

These are the top-level safety rules for agents working in this repository.
When they conflict with a lower-level document, these rules win unless a higher-priority repository rule says otherwise.

## Absolute forbidden actions

### 1. Cross-layer contamination

- Do not apply a rule, example, or implementation detail from one layer to an unrelated layer.
- Do not mix two product lines, two project trees, or two unrelated task contexts.
- Always verify which layer the current prompt is actually about.

### 2. Unrequested translation or localization

- Do not invent translation files or new locale keys.
- Reuse existing localization assets when they already exist.
- If localization is required, explain the path instead of creating it blindly.

### 3. CSS or style generation

- Do not write `<style>` blocks.
- Do not add inline styles.
- If styling is needed, suggest class names or a separate styling task.

### 4. Vendor-specific SQL without justification

- Avoid vendor-specific SQL unless the repository already depends on it.
- Prefer portable SQL or the repository's documented database conventions.

### 5. Path guessing

- Do not invent file paths or folders that are not present in the repository or `PATHS.md`.
- Only refer to paths that are already documented or observable in the tree.

## Restricted behaviors

- Do not propose large refactors when a smaller change is enough.
- Do not make the final decision for the user when multiple safe options exist.
- Do not suggest changing repository policy to solve a local implementation issue unless the current policy is actually the problem.

## Required attitude

1. Check the current layer before answering.
2. Prefer evidence over intuition.
3. Keep the response safe, small, and reversible when possible.

## Violation handling

If a request appears to violate these rules:

1. Stop.
2. Explain the conflict briefly.
3. Offer a safer alternative.

## Final principle

Safety over speed. Context over guesswork.
