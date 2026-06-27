---
name: ".agents/skills/dnl-query"
status: "draft"
tags: ["portal-dnl", "dnl-query"]
paths:
  "@dnl-query.py": "{@dnl-root}/.agents/skills/dnl-query/dnl_query.py"
  "@dnl-builder.md": "{@dnl-root}/.agents/skills/dnl-builder/SKILL.md"
  "@tree.md": "{@dnl-root}/.agents/skills/tree/SKILL.md"
  "@tag-index": "{@dnl-root}/.agents/skills/dnl-query/tag-index"
  "@link-index": "{@dnl-root}/.agents/skills/dnl-query/link-index"
---

# .agents/skills/dnl-query

`dnl-query`는 DNL 문서를 수정하지 않고 조회하는 스킬입니다.
생성된 tag index를 읽어 태그, 상태, 이름, 경로 조건으로 필요한 DNL 문서를 빠르게 찾습니다.

## 역할

- 태그 목록과 count 확인
- 특정 태그를 가진 DNL 문서 조회
- `status`, `name`, path prefix 조건으로 문서 후보 좁히기
- link index 기반 outbound/inbound link 조회
- unresolved internal path 후보 확인
- AI가 후속 작업에 쓰기 좋은 `paths`, `jsonl`, `json` 출력 제공

## 책임 경계

- 찾기: `@dnl-query.py`
- 구조 보기: `@tree.md`
- 작성/정비/검증/index 갱신: `@dnl-builder.md`

`dnl-query`는 index를 읽기만 합니다.
tag index 생성/최신성 확인/파일 1개 갱신은 `dnl-builder`의 `tag index` 명령이 담당합니다.
link index 생성/최신성 확인은 `dnl-builder`의 `link index` 명령이 담당합니다.

## 기본 명령

```bash
# 태그 목록과 count
python3 .agents/skills/dnl-query/dnl_query.py tags

# 특정 태그 문서 목록
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl

# 경로만 출력
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format paths

# AI 후속 처리용 JSONL
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format jsonl

# 문서가 선언한 outbound link 조회
python3 .agents/skills/dnl-query/dnl_query.py links --path docs/index.md

# 특정 문서를 참조하는 source 문서 조회
python3 .agents/skills/dnl-query/dnl_query.py backlinks --path DNL-system/README.md

# 내부 target 미해결 후보 조회
python3 .agents/skills/dnl-query/dnl_query.py unresolved

# 미해결 후보를 source 디렉토리별로 요약
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# 선언됐지만 본문에서 쓰이지 않은 path token 후보
python3 .agents/skills/dnl-query/dnl_query.py unused

# 본문에 있지만 YAML paths에 없는 파일형/path형 token 후보
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens
```

## 필터

```bash
# 여러 태그를 모두 가진 문서
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --tag reference-dnl

# 상태 필터
python3 .agents/skills/dnl-query/dnl_query.py docs --tag rule-dnl --status draft

# 하위 경로 필터
python3 .agents/skills/dnl-query/dnl_query.py docs --tag rule-dnl --under docs

# name 부분 검색
python3 .agents/skills/dnl-query/dnl_query.py docs --name "OIDC"

# unresolved source 범위 축소
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary --under docs --depth 3
```

필터는 AND 조건으로 조합됩니다.

## 추천 태그

AI가 어떤 태그로 시작할지 모를 때는 아래 기준으로 먼저 조회합니다.
현재 index에 존재하는 전체 태그와 count는 `python3 .agents/skills/dnl-query/dnl_query.py tags`가 정본입니다.

### 구조/탐색

| 태그 | 먼저 찾을 때 |
| --- | --- |
| `portal-dnl` | README/진입점/하위 문서 라우팅 |
| `map-dnl` | 모듈, 화면, 패키지, 소스 연결 지도 |
| `glossary-dnl` | 용어, 약어, 화면명, 공통 명칭 |
| `rule-dnl` | 작성 규칙, 판단 규칙, 개발 규칙 |
| `template-dnl` | 요청/출력 템플릿 |

### 작업 성격

| 태그 | 먼저 찾을 때 |
| --- | --- |
| `guide-dnl` | 사용법, 작성법, 통합 가이드 |
| `playbook-dnl` | 반복 작업 절차 |
| `runbook-dnl` | 운영/장애 대응 절차 |
| `reference-dnl` | 빠르게 확인하는 참조 문서 |
| `troubleshooting-dnl` | 문제 해결, 흔한 실수, 증상별 대응 |

### 주제/기술

| 태그 | 먼저 찾을 때 |
| --- | --- |
| `auth` | 인증, 권한, OIDC, JWT, 세션 |
| `api` | API 계약, client/server 연동 |
| `sql` | DB, DDL, mapper, query |
| `i18n` | 다국어, 메시지 키, paraglide |
| `svelte` | Svelte/SvelteKit 규칙과 문제 해결 |
| `migration` | 버전 전환, legacy-to-new, 포팅 |
| `important` | 사용자나 AI가 우선 확인해야 하는 핵심 문서 |

### 모듈 예시

모듈 태그는 반복 사용해도 됩니다.
특정 업무 모듈의 문서만 빠르게 좁힐 때 사용합니다.

```bash
python3 .agents/skills/dnl-query/dnl_query.py docs --tag guide-dnl --format paths
python3 .agents/skills/dnl-query/dnl_query.py docs --tag reference-dnl --format paths
python3 .agents/skills/dnl-query/dnl_query.py docs --tag portal-dnl --format paths
```

## 출력 포맷

- `text`: `path | status | name`
- `paths`: path만 1줄 1개
- `jsonl`: 1줄 1개 JSON
- `json`: JSON 배열

## Link health 조회

link health는 먼저 요약으로 문제가 많은 영역을 찾고, 그 다음 상세 record를 좁혀 봅니다.

```bash
# source directory별 unresolved count
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# 특정 범위만 보기
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary --under docs --depth 3

# 상세 후보 확인
python3 .agents/skills/dnl-query/dnl_query.py unresolved --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --under docs --format jsonl
```

`unresolved`는 target 경로가 resolve되지 않는 후보, `unused`는 YAML `paths`에 선언됐지만 본문에서 쓰이지 않은 token 후보,
`missing-tokens`는 본문에 있지만 YAML `paths`에 없는 파일형/path형 token 후보입니다.

## Index

기본 index 위치는 `@tag-index`입니다.
link 조회 명령은 `@link-index`를 읽습니다.
index 파일은 git에 커밋하지 않는 로컬 생성물입니다.
index가 없거나 최신성이 의심되면 아래 명령을 사용합니다.

```bash
# tag index 전체 재생성
python3 .agents/skills/dnl-builder/dnl_util.py tag index build

# tag index 최신성 확인
python3 .agents/skills/dnl-builder/dnl_util.py tag index check

# link index 전체 재생성
python3 .agents/skills/dnl-builder/dnl_util.py link index build

# link index 최신성 확인
python3 .agents/skills/dnl-builder/dnl_util.py link index check
```
