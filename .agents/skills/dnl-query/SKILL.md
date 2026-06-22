---
name: dnl-query
description: DNL 문서를 수정하지 않고 tag/name/status/path 조건으로 빠르게 찾아야 할 때 사용하는 조회 스킬
---

# DNL Query

`.agents/skills/dnl-query`는 DNL 문서를 수정하지 않고 찾기만 할 때 사용합니다.

## 언제 사용하나

- 태그로 DNL 문서를 찾을 때
- `name`, `status`, 경로 prefix 조건으로 문서를 좁힐 때
- 많은 markdown을 직접 스캔하지 않고 생성된 index를 읽고 싶을 때
- 문서의 outbound link, backlinks, unresolved path 후보를 빠르게 확인할 때

## 기본 사용

```bash
# 태그 목록과 count
python3 .agents/skills/dnl-query/dnl_query.py tags

# 특정 태그 문서 목록
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl

# 경로만 출력
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format paths

# AI 후속 처리용 JSONL
python3 .agents/skills/dnl-query/dnl_query.py docs --tag glossary-dnl --format jsonl

# 문서가 선언한 outbound link
python3 .agents/skills/dnl-query/dnl_query.py links --path docs/index.md

# 특정 문서를 참조하는 source 문서
python3 .agents/skills/dnl-query/dnl_query.py backlinks --path DNL-system/README.md

# 내부 target 미해결 후보
python3 .agents/skills/dnl-query/dnl_query.py unresolved

# 미해결 후보를 source 디렉토리별로 요약
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary

# 선언됐지만 본문에서 쓰이지 않은 path token 후보
python3 .agents/skills/dnl-query/dnl_query.py unused

# 본문에 있지만 YAML paths에 없는 파일형/path형 token 후보
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens
```

## link health 조회 순서

문서 연결 건강검진은 먼저 요약으로 범위를 좁힌 뒤 상세 record를 봅니다.

```bash
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary
python3 .agents/skills/dnl-query/dnl_query.py unresolved --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --under docs --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --under docs --format jsonl
```

## 추천 태그

처음에는 아래 태그로 후보를 좁힙니다.

- 구조/탐색: `portal-dnl`, `map-dnl`, `glossary-dnl`, `rule-dnl`
- 작업 성격: `guide-dnl`, `playbook-dnl`, `runbook-dnl`, `reference-dnl`, `troubleshooting-dnl`
- 주제/기술: `auth`, `api`, `sql`, `i18n`, `svelte`, `migration`

현재 index의 전체 태그와 count는 `python3 .agents/skills/dnl-query/dnl_query.py tags`로 확인합니다.

## 역할 경계

- 찾기: `.agents/skills/dnl-query/dnl_query.py`
- 구조 보기: `.agents/skills/tree/tree.py`
- 작성/정비/검증: `.agents/skills/dnl-builder`

`dnl-query`는 index를 읽기만 합니다.
tag index 생성/최신성 확인/파일 1개 갱신은 `.agents/skills/dnl-builder/dnl_util.py tag index ...`를 사용합니다.
link index 생성/최신성 확인은 `.agents/skills/dnl-builder/dnl_util.py link index ...`를 사용합니다.

## index가 없을 때

tag/link index는 git에 커밋하지 않는 로컬 생성물입니다.
index가 없거나 최신성이 의심되면 아래 명령으로 생성합니다.

```bash
python3 .agents/skills/dnl-builder/dnl_util.py tag index build
python3 .agents/skills/dnl-builder/dnl_util.py link index build
```
