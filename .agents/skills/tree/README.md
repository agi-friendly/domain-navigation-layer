---
name: "DNL Tree Generator — 상세 문서"
status: "draft"
tags: ["portal-dnl"]
paths: {}
---

# DNL Tree Generator — 상세 문서

`.agents/skills/tree/tree.py`는 DNL 탐색용 트리 생성 도구입니다.
Windows/macOS/Linux에서 동일하게 동작하며, `.gitignore`를 반영한 경량 트리/JSON 출력을 제공합니다.

## 설치

Python 3.10+ 권장. 최초 1회 의존성 설치.

**권장 (로컬 설치):**

```bash
# macOS/Linux
python3 -m pip install --upgrade --target .agents/skills/tree/.vendor -r .agents/skills/tree/requirements.txt

# Windows
python -m pip install --upgrade --target .agents/skills/tree/.vendor -r .agents/skills/tree/requirements.txt
```

`tree.py`는 실행 시 `.vendor`를 자동 로딩하므로 별도 활성화 없이 동작합니다.

**전역 설치(선택):**

```bash
python3 -m pip install -r .agents/skills/tree/requirements.txt
```

`pathspec`이 없으면 fallback 매칭으로 동작하므로, `.gitignore` 정확도가 중요하면 설치를 권장합니다.

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--root PATH` | `.` | 탐색 시작 경로 |
| `--files` | `False` | 파일까지 포함 |
| `--depth N` | `5` | 최대 깊이 (`-1` 무제한) |
| `--hidden` | `False` | 숨김 파일/폴더 포함 |
| `--ignore PATTERN` | 반복 가능 | 추가 제외 패턴 |
| `--no-gitignore` | `False` | `.gitignore` 기반 제외 비활성화 |
| `--no-readme-title` | `False` | README H1 추출 비활성화 |
| `--json` | `False` | JSON 모드 출력 |
| `--ascii` | `False` | 트리 라인을 ASCII로 강제 |
| `--absolute-path` | `False` | 절대 경로 출력 |
| `--out FILE` | 없음 | UTF-8 파일로 저장 |

## 출력 예시 (텍스트)

```text
domain-navigation-layer/ [3 dirs, 0 files]
├── docs/ [0 dirs, 4 files]
│   ├── README.md [23 lines] # public landing page
│   └── core-concept.md [17 lines]
├── DNL-system/ [1 dirs, 0 files]
│   └── authoring/ [1 dirs, 2 files]
└── .agents/skills/ [1 dirs, 0 files]
    └── tree/ [0 dirs, 4 files]
```

## 출력 예시 (JSON)

```json
{
  "name": "domain-navigation-layer",
  "path": ".",
  "type": "dir",
  "children": [
    {
      "name": "README.md",
      "path": "README.md",
      "type": "file",
      "readme_title": "Domain Navigation Layer",
      "lines": 23,
      "size": 1024,
      "children": []
    }
  ],
  "num_dirs": 0,
  "num_files": 1
}
```

## DNL 활용 팁

트리 결과를 프롬프트에 함께 제공하면 AI가 필요한 문서만 빠르게 라우팅할 수 있습니다.

```bash
python3 .agents/skills/tree/tree.py --root docs --files --depth 3 > dnl-tree.txt
# Paste the tree into the prompt when you want the agent to pick the relevant docs quickly.
```

## 스모크 테스트

```bash
python3 .agents/skills/tree/test_tree.py
```

## Windows 인코딩 상세

PowerShell 기본 인코딩이 cp949일 때 한글/이모지 포함 트리 출력 시 에러 발생:

```text
UnicodeEncodeError: 'cp949' codec can't encode character ...
```

**권장:** `-X utf8` 플래그로 실행

```powershell
python -X utf8 .agents/skills/tree/tree.py --root docs --files --depth 3 --ascii
```

**세션 단위 대안:**

```powershell
$env:PYTHONUTF8 = "1"
python .agents/skills/tree/tree.py --root docs --files --depth 3 --ascii
```

**`Get-Content`도 깨지는 경우:**

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Raw -Encoding UTF8 "path\to\file"
```
