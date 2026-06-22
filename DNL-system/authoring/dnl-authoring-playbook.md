---
name: "DNL Authoring Playbook (for AI-assisted writing)"
status: "draft"
tags: ["playbook-dnl", "dnl-builder"]
paths:
  "@markdown-rule.md": "{@DNL-system}/authoring/rules/markdown-rule.md"
  "@yaml-frontmatter-rule.md": "{@DNL-system}/authoring/rules/yaml-frontmatter-rule.md"
  "@multi-dnl-authority.md": "{@DNL-system}/authoring/rules/multi-dnl-authority.md"
  "@workflow-root.md": "{@DNL-system}/workflow/README.md"
  "@future-to-dnl.md": "{@DNL-system}/workflow/future-to-dnl.md"
  "@future-to-archive.md": "{@DNL-system}/workflow/future-to-archive.md"
  "@dnl-builder-qa.py": "{@dnl-root}/.agents/skills/dnl-builder/qa.py"
  "@dnl-builder/README.md": "{@DNL-system}/authoring/README.md"
---

# DNL Authoring Playbook (for AI-assisted writing)


> 이 문서는 **DNL을 추가/수정할 때 AI에게 주는 작업 지침서**입니다.
> {@DNL-system}/authoring 포털에서만 노출하고, 필요할 때만 프롬프트로 지정해서 읽히는 용도입니다.

---

## 0) 시작 전 확인(필수)
1. 규칙: `@markdown-rule.md`
2. YAML frontmatter 규칙: `@yaml-frontmatter-rule.md`
3. 권위/override: `@multi-dnl-authority.md`
4. 작업이 `future`, `future-to-dnl`, promotion, archive, history 정리를 포함하면 workflow: `@workflow-root.md` → `@future-to-dnl.md` → 필요 시 `@future-to-archive.md`

---

## 0.5) DNL Steward Lens(총괄담당자 관점)

DNL을 쓰는 AI는 "문서 작성자"에서 멈추지 않고, 다음 AI가 맥락을 적게 읽고도 정확한 정본으로 도착하게 만드는 운영자처럼 판단한다.

### 핵심 원칙

- DNL의 핵심은 모든 맥락을 보존하는 것이지만, 모든 맥락을 한 파일에 몰아넣는 것이 아니다.
- 포털/README는 현재 결론, 문서 역할, 다음 이동 경로만 담는다.
- 긴 조사 과정, 과거 계획, 비교 근거, 세부 판단은 별도 문서로 분리하고 포털에서 `@토큰`으로 안내한다.
- `future` 문서는 현재 정본이 아니라 승격 후보와 작업 힌트다. 승격 후 active 문서가 여전히 `future`를 우선 경로로 보게 두면 안 된다.
- `future` 자료를 정본에 흡수할 때는 authoring보다 먼저 작업 수명주기 경계를 세운다. main/README에는 현재 핵심과 길찾기만 두고, 과거 변경 이력·future 경고·비교 분석은 `@future-to-dnl.md` 기준으로 분리한다.
- UI 화면 문서는 화면 구조와 의사결정, 서버 도메인 문서는 Controller/Service/Mapper/API/DDL 근거, 설계 결정 문서는 왜 그렇게 했는지를 맡는다.
- 같은 사실을 여러 곳에 단정하지 말고, source-of-truth 하나와 얇은 cross-link 여러 개로 유지한다.

### 승격/정비 완료 기준

문서를 작성하거나 `future` 내용을 현재 DNL로 승격할 때는 아래를 모두 확인한다.

1. leaf 문서가 현재 코드/화면/도메인 근거를 반영한다.
2. 상위 README가 새 문서로 라우팅한다.
3. 모듈 지도, 화면 지도, 구현 가이드 같은 집계 문서가 같은 구조를 말한다.
4. `future` 문서는 남은 작업 허브인지, archive 후보인지, 더 이상 우선 경로가 아닌지 분명하다.
5. UI 문서와 서버 도메인 문서의 책임이 분리되어 있고, 서버 상세는 서버 도메인 정본으로 연결된다.
6. YAML `paths`는 `{@변수}/...` 기반 논리 경로를 사용하고, 본문은 `@토큰` 중심으로 안내한다.
7. QA와 semantic stale 검색을 모두 통과한다.

### semantic stale 검색

QA가 문법과 링크를 잡아준다면, semantic stale 검색은 "내용은 남아 있지만 방향이 낡은 상태"를 잡는다.

대표적으로 아래를 검색한다.

- 승격 전 경로가 현재 지도에 남아 있는지
- `future 우선`, `future 기준`, `draft만 존재` 같은 예전 우선순위가 active 문서에 남아 있는지
- 완료라고 썼지만 상위 README나 지도에서 찾아갈 수 없는 문서가 있는지
- UI 문서가 서버 내부 구현을 정본처럼 길게 복제하고 있지 않은지
- 서버 도메인 문서가 없는데 화면 문서만 서버 동작을 단정하고 있지 않은지
- YAML `paths`에 `README.md`, `../`, `./` 같은 위치 의존 경로가 남아 있는지

---

## 1) 문서 작성 원칙(핵심)
- DNL 주 독자는 AI다.
- 로컬 파일/폴더를 가리키는 마크다운 링크(`[text](path)`)는 사용하지 않는다.
- DNL 정본 문서는 YAML frontmatter에 `name`, `status`, `tags`를 반드시 둔다.
- 경로는 YAML frontmatter의 `paths` map과 `@토큰`으로 안내한다.
- 새 문서나 의미 있게 수정한 문서는 YAML frontmatter `status: "draft"`를 기본으로 둔다.
- `README.md` 문서는 `tags`에 `portal-dnl`을 포함한다.
- 예외는 이미지 링크, 외부 웹 URL, 규칙 설명용 fenced code block 내부 예시만 허용한다.

---

## 2) 레이어별 작성 범위(System → Shared layer → Product → Project)
- System(DNL-system/*): DNL 작성/운영 규칙, AI 규칙, workflow, templates, boundaries
- Shared layer(`docs/sample-dnl/*` 또는 이 저장소가 실제로 쓰는 동등한 공용 계층): 공통 용어, 지도, 게이트웨이, 현황
- Product(`sample-product/README.md`): "어디로 내려가야 하는지" 라우팅
- Project(`sample-product/sample-project/README.md`): 구현/모듈/화면/코드 경로

모든 저장소가 네 층을 다 갖는 것은 아닙니다. 존재하는 레이어만 쓰고, 있는 레이어끼리만 같은 규칙을 적용합니다.

---

## 3) 작업 절차(권장)
1) 변경 범위와 레이어를 좁힌다(System → Shared layer → Product → Project)
2) 작업이 `future` 자료 흡수/promotion/archive라면 `@future-to-dnl.md` 체크리스트로 main/배경/archive 경계를 먼저 정한다
3) 대상 문서의 역할을 정한다(라우터/정본/배경/future/archive)
4) 프로그램으로 스캔한다(패턴 검색/잔재 찾기)
5) 수정한다
6) 상위 README, 지도, 가이드, cross-link가 새 정본으로 이어지는지 확인한다
7) **주변 문맥(앞/뒤 문단 흐름) 확인**
8) semantic stale을 검색한다
9) 1작업 = 1커밋
10) QA:
   - 포털 기준: `python3 .agents/skills/dnl-builder/qa.py --profile portal`

---

## 4) 프롬프트 템플릿(복붙용)
아래 블록을 그대로 AI에게 전달하면 됨.

```text
You are editing a public DNL repository.
Before writing, read:
- DNL-system/workflow/README.md
- DNL-system/workflow/future-to-dnl.md (required when promoting/absorbing future material)
- DNL-system/authoring/dnl-authoring-playbook.md
- DNL-system/authoring/rules/markdown-rule.md
- DNL-system/authoring/rules/yaml-frontmatter-rule.md
- DNL-system/authoring/rules/multi-dnl-authority.md

Rules:
- No local markdown file/folder links in authored docs.
- Every canonical DNL markdown document must include YAML frontmatter `name`, `status`, and `tags`.
- New or meaningfully edited DNL docs should use status: "draft" unless the user explicitly says otherwise.
- README.md docs must include tag: `portal-dnl`.
- Use YAML frontmatter paths + @tokens for navigation.
- Exceptions are images, external web URLs, and fenced-code rule examples only.
- Work as a DNL steward, not only as a local document editor.
- Keep routers/README files light: current truth + next navigation only.
- Split heavy background, investigation notes, and decision history into load-on-demand docs.
- For future-to-DNL work, do not place future warnings, historical name drift, or comparison analysis in the main README unless it is only a minimal route to a separate background/history document.
- After promoting future content, rewire parent README/map/guide docs so active DNL no longer treats future as the priority path.
- Separate UI screen facts, server-domain facts, and design decisions; use thin cross-links instead of duplicated assertions.
- Search semantic stale after edits: old paths, old priority wording, missing parent routing, and completion claims without navigation.
- After changes, run: python3 .agents/skills/dnl-builder/qa.py --profile portal

Task:
<write your task here>
```
