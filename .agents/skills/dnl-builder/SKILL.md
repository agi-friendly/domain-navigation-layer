---
name: dnl-builder
description: DNL 문서 작업 시 DNL-system/authoring 정본으로 라우팅하고 QA까지 수행하는 스킬
---

# DNL Builder

이 스킬은 `.agents/skills/dnl-builder/qa.py`만 실행하는 도구가 아니라,
AI를 `DNL-system/authoring`의 정본 규칙/플레이북으로 먼저 보내는 브리지입니다.

## 기본 자세: DNL 총괄담당자

이 스킬을 쓰는 AI는 한 문서의 작성자가 아니라, DNL 전체의 탐색 품질을 책임지는 총괄담당자처럼 행동합니다.

- 현재 파일이 맞는지만 보지 말고, 상위 README/지도/가이드가 새 정본으로 이어지는지 확인합니다.
- README와 포털 문서는 현재 정본과 다음 이동 경로만 얇게 유지하고, 긴 배경/조사/판단 근거는 필요할 때 여는 보조 문서로 분리합니다.
- `future` 문서는 힌트입니다. 현재 DNL로 승격한 뒤에는 active 문서가 `future`를 우선 경로로 보지 않게 재배선합니다.
- UI 문서, 서버 도메인 문서, 설계 결정 문서의 source-of-truth를 나누고 중복 단정을 피합니다.
- QA 통과만으로 끝내지 말고, 옛 경로/옛 우선순위/상위 라우터 누락 같은 semantic stale도 검색합니다.

## 이 스킬을 먼저 써야 하는 경우

- DNL 문서를 새로 작성할 때
- DNL 문서를 수정/리팩터링할 때
- `README.md`, YAML frontmatter, `@토큰`, 로컬 파일링크/HUMAN_LINK 제거 작업을 할 때
- 작업 후 DNL 문서 품질을 점검할 때

## 필수 읽기 순서

1. `DNL-system/authoring/README.md`
2. `DNL-system/authoring/rules/markdown-rule.md`
3. `DNL-system/authoring/rules/yaml-frontmatter-rule.md`
4. `DNL-system/authoring/rules/multi-dnl-authority.md`
5. `DNL-system/authoring/dnl-authoring-playbook.md`
6. 필요한 경우 `.agents/skills/dnl-builder/README.md`

## 기본 작업 순서

1. 정본 규칙 문서를 읽고 변경 범위와 레이어를 좁힙니다.
2. 대상 문서의 역할을 정합니다: 라우터, 정본, 배경, future, archive.
3. 대상 DNL 문서를 수정합니다.
4. 상위 README, 관련 지도/가이드, cross-link가 새 정본을 가리키는지 확인합니다.
5. 주변 문맥과 semantic stale을 다시 확인합니다.
6. QA를 실행합니다.

## QA 실행 (자주 쓰는 것만)

> **Windows:** `python -X utf8 .agents/skills/dnl-builder/qa.py ...`
> **macOS/Linux:** `python3 .agents/skills/dnl-builder/qa.py ...`

```bash
# 전체 스캔
python3 .agents/skills/dnl-builder/qa.py

# 포털(회사+제품+핵심 프로젝트)만
python3 .agents/skills/dnl-builder/qa.py --profile portal --fail-on all
```

리포트: `.agents/skills/dnl-builder/reports/qa-report.md` (gitignored)

## 상세 문서

- 작업 절차, 체크 항목, 실패 정책: `.agents/skills/dnl-builder/README.md`
- 정본 작성 규칙과 플레이북: `DNL-system/authoring/`
