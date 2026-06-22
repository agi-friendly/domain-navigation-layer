---
name: "ai - AI 운영 포털"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@context-loading.md": "context-loading.md"
  "@doc-selection-rules.md": "doc-selection-rules.md"
  "@output-format.md": "output-format.md"
  "@guardrails.md": "guardrails.md"
  "@prompt-playbook.md": "prompt-playbook.md"
  "@local-context.md": "{@DNL-system}/ai/local-context/README.md"
  "@paths-md.md": "{@DNL-system}/ai/local-context/paths-md.md"
  "@current-user-md.md": "{@DNL-system}/ai/local-context/current-user-md.md"
  "@dnl-builder.md": "{@DNL-system}/authoring/README.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
  "@future-to-archive.md": "{@DNL-system}/workflow/future-to-archive.md"
---

# ai - AI 운영 포털


> 이 디렉토리는 DNL을 활용하는 **AI 에이전트 운영 규칙**을 모아둔 포털입니다.

---

## 추천 읽기 순서
1. `@context-loading.md` — 필요한 문서만 읽는 규칙
2. `@doc-selection-rules.md` — 어떤 문서를 선택할지(키워드→포털→세부)
3. `@output-format.md` — 산출물 포맷 통일
4. `@guardrails.md` — 안전 가드

## Repository-local context

Repository-local path and user handoff notes live under `ai/local-context/` so they can be managed as DNL documents.

- `@local-context.md`
- `@paths-md.md`
- `@current-user-md.md`

---

## DNL 문서 작업 라우팅

프롬프트가 아래에 해당하면 일반 코드 탐색보다 먼저 `@dnl-builder.md`로 이동합니다.

- `DNL 개선`
- `문서화`
- `README 정리`
- `YAML paths`
- `@토큰`
- `HUMAN_LINK 제거`
- `파일링크 금지`
- `라우팅 개선`
- `dnl builder`
- `future`, `future-to-dnl`, promotion, archive, history 정리

읽기 순서는 다음을 따릅니다.

1. `@dnl-builder.md`
2. `@markdown-rule.md`
3. `@yaml-frontmatter-rule.md`
4. `@multi-dnl-authority.md`
5. `@dnl-authoring-playbook.md`
6. 작업이 `future` 자료 흡수, DNL promotion, archive 판단, history 정리를 포함하면 `@workflow-root.md` → `@future-to-dnl.md` → 필요 시 `@future-to-archive.md`
7. 실제로 수정할 대상 문서

> 목적: DNL 문서 작업을 일반 코드 탐색으로 오인하지 않고, 작성 규칙과 권위 체계를 먼저 고정합니다.
> workflow는 작업 묶음의 수명주기 정본이고, authoring은 문서 작성 규칙 정본입니다.

---

## Project-level AI 문서 작성 원칙 (Override 방식)

Project DNL에서 `ai/` 디렉토리를 둘 수는 있지만, 아래 원칙을 지킵니다.

1. **정본은 DNL-system AI 문서(`{@DNL-system}/ai`)**
   - Project DNL은 여기 내용을 **복제하지 않습니다.**
2. Project-level `ai/`에는 아래만 둡니다.
   - `ai/README.md` : “정본은 DNL-system/ai”임을 선언하고 링크 제공
   - `ai/overrides.md` : 해당 프로젝트에만 해당하는 **추가 규칙/예외(Override)**만 작성 *(권장 파일명)*
3. Override가 필요하면 반드시 문서에 **명시적으로 선언**합니다.
   - 예: `Override: 이 프로젝트에서는 ...`

> 목표: “규칙이 프로젝트마다 복제되면서 서로 다른 버전으로 진화”하는 상황을 막는다.
