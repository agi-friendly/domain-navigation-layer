---
name: "Agents Skills Portal"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@multi-agent-skill-guide.md": "{@dnl-root}/.agents/skills/multi-agent-skill-guide.md"
  "@skill-source-migration.md": "{@dnl-root}/docs/skill-source-migration.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@dnl-query.md": "{@dnl-root}/.agents/skills/dnl-query/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
---

# Agents Skills Portal


## 목적
- 이 디렉토리는 스킬의 정본(Source of Truth)입니다.
- 모든 AI는 최종적으로 `.agents/skills/{skill}/SKILL.md`를 읽습니다.
- 에이전트별 `skills/*/SKILL.md`는 도구 호환을 위한 짧은 라우팅 래퍼입니다.
- Codex와 Antigravity/Gemini 계열은 repo-local 래퍼 없이 `.agents/skills`를 직접 참조합니다.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, `.windsurfrules`는 현재 운영 표면이 아니므로 새로 만들지 않습니다.

## 공통 사용 순서
1. 루트 `AGENTS.md`를 먼저 읽습니다.
2. `README.md`와 `docs/`는 public explanation, onboarding, README/docs 작업일 때만 읽습니다.
3. 현재 AI에 유지 중인 래퍼 파일이 있으면(`<agent>/skills/{skill}/SKILL.md`) 짧은 라우터로만 사용합니다.
4. 정본 스킬 문서(`.agents/skills/{skill}/SKILL.md`)를 읽고 필요한 스크립트/참조만 추가 로딩합니다.
5. 스크립트 실행/수정은 항상 `.agents/skills/{skill}` 기준 경로로 수행합니다.

## 멀티 에이전트 가이드
- 상세 규칙과 체크리스트: `@multi-agent-skill-guide.md`
- 스킬 정본 위치를 `.agents/skills` 밖으로 옮기거나 다른 tool-specific 폴더에서 모아올 때: `@skill-source-migration.md`

## Skills
- `dnl-builder` (`@dnl-builder.md`)
  - DNL 작성/정비 정본 문서(`DNL-system/authoring`)로 라우팅하고 QA를 제공.
- `dnl-query` (`@dnl-query.md`)
  - 생성된 tag index를 읽어 tag/name/status/path 조건으로 DNL 문서를 조회.
- `tree` (`@tree.md`)
  - Python 기반 트리 구조 분석 도구(Windows `tree` 대체).
