---
name: "Multi-Agent Skill Guide"
status: "draft"
tags: ["guide-dnl"]
paths:
  "@skills-portal.md": "{@dnl-root}/.agents/skills/README.md"
  "@skill-source-migration.md": "{@dnl-root}/docs/skill-source-migration.md"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@dnl-query.md": "{@dnl-root}/.agents/skills/dnl-query/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
---

# Multi-Agent Skill Guide


이 문서는 여러 AI 에이전트가 `.agents/skills` 정본 스킬을 일관되게 사용하도록 하기 위한 운영 가이드입니다.

## 핵심 원칙
- 스킬 정본은 항상 `.agents/skills/{skill-name}` 입니다.
- 에이전트별 `*/skills/{skill-name}/SKILL.md`는 필수 구조가 아니라, 필요한 도구만 유지하는 라우팅 래퍼입니다.
- 래퍼는 짧게 유지하고, 상세 지침은 정본 스킬 문서에만 둡니다.
- 신규 스킬 추가/이름 변경 시 지원 중인 래퍼만 함께 동기화합니다.
- Codex와 Antigravity/Gemini 계열은 repo-local 래퍼 없이 `.agents/skills`를 직접 참조합니다.
- `.codex`, `.antigravity`, `GEMINI.md`, `.kiro`, `.windsurfrules`는 현재 운영 표면이 아니므로 새로 만들지 않습니다.
- 스킬 정본 위치 자체를 바꾸는 작업은 일반 스킬 수정이 아니라 `@skill-source-migration.md`를 따릅니다.

## 공통 구조
```text
.agents/skills/
  <skill-name>/
    SKILL.md
    (scripts/references/assets...)

.claude/skills/<skill-name>/SKILL.md
.github/skills/<skill-name>/SKILL.md
.cursor/skills/<skill-name>/SKILL.md
```

## 스킬 실행 흐름 (모든 AI 공통)
1. 루트 `AGENTS.md`를 먼저 읽습니다.
2. `README.md`와 `docs/`는 public explanation, onboarding, README/docs 작업일 때만 읽습니다.
3. 현재 AI에 유지 중인 래퍼 `SKILL.md`가 있으면 짧은 라우터로만 사용합니다.
4. 정본 `.agents/skills/{skill}/SKILL.md`를 읽습니다.
5. 필요 시 정본 스킬의 스크립트/참조 파일만 추가로 읽습니다.

## 신규 스킬 추가 체크리스트
1. `.agents/skills/{skill-name}/SKILL.md`를 생성합니다.
2. `@skills-portal.md`의 Skills 목록에 항목을 추가합니다.
3. 필요한 경우 아래 지원 래퍼 경로에 동일한 이름으로 `SKILL.md`를 생성합니다.
   - `.claude/skills/{skill-name}/SKILL.md`
   - `.github/skills/{skill-name}/SKILL.md`
   - `.cursor/skills/{skill-name}/SKILL.md`
4. 래퍼 내용은 정본 스킬로 연결하는 최소 지시만 유지합니다.
5. Codex, Antigravity/Gemini, Kiro, Windsurf용 repo-local 파일은 만들지 않습니다.

## 기존 스킬 수정 체크리스트
1. 정본 `.agents/skills/{skill-name}/SKILL.md`를 먼저 수정합니다.
2. 필요할 때만 지원 중인 래퍼의 설명(`name`, `description`)을 동기화합니다.
3. 경로/명칭이 바뀌었다면 지원 중인 래퍼 경로만 함께 수정합니다.

## 권장 검증 명령
구조 확인:
```bash
python .agents/skills/tree/tree.py --root . --depth 3 --hidden --ascii
```

DNL 링크 품질 확인:
```bash
python .agents/skills/dnl-builder/qa.py --profile links --fail-on all
```

## 래퍼 템플릿
```markdown
---
name: <skill-name>
description: <trigger description>
---

read `AGENTS.md` of root directory and get the information about the project.
then, read `{@dnl-root}/.agents/skills/<skill-name>/SKILL.md` as the canonical skill source.
```
