---
name: "DNL authoring - DNL 작성/정비 포털"
status: "draft"
tags: ["portal-dnl"]
paths:
  "@dnl-authoring-playbook.md": "{@DNL-system}/authoring/dnl-authoring-playbook.md"
  "@rules/README.md": "{@DNL-system}/authoring/rules/README.md"
  "@rules/markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@rules/yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@rules/multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@dnl-config.toml": "{@dnl-root}/dnl-config.toml"
  "@qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-util.py": "{@dnl-root}/.agents/skills/dnl-builder/dnl_util.py"
---

# DNL authoring - DNL 작성/정비 포털


> 이 디렉토리는 **DNL을 작성/정비하는 사람/AI**를 위한 전역 규칙 포털입니다.
> “DNL을 어떻게 탐색/활용해서 답변할지”는 {@DNL-system}/ai 문서를 따릅니다.

---

## 추천 읽기 순서
1) 작성 규칙(필수): `@rules/README.md` → `@rules/markdown-rule.md` → `@rules/yaml-frontmatter-rule.md`
2) 권위/override(필수): `@rules/multi-dnl-authority.md`
3) 실제 작업 절차: `@dnl-authoring-playbook.md`

---

## 총괄담당자 관점

`dnl-builder` 스킬을 사용하는 AI는 "지금 이 파일을 예쁘게 고치는 사람"이 아니라, DNL 전체를 앞으로 운영할 총괄담당자 관점으로 움직입니다.

DNL의 핵심 가치는 모든 맥락을 보존하되, 한 번에 전부 읽지 않아도 되는 길을 만드는 것입니다. 그래서 좋은 문서는 긴 문서가 아니라, 현재 정본과 다음 이동 경로가 선명한 문서입니다. 내용이 커질수록 README에 더 많이 쌓지 말고, 포털은 얇게 유지한 채 배경·조사·결정 근거를 load-on-demand 문서로 분리합니다.

문서 하나를 승격하거나 정리했다면 그 파일만 보지 않습니다. 상위 README, 화면 지도, 구현 가이드, future 허브, 관련 서버 도메인 문서까지 따라가며 "다음 AI가 어디서 시작해도 현재 정본으로 도착하는가"를 확인합니다. 이 연결이 끊기면 내용이 맞아도 DNL 작업은 아직 끝난 것이 아닙니다.

---

## 작업 루틴(권장)
1) 변경 범위와 레이어 확정(Shared layer → Product → Project, 있는 레이어만)
2) 대상 문서 역할 확정(라우터/정본/배경/future/archive)
3) 문서 수정(규칙 준수: YAML `paths`/@토큰 중심, 로컬 파일링크/HUMAN_LINK 금지)
4) 라우터 재배선(상위 README/지도/가이드/cross-link가 새 정본을 가리키는지 확인)
5) semantic stale 검색(옛 경로, 옛 우선순위, future 잔재, 완료 주장과 라우팅 불일치)
6) QA 실행:
   - 포털 기준: `python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all`
   - 전체 기준: `python3 .agents/skills/dnl-builder/qa.py --profile full --fail-on all`
   - link-index health summary: `python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary`
7) 1작업 = 1커밋

## dnl-config.toml 경계

`@dnl-config.toml`은 DNL 도구가 공유하는 프로젝트 지도입니다.
`qa.py --profile full`과 tag index는 여기의 `scan.include`, `scan.exclude`, `tags.required_by_filename`, `tags.required_by_path`를 읽습니다.

반대로 DNL 자체의 정책은 config로 열지 않습니다.
YAML 필수 필드, field order, status 허용값, tag/token 문자 규칙, 숨김 디렉토리와 `SKILL.md` 제외 규칙은 코드 상수와 `@rules/yaml-frontmatter-rule.md`가 기준입니다.

## 유틸리티

- `@dnl-util.py`: DNL 문서 대량 정비용 유틸리티 진입점
- 태그 추가 dry-run:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs/sample-dnl/sample-module --tag sample-module --recursive`
- 태그 추가 write:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag add --dir docs/sample-dnl/sample-module --tag sample-module --recursive --write`
- 태그 인덱스 전체 재생성:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index build`
- 태그 인덱스 최신성 확인:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index check`
- link index 전체 재생성:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index build`
- link index 최신성 확인:
  - `python3 .agents/skills/dnl-builder/dnl_util.py link index check`
- 태그 인덱스 파일 1개 갱신:
  - `python3 .agents/skills/dnl-builder/dnl_util.py tag index update --path docs/sample-dnl/sample-module/README.md`

## Link health 점검 루틴

link health는 DNL을 바로 실패시키는 gate가 아니라, `paths` 연결 상태를 먼저 관찰하는 report-only 루틴입니다.

1. link index를 갱신합니다.
   - `python3 .agents/skills/dnl-builder/dnl_util.py link index build`
2. index 최신성을 확인합니다.
   - `python3 .agents/skills/dnl-builder/dnl_util.py link index check`
3. QA summary로 전체 수치를 봅니다.
   - `python3 .agents/skills/dnl-builder/qa.py --profile health --json-summary`
4. 문제가 많은 영역을 좁힙니다.
   - `python3 .agents/skills/dnl-query/dnl_query.py unresolved-summary`
5. 상세 후보를 확인합니다.
   - `python3 .agents/skills/dnl-query/dnl_query.py unresolved --format jsonl`
   - `python3 .agents/skills/dnl-query/dnl_query.py unused --format jsonl`
   - `python3 .agents/skills/dnl-query/dnl_query.py missing-tokens --format jsonl`

현재 기준으로는 `unresolved`, `unused`, `missing-tokens` 모두 health signal입니다.
정책이 안정되기 전까지는 report를 보고 사람이 정리 대상을 고르는 흐름을 우선합니다.
