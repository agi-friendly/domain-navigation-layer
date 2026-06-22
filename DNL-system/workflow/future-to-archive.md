---
name: "future -> archive 이동 가이드"
status: "draft"
tags: ["guide-dnl", "workflow-dnl"]
description:
  - "이 문서는 future 작업 묶음을 active 경로에서 분리해 raw archive로 옮기는 기준을 설명한다."
  - "DNL promotion과 참조 재배선이 끝난 뒤 archive 가능 여부를 판단할 때 사용한다."
paths:
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@concepts.md": "{@DNL-system}/workflow/concepts.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
  "@repo-history-guide.md": "{@dnl-root}/.repo-history/GUIDE.md"
---

# future -> archive 이동 가이드

이 문서는 `future` 작업 묶음을 raw archive로 이동할 때의 기준을 정리한다.

---

## archive 이동의 목적

- active 문서와 과거 작업 묶음을 분리한다
- AI 기본 탐색에서 raw bundle 노이즈를 줄인다
- 당시의 판단 재료는 보존하되, 현재 정본과 섞이지 않게 한다

---

## 언제 archive로 이동하나

아래 조건을 모두 만족하는 경우를 기본으로 본다.

1. 필요한 정본 내용이 DNL에 승격되었다
2. 현재 active 문서가 더 이상 해당 `future` 경로를 정본으로 참조하지 않는다
3. 작업이 현재 진행 중 상태가 아니다
4. raw bundle은 보존 가치가 있지만 기본 탐색에 둘 필요는 없다

---

## 아직 archive로 보내면 안 되는 경우

- 프로젝트 DNL이 아직 `future`를 현재 기준 문서로 보고 있다
- 작업이 아직 active다
- 승격할 문서가 아직 정리되지 않았다
- 다음 AI가 계속 이 묶음을 시작점으로 읽어야 한다

---

## archive 이동 후 원칙

- archive는 참고용이다
- active 포털에서 기본 시작점으로 링크하지 않는다
- archive가 현재 정본이라는 표현을 쓰지 않는다
- 필요하면 사건 요약 문서를 별도 history 공간에 남긴다

---

## 권장 경로 패턴

raw bundle archive는 아래처럼 날짜와 주제로 나누는 방향을 기본으로 본다.

```text
.workflow-archive/
  sample-product/
    2026/
      03/
        22/
          insight/
            code-rule/
```

이 구조의 목적은
- 어떤 시기의 작업인지 보이게 하고
- 원래 주제 단위를 유지하며
- active product 문서군과 시각적으로 분리하는 데 있다.

현재 이 저장소에서는 이 보관소를 `{@dnl-root}/.workflow-archive` 경로로 둔다.

---

## `.repo-history`와의 차이

archive는 원본 작업 묶음을 보관하는 곳이다.

반면 `.repo-history`에는 아래만 남긴다.

- 왜 이 구조를 만들었는가
- 어떤 운영 변화가 있었는가
- 지금 관점에서 남는 의미가 무엇인가

즉:
- raw bundle -> archive
- 사건의 맥락 요약 -> history

---

## 이동 체크리스트

- DNL 정본이 이미 만들어졌는가
- active 문서의 참조 기준이 바뀌었는가
- archive라는 성격이 문서 설명에서 분명한가
- active 포털에서 직접 링크하지 않는가
- 사건 의미를 history로 따로 남길지 판단했는가

---

## 실무 원칙

- 기본은 copy보다 move를 선호한다
  - WHY: active와 archive 두 군데가 동시에 정본처럼 남지 않게 하기 위해서다.
- 다만 이동 전에 참조 관계를 먼저 정리한다
  - WHY: archive 이동 후에도 active DNL이 옛 경로를 가리키면 탐색이 깨지기 때문이다.

---

## 한 줄 결론

> archive 이동은 "옛 문서를 치우는 일"이 아니라,
> **active 문서군에서 raw bundle을 분리해 탐색 품질을 지키는 일**이다.
