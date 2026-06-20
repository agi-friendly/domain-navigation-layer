---
name: "YAML frontmatter 작성 규칙"
status: "draft"
tags: ["rule-dnl", "yaml-frontmatter", "dnl-builder"]
description:
  - "이 문서는 DNL markdown 상단 YAML frontmatter의 필드 순서, 상태, 태그, 설명, 경로 선언 규칙을 설명한다."
paths:
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@dnl-config.toml": "{@dnl-root}/dnl-config.toml"
---

# YAML frontmatter 작성 규칙

> 이 문서는 DNL markdown 문서의 상단 YAML frontmatter 작성 규칙이다.
> 일반 markdown 작성 규칙과 링크 정책은 `@markdown-rule.md`를 따른다.

## Scope

This rule applies to DNL markdown documents whose paths are included by `scan.include` in `dnl-config.toml`.
In this public starter, that currently means `DNL-system` and `DNL-example`.

- Included: the markdown documents under `scan.include`
- Excluded: `SKILL.md`, repository-root markdown, documents under hidden directories that start with `.`, and gitignored files
- Documents under `.agents/skills` are agent tool docs, so they follow tool-specific rules and stay out of DNL YAML QA/indexing by default

## 필드 순서

frontmatter 필드 순서는 아래를 기준으로 한다.

1. `name`
2. `status`
3. `tags`
4. `description` (optional)
5. `paths` (optional)

예시:

```yaml
---
name: "샘플 화면"
status: "draft"
tags: ["portal-dnl", "screen", "eml"]
description:
  - "이 문서는 샘플 화면의 구조와 주요 진입점을 설명한다."
paths:
  "@sample-screen.md": "{@dnl-root}/docs/sample-dnl/sample-product/sample-project/screens/sample-screen/README.md"
---
```

## 공통 YAML 규칙

- 들여쓰기는 space 2칸을 사용한다.
- 문자열 값은 큰따옴표로 감싼다.
- 빈 값을 의미 없이 채우지 않는다.
- 필드 순서를 임의로 바꾸지 않는다.
- `description`, `paths`는 필요할 때만 작성한다.

## name

`name`은 문서의 표시 이름이다.

규칙:

- 필수 필드다.
- 사람이 보고 문서 목적을 이해할 수 있는 이름을 쓴다.
- 가능하면 첫 번째 H1 제목과 같은 의미를 유지한다.

예시:

```yaml
name: "전자우편 화면 지도"
```

## status

`status`는 문서의 신뢰 상태를 표시한다.

규칙:

- 필수 필드다.
- 기본값은 `"draft"`다.
- 허용 값은 아래 3개뿐이다.

| status | 의미 |
| --- | --- |
| `"active"` | 현재 기준으로 신뢰 가능한 정본 문서 |
| `"draft"` | 신규 작성, 수정 중, 검토 필요, 오래되어 최신성 확인이 필요한 문서 |
| `"deprecated"` | 대체 문서가 있거나, 현재 정본 탐색에서는 기본으로 쓰지 않는 보존/아카이브 문서 |

AI 작성 규칙:

- AI가 새 DNL 문서를 만들 때는 `status: "draft"`로 작성한다.
- AI가 기존 `active` 문서를 의미 있게 수정하면 `status: "draft"`로 바꾼다.
- AI는 사용자의 명시 요청 없이 문서를 `active`로 승격하지 않는다.
- AI는 사용자의 명시 요청 없이 문서를 `deprecated`로 변경하지 않는다.

## tags

`tags`는 문서 검색, 인덱싱, tree 필터링을 위한 분류 값이다.

규칙:

- 필수 필드다.
- inline list 형식으로 작성한다.
- 태그가 아직 없으면 빈 list를 사용한다.
- 같은 태그를 중복해서 넣지 않는다.
- `@dnl-config.toml`의 required tag 규칙을 만족해야 한다.
- 현재 기본 config에서는 `README.md` 파일에 `portal-dnl` 태그를 요구한다.
- 경로 패턴에 따라 `rule-dnl`, `runbook-dnl` 같은 추가 required tag가 적용될 수 있다.

예시:

```yaml
tags: ["portal-dnl", "screen", "troubleshooting"]
```

태그 문자 규칙:

- 소문자 kebab-case를 사용한다.
- 영문 소문자와 숫자를 사용할 수 있다.
- 공백은 사용할 수 없다.
- 특수문자는 `-`와 `:`만 사용할 수 있다.
- `:`는 최대 1개만 사용할 수 있다.
- 한글, 대문자, `_`는 사용하지 않는다.

정규식 기준:

```text
^[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?$
```

## 태그 추천 후보

태그는 문서 성격을 빠르게 좁히기 위한 힌트다.
폴더 구조로 이미 알 수 있는 정보를 기계적으로 반복하지 말고, 검색/필터링에 의미가 있을 때만 추가한다.

### 구조 태그

- `portal-dnl`: 다른 DNL 문서로 들어가는 README/포털 문서
- `map-dnl`: 경로, 모듈, 화면, 소스 연결 지도
- `glossary-dnl`: 용어/약어/개념 사전
- `rule-dnl`: 작성 규칙, 판단 규칙, 운영 규칙
- `template-dnl`: 요청/출력 템플릿

### 문서 성격 태그

- `guide-dnl`: 사용법이나 작성법을 설명하는 가이드
- `playbook-dnl`: 반복 작업 절차
- `runbook-dnl`: 장애/운영 대응 절차
- `reference-dnl`: 빠르게 확인하는 참조 문서
- `troubleshooting-dnl`: 문제 해결 문서

### 대상 태그

대상 태그는 현재 문서가 위치한 폴더만 반복하기 위해 쓰지 않는다.
현재 문서가 다른 계층이나 서비스와의 관계를 설명할 때 사용한다.

- `example-company`
- `sample-product`
- `sample-project`
- `sample-module`
- `sample-service`

예시:

- 샘플 product 문서가 다른 product 차이를 설명할 때 `sample-product`
- 샘플 project 문서가 외부 service 연동을 설명할 때 `sample-service`

### 모듈 태그

모듈 태그는 반복 사용해도 된다.
화면, API, 장애, 지도 문서를 모듈 단위로 다시 필터링할 때 도움이 되면 사용한다.

- `eml`
- `org`
- `mmo`
- `ptl`
- `prj`

### 기술/주제 태그

- `java`
- `svelte`
- `sql`
- `api`
- `screen`
- `auth`
- `i18n`
- `migration`

### 강조 태그

- `important`: 사용자나 AI가 우선적으로 확인해야 하는 핵심 문서

## description

`description`은 문서가 무엇을 설명하는지 짧게 적는 optional 필드다.

규칙:

- list 형식으로 작성한다.
- 1~3개 문장을 권장한다.
- 각 항목은 "이 문서는 ..." 흐름으로 작성한다.
- 본문 요약 전체를 복붙하지 않는다.
- 문서 목적, 읽어야 하는 상황, 포함 범위를 짧게 설명한다.

예시:

```yaml
description:
  - "이 문서는 샘플 화면의 구조와 주요 진입점을 설명한다."
  - "AI가 샘플 화면 관련 문서를 찾을 때 출발점으로 사용한다."
```

## paths

`paths`는 이 문서에서 사용할 `@토큰`과 논리 경로를 선언하는 optional 필드다.

규칙:

- `paths`가 필요 없으면 생략할 수 있다.
- 선언한다면 map 형식을 사용한다.
- key는 `@`로 시작한다.
- key와 value는 큰따옴표로 감싼다.
- 같은 key를 중복해서 선언하지 않는다.
- 같은 path 값을 여러 key로 반복하지 않는다.
- path 값은 가능하면 `{@변수}/...` 기반 논리 경로를 사용한다.

예시:

```yaml
paths:
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
```

잘못된 예시:

```yaml
paths:
  - "@markdown-rule.md: {@DNL-system}/authoring/rules/markdown-rule.md"
```

## 신규/수정 문서 작성 절차

1. 새 문서는 `status: "draft"`로 시작한다.
2. 파일명이 `README.md`면 `tags`에 `portal-dnl`을 넣는다.
3. 문서 성격에 맞는 태그를 1~3개 정도 추가한다.
4. `description`은 문서 목적을 빠르게 전달할 가치가 있을 때만 쓴다.
5. 본문에서 참조할 문서/파일은 `paths`에 선언하고 `@토큰`으로 사용한다.
6. 사용자가 명시적으로 요청하지 않는 한 `active`, `deprecated` 상태 변경은 하지 않는다.
