---
name: "작성 규칙"
status: "draft"
tags: ["rule-dnl", "dnl-builder"]
paths: {}
---

> This document is a writing rule for DNL authors and AI agents, not part of the DNL itself.

# 작성 규칙
- DNL의 md 파일 작성 시 모든 문법은 markdown 문법을 따릅니다.

# 네비게이션 원칙
- 디렉토리간 슬래시 표기는 `/` 사용합니다. (백슬래시 `\` 사용 금지)
- DNL의 주 독자는 AI입니다. 따라서 문서 네비게이션의 정본은 **YAML frontmatter `paths` 선언 + 심볼(@토큰) 참조**입니다.
- 사람 클릭 편의보다, 문서 이동/리팩토링 이후에도 안정적으로 추론 가능한 표기를 우선합니다.

## AI 우선 링크 표기(정본)
DNL의 주 독자는 AI입니다. 따라서 **로컬 마크다운 링크 대신, YAML `paths` 선언 + 심볼(@토큰) 참조**를 사용합니다.

### 권장 패턴(정본)
- 문서 상단 YAML frontmatter에 필요한 경로만 `paths` map으로 선언 (java import처럼)
- 본문에서는 경로를 `@토큰` 또는 `{@변수}` 기반 절대경로(논리경로)로만 표기

예시:
```md
---
name: "작성 규칙"
status: "draft"
tags: ["rule-dnl"]
paths:
  "@rule": "{@dnl-root}/docs/sample-dnl/rule/README.md"
---

규칙은 `@rule` 참고.
```

### paths 값 표기(정본)
- YAML `paths`의 값은 가능하면 **`{@변수}/...` 기반 논리 경로**로 통일합니다.
  - ✅ `{@dnl-root}/docs/sample-dnl/maps/projects-map.md`
  - ✅ `{@dnl-root}/docs/sample-dnl/sample-product/README.md`
  - ❌ `../maps/projects-map.md` (문서 위치가 바뀌면 깨지기 쉬움)
  - ❌ `/docs/sample-dnl/sample-product/README.md` (환경/뷰어에 따라 해석이 달라질 수 있음)

## 마크다운 링크 사용 정책
- 로컬 파일/폴더를 가리키는 마크다운 링크(`[text](path)`)는 **DNL 문서에서 금지**합니다.
  - 금지 범위: 본문, 부록, 목차, `HUMAN_LINKS` 같은 보조 섹션을 포함한 모든 실문서 영역
  - 이유: 링크 표기가 섞이면(상대경로/절대경로/변수경로 혼재) 저가 모델에서 혼란이 커지고, 구조 변경 시 링크가 대량으로 깨집니다.
- 허용 예외는 아래 3가지뿐입니다.
  - 이미지 링크: `![alt](assets/example.png)`
  - 외부 웹 URL: `[OpenAI](https://openai.com)`
  - 규칙 설명용 fenced code block 내부 예시

- `## HUMAN_LINKS` 섹션과 `- [HUMAN_LINK]` 라인은 더 이상 허용하지 않습니다.
- 클릭 가능한 로컬 링크가 필요하더라도, 새 예외를 만들지 말고 YAML `paths` 선언과 `@토큰`/`{@변수}` 설명을 보강합니다.

예시:
```md
---
name: "작성 규칙"
status: "draft"
tags: ["rule-dnl"]
paths:
  "@rule": "{@dnl-root}/docs/sample-dnl/rule/README.md"
---

규칙은 `@rule` 참고.
```

금지 예시:
```md
규칙은 [rule/README.md](rule/README.md) 참고.

## HUMAN_LINKS
- [HUMAN_LINK] [rule/README.md](rule/README.md)
```

> 핵심 원칙: 문서의 의미와 네비게이션은 YAML `paths`, `@토큰`, `{@변수}`로 통일하고, 로컬 파일 링크는 예외 없이 제거합니다.

## 프로젝트 기준 상대 경로 작성 방법
- 다른 문서, 소스코드에 대한 자세한 경로 파일 참조 시, 문서의 핵심 흐름을 설명하는 데 필요한 파일만 YAML frontmatter에 선언합니다. (java의 import 처럼)
md 파일 작성 예시
```markdown
---
name: "코드 설명"
status: "draft"
tags: ["guide-dnl"]
paths:
  "@sample-company.md": "{@dnl-root}/docs/sample-dnl/README.md"
  "@sample-product.md": "{@dnl-root}/docs/sample-dnl/sample-product/README.md"
  "@sample-project.md": "{@dnl-root}/docs/sample-dnl/sample-product/sample-project/README.md"
  "@sample-module.md": "{@dnl-root}/docs/sample-dnl/sample-product/sample-project/modules/sample-module/README.md"
---

# 코드 설명
- 샘플 화면에 대한 module 설명은 `@sample-module.md` 에서 확인합니다.
- 샘플 project의 구현 상세는 `@sample-project.md` 에서 확인합니다.

## 프로세스
@sample-screen.md -> @sample-module.md -> @sample-project.md

샘플 기능에 대한 자세한 설명은 `@sample-product.md` 문서를 참조하세요.
```
- @ 토큰 규칙
  @파일명 표기는 문서 상단 YAML `paths`에 선언된 항목을 참조하는 심볼로 사용한다.


# 첨부 파일
- 이미지 및 첨부 파일 경로는 `assets/` 디렉토리 안에 작성됩니다.
- assets는 작성중인 md 파일과 동일한 디렉토리 안에 작성됩니다.
- markdown 이미지 표기 시 `![이미지 설명](이미지 경로)` 사용
### 이름 규칙
- 이미지 파일 이름은 소문자 kebab-case 사용
- 이미지 설명은 이미지 파일 이름으로 작성
- 예시
  - ✅ `![샘플 작성 화면](assets/compose-main.png)`
  - ❌ `![샘플 작성 화면](assets/Compose-Main.png)`

## 파일, 폴더 명 규칙
- 소문자 kebab-case 사용
- 폴더명, 파일명 이름으로도 AI에게 파악하기 용이하도록 작명
- 예외
  - 화면이름, 소스코드 명 등은 직관적 전달을 위해 그대로 사용 가능
  - 예시
    - admin-screen/
      - 기본환경설정.md
      - 사용자관리.md
