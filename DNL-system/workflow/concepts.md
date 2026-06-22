---
name: "workflow 개념 정리"
status: "draft"
tags: ["reference-dnl", "workflow-dnl"]
description:
  - "이 문서는 future, DNL, archive, history의 의미와 경계를 짧게 정의한다."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@future-authoring-rule.md": "{@DNL-system}/workflow/future-authoring-rule.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
  "@future-to-archive.md": "{@DNL-system}/workflow/future-to-archive.md"
  "@repo-history-guide.md": "{@dnl-root}/.repo-history/GUIDE.md"
---

# workflow 개념 정리

이 문서는 이 저장소의 workflow에서 쓰는 주요 개념을 짧게 고정한다.

---

## `future`

- 현재 진행 중인 작업 허브
- 사용자와 AI가 같이 읽고 쓰는 active 공간
- 설계 초안, 대화 정리, TODO, 비교 분석, 작업 가이드를 계속 누적할 수 있다
- 무엇을 어떻게 남길지는 `@future-authoring-rule.md`를 따른다
- 특정 작업에서는 `future` 문서가 현재 기준 정본일 수 있다

요약:
- **active work area**

---

## `DNL`

- 반복 재사용 가치가 있는 지식의 정본
- 용어, 포털, 규칙, 지도, 가이드, 플레이북을 담는 공간
- 개별 작업 맥락보다 더 오래 유지해야 하는 기준을 둔다

요약:
- **promoted knowledge**

---

## `archive`

- active 상태를 마친 raw 작업 묶음을 보관하는 공간
- 현재 작업의 기본 시작점으로 쓰지 않는다
- 필요할 때만 참고한다

중요:
- archive는 "과거 작업 원본"의 의미다
- 사건/판단을 정리한 history와는 다르다

요약:
- **archived raw bundle**

---

## `history`

- 사건, 판단, 철학 변화, 의사결정 맥락을 정리한 문서
- 원본 자료 전체를 보관하는 폴더가 아니라, 의미를 요약하는 기록이다

예:
- `DNL-system/workflow/README.md`처럼 history 운영 방식을 설명하는 문서
- `.repo-history/GUIDE.md`처럼 repository-level history 규칙을 설명하는 문서

요약:
- **interpreted history**

---

## `.repo-history`

- 이 저장소 자체의 운영/구조/협업 방식 변화 기록
- Company / Product / Project DNL이 아니다
- 기본 DNL 라우팅 대상이 아니다

여기에 남길 것:
- `workflow` 개념 도입
- 폴더 구조 개편 이유
- 대형 문서 정리 캠페인의 운영 노하우

여기에 남기지 않을 것:
- 화면별 raw 작업 묶음
- 특정 기능 설계 폴더 전체

---

---

## 이름 선택 원칙

- raw bundle 보관소에는 `history`보다 `archive`를 우선 사용한다
- `history`는 사건/판단/철학 정리에 제한적으로 사용한다
- 같은 단어가 코드 이름, 화면 이름, 보관 의미를 동시에 가지지 않게 한다

---

## 판단 기준 한 줄 요약

- 지금 계속 작업 중인가
  - `future`
- 반복 재사용 가능한 기준인가
  - `DNL`
- 원본 묶음을 참고용으로만 남길 것인가
  - `archive`
- 사건의 의미와 맥락을 남기려는가
  - `history`
