---
name: ".agents/skills/dnl-builder"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-util.py": "{@dnl-root}/.agents/skills/dnl-builder/dnl_util.py"
  "@dnl-config.toml": "{@dnl-root}/dnl-config.toml"
---

# .agents/skills/dnl-builder

이 디렉토리는 DNL 문서 작업을 위한 AI 진입점입니다.
정본 작성 규칙은 `DNL-system/authoring`에 두고, 이 디렉토리는 그 정본으로 라우팅하며 QA 도구를 제공합니다.

## 역할

- `DNL-system/authoring` 정본 문서로 라우팅
- `qa.py`로 DNL 품질 점검
- `dnl_util.py`로 DNL 문서 대량 정비 보조
- 멀티 에이전트 환경에서 동일한 진입점 제공

## 기본 자세

`dnl-builder`를 사용하는 AI는 "문서 하나를 고치는 작업자"가 아니라, DNL 전체가 1년 뒤에도 길을 잃지 않도록 운영하는 총괄담당자 관점으로 판단합니다.

좋은 DNL 작업은 내용 추가보다 길 정리에 가깝습니다. 새 정본을 만들었으면 상위 README, 모듈 지도, 화면 지도, future 허브가 그 정본으로 이어지는지 확인하고, 과거 메모가 현재 경로인 것처럼 남지 않게 정리합니다.

문서가 길어질수록 더 많이 설명하지 말고 더 잘 나눕니다. 포털/README는 현재 결론과 다음 경로만 남기고, 조사 근거·비교표·이전 계획은 필요할 때 여는 보조 문서로 분리합니다.

## DNL 문서 작업 시 권장 읽기 순서

1. `DNL-system/authoring/README.md`
2. `DNL-system/authoring/rules/markdown-rule.md`
3. `DNL-system/authoring/rules/yaml-frontmatter-rule.md`
4. `DNL-system/authoring/rules/multi-dnl-authority.md`
5. `DNL-system/authoring/dnl-authoring-playbook.md`
6. `.agents/skills/dnl-builder/README.md`

## 권장 작업 루틴

1. 작업이 DNL 문서화/라우팅/README 정리인지 먼저 판단합니다.
2. DNL 작업이면 정본 규칙 문서를 먼저 읽고, 변경 범위와 레이어를 좁힙니다.
3. 대상 문서의 역할을 정합니다: 라우터, 정본, 배경, future, archive.
4. 대상 문서를 수정합니다.
5. 상위 README, 관련 지도/가이드, cross-link가 새 정본을 가리키는지 확인합니다.
6. 옛 경로, 옛 우선순위, 완료 주장과 실제 라우팅 불일치 같은 semantic stale을 검색합니다.
7. QA를 실행하고, 리포트를 보고 필요한 정리를 마칩니다.

## dnl-config.toml

`@dnl-config.toml`은 dnl-builder 계열 도구가 공유하는 프로젝트 지도입니다.

- `qa.py --profile full`은 `scan.include`와 `scan.exclude`를 사용합니다.
- `qa.py --profile portal`은 `profiles.portal`로 스캔 범위를 잡고, `portal.readme_dirs`로 포털 README 디렉토리명을 판단합니다.
- tag index build/check/update는 같은 scan 범위로 index를 만듭니다.
- QA required tag 검사는 `tags.required_by_filename`, `tags.required_by_path`를 사용합니다.

`dnl-config.toml`은 DNL 정책을 바꾸는 파일이 아닙니다.
YAML 필수 필드, field order, status/tag/token 형식, 숨김 디렉토리와 `SKILL.md` 제외 규칙은 코드와 `DNL-system/authoring/rules/yaml-frontmatter-rule.md`가 기준입니다.

## QA (lint)

- 실행:
  - 전체 스캔(기본): `python3 .agents/skills/dnl-builder/qa.py`
  - 기본은 `--fail-on all`이므로, 이슈가 있으면 비0 종료합니다.
  - 설정된 포털 범위만: `python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all`
  - 링크 중심(노이즈 적게): `python3 .agents/skills/dnl-builder/qa.py --profile links`
  - link-index health summary(report-only): `python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary`
  - 실패 정책 조정: `--fail-on none|low|med|high|all`
  - JSON 요약 출력: `python3 .agents/skills/dnl-builder/qa.py --json-summary`

- 결과 리포트:
  - 기본값: `.agents/skills/dnl-builder/reports/qa-report.md`

- 터미널 출력 규칙:
  - 이슈가 없으면 `SUCCESS`
  - 이슈가 있지만 현재 `--fail-on` 정책상 실패는 아니면 `WARN`
  - 이슈가 있고 현재 `--fail-on` 정책상 실패면 `FAIL`
  - `WARN`/`FAIL`에는 문제 유형별 카운트와 리포트 경로를 함께 출력합니다.
  - `--json-summary`를 주면 텍스트 대신 JSON 요약을 `stdout`으로 출력합니다.
  - 종료 코드는 `SUCCESS`/`WARN`이면 `0`, `FAIL`이면 `1`입니다.

- 체크 항목(요약):
  - YAML frontmatter 필수 필드(`name`, `status`, `tags`) 존재 여부
  - YAML frontmatter field order/status/tag/path 형식
  - `dnl-config.toml`의 required tag 규칙 준수 여부
  - 포털 README의 YAML `paths` 존재 여부
  - `## HUMAN_LINKS` 섹션 존재 여부
  - `- [HUMAN_LINK]` 라인 존재 여부
  - 로컬 markdown 파일/폴더 링크 존재 여부
  - `../../` 이상의 깊은 상대경로 링크 탐지
  - 깨진 로컬 링크(베스트에포트)
  - `--profile health`에서 link-index unresolved/unused/missing token count 요약

> 리포트는 `.agents/skills/dnl-builder/reports/` 아래에 생성되며, 해당 경로는 git ignore 처리되어 있습니다.

## DNL utility

`@dnl-util.py`는 DNL 문서 대량 정비용 유틸리티 진입점입니다.
기본은 dry-run이며, 실제 파일 수정은 `--write`를 명시해야 합니다.

- 태그 추가 dry-run:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs --tag guide-dnl --recursive`
- 태그 추가 write:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs --tag guide-dnl --recursive --write`

태그 추가 명령은 YAML frontmatter의 `tags` 필드만 변경합니다.
숨김 디렉토리, gitignored 파일, `SKILL.md`, generated `reports` 문서는 수정하지 않습니다.

### Tag index

태그 인덱스는 태그 검색/목록/audit/tree 필터가 전체 markdown을 매번 스캔하지 않도록 미리 생성한 JSONL 색인입니다.
기본 출력 위치는 `.agents/skills/dnl-query/tag-index/`입니다.
`dnl-builder`는 index를 만들고 갱신하며, `dnl-query`는 생성된 index를 읽습니다.
index 대상 범위는 `dnl-config.toml`의 `scan.include`, `scan.exclude`를 따릅니다.

- 전체 재생성:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index build`
- 최신성 확인:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index check`
- 파일 1개 갱신:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index update --path docs/index.md`

생성 파일:

- `.agents/skills/dnl-query/tag-index/manifest.json`: 문서 수와 태그별 파일/count
- `.agents/skills/dnl-query/tag-index/all-docs.jsonl`: index 대상 전체 문서 메타데이터
- `.agents/skills/dnl-query/tag-index/tags/*.jsonl`: 태그별 문서 목록

### Link index

link index는 YAML `paths` 선언과 본문 `@토큰` 사용 관계를 색인합니다.
기본 출력 위치는 `.agents/skills/dnl-query/link-index/`입니다.
첫 구현은 health-check report 기반이며, unresolved/unused/missing token을 바로 QA fail로 올리지 않습니다.

- 전체 재생성:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index build`
- 최신성 확인:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index check`

생성 파일:

- `.agents/skills/dnl-query/link-index/manifest.json`: 문서/link/report count
- `.agents/skills/dnl-query/link-index/all-links.jsonl`: YAML `paths` 기반 outbound link 목록
- `.agents/skills/dnl-query/link-index/backlinks.jsonl`: 내부 target 기준 inbound source 목록
- `.agents/skills/dnl-query/link-index/unresolved-paths.jsonl`: 내부 target 미해결 후보
- `.agents/skills/dnl-query/link-index/unused-paths.jsonl`: 선언됐지만 본문에서 쓰이지 않은 token 후보
- `.agents/skills/dnl-query/link-index/missing-path-tokens.jsonl`: 본문에 있으나 `paths`에 없는 파일형/경로형 token 후보

### Link health workflow

link health는 fail보다 먼저 관찰 가능한 신호를 안정적으로 만드는 것이 목적입니다.
정비할 때는 아래 순서로 봅니다.

```bash
# 1. index 생성/최신성 확인
python3 .agents/skills/dnl-builder/dnl_util.py link index build
python3 .agents/skills/dnl-builder/dnl_util.py link index check

# 2. QA summary(report-only)
python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary

# 3. 상세 후보 조회
python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary
python3 .agents/skills/dnl-query/dnl_query.py unresolved --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py unused --format jsonl
python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --format jsonl
```

`unresolved`와 `missing-tokens`는 실제 경로/토큰 오류일 가능성이 높고, `unused`는 포털 문서의 의도적 예비 link일 수 있습니다.
따라서 현재 단계에서는 `--profile health`가 count를 보여주되 QA 실패로 올리지는 않습니다.
