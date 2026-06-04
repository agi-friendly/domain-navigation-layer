---
name: "Agents Skills Portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@multi-agent-skill-guide.md": "{@dnl-root}/.agents/skills/multi-agent-skill-guide.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@dnl-query.md": "{@dnl-root}/.agents/skills/dnl-query/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
---

# Agents Skills Portal


## 목적
- 이 디렉토리는 스킬의 정본(Source of Truth)입니다.
- 모든 AI는 최종적으로 `.agents/skills/{skill}/SKILL.md`를 읽습니다.
- `.claude`, `.cursor`, `.github`의 `skills/*/SKILL.md`는 도구 호환을 위한 라우팅 래퍼입니다.
- Codex와 Antigravity/Gemini 계열은 repo-local 래퍼 없이 `.agents/skills`를 직접 참조합니다.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, `.windsurfrules`는 현재 운영 표면이 아니므로 새로 만들지 않습니다.

## 공통 사용 순서
1. 루트 `README.md`, `AGENTS.md`를 먼저 읽습니다.
2. 현재 AI에 유지 중인 래퍼 파일이 있으면(`<agent>/skills/{skill}/SKILL.md`) 먼저 읽습니다.
3. 래퍼가 없으면 `.agents/skills/README.md`와 이 문서를 기준으로 바로 정본 스킬 문서로 이동합니다.
4. 정본 스킬 문서(`.agents/skills/{skill}/SKILL.md`)를 읽고 필요한 스크립트/참조만 추가 로딩합니다.
5. 스크립트 실행/수정은 항상 `.agents/skills/{skill}` 기준 경로로 수행합니다.

## 멀티 에이전트 가이드
- 상세 규칙과 체크리스트: `@multi-agent-skill-guide.md`

## Skills
- `dnl-builder` (`@dnl-builder.md`)
  - DNL 작성/정비 정본 문서(`DNL-system/authoring`)로 라우팅하고 QA를 제공.
- `dnl-query` (`@dnl-query.md`)
  - 생성된 tag index를 읽어 tag/name/status/path 조건으로 DNL 문서를 조회.
- `tree` (`@tree.md`)
  - Python 기반 트리 구조 분석 도구(Windows `tree` 대체).