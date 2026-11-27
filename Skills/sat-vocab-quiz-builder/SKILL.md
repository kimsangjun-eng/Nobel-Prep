---
name: sat-vocab-quiz-builder
description: SAT Reading & Writing 모의고사 PDF를 받아 500점대 학생용 단어 리스트 PDF + 자동채점 HTML 퀴즈(A/B)를 만들고 GitHub·Notion까지 자동 반영하는 Nobel Prep 전용 파이프라인. 새 Mock Test PDF가 업로드되면 질문 없이 바로 이 절차를 시작한다.
---

# SAT 단어 리스트 + 자동채점 퀴즈 제작 (Nobel Prep)

## 트리거 조건

- 사용자가 SAT Reading & Writing 모의고사(Mock Test) PDF를 업로드하면, **추가 지시 없이 즉시 아래 8단계를 전부 수행한다.** ("앞으로 파일 추가하면 작업 시작해라" — 확정된 standing instruction)
- 질문은 하지 않는다. 다만 Mock Test 번호가 파일명과 본문 내용이 서로 다르게 보이면, **반드시 PDF 본문에 적힌 번호·출처(Source)를 기준으로 삼는다** (파일명은 신뢰하지 않는다).

## 전체 워크플로우 (8단계, 순서 고정)

### 1. 텍스트 추출
```bash
mkdir -p vocab{N}
pdftotext -layout "<업로드된 PDF 경로>" vocab{N}/mt{N}.txt
```
`cat -n`으로 전체를 끝까지 읽는다 (Module 1 + Module 2, 지문·선택지·전환어 문제 포함 전부). 일부만 보고 단어를 뽑으면 안 된다.

### 2. 단어 큐레이션 (핵심 — 판단이 필요한 단계, 생략/자동화 불가)
- 기준: **500점대 한국 학생이 모를 수 있다고 생각되는 단어는 무조건 전부 포함한다. 개수 제한(cap)을 절대 걸지 않는다.** ("단어 갯수 고정 하지 말고 500점 정도의 학생들이 모를수 있다고 생각하는 단어는 무조건 넣으세요" — 확정 규칙)
- 지문에 등장한 순서대로, 본문에 나온 형태(원형이 아니어도 됨 — 예: "diverging", "attributable")를 그대로 표제어로 쓴다.
- 중복 단어 절대 금지 (최종 JSON 작성 후 반드시 Python으로 dedup 검증).
- 각 단어마다 다음 4개 필드로 JSON 배열을 만든다:
  ```json
  {"word": "nonperishable", "edef": "영어 정의 (English definition, 쉬운 영어로)", "kdef": "한글 뜻 1, 한글 뜻 2", "ensyn": "영어 동의어 1, 영어 동의어 2"}
  ```
  - `kdef`/`ensyn`은 **콤마로 구분된 복수 표현**을 넣어야 한다 (퀴즈 정답 인정 범위를 넓히기 위함 — 아래 5단계 참고).
- 저장 파일명: `vocab{N}/merged_words_mt{N}.json`
- 저장 후 바로 아래로 검증:
  ```python
  import json
  w = json.load(open("merged_words_mt{N}.json"))
  words = [x["word"] for x in w]
  assert len(set(words)) == len(words), "중복 단어 존재"
  print(len(w))
  ```

### 3. 퀴즈 데이터 생성 (결정론적 — 템플릿 그대로 사용)
`templates/gen_data.py`를 `vocab{N}/`로 복사 후:
- `__JSON_FILE__` → `merged_words_mt{N}.json` 로 치환
- 실행: `python3 gen_data.py`
- 동작 방식: 큐레이션된 단어 중 **앞에서부터 60개만** 퀴즈에 사용(원서 등장 순서 기준), 짝/홀 번호로 Quiz A(30문항)/Quiz B(30문항)로 반씩 나눔 — **겹치는 단어 없음**. 60개를 넘는 단어는 단어 리스트 PDF에만 들어가고 퀴즈에는 안 들어감 (정상 동작).
- 정답은 SHA-256 해시로만 저장 (평문 노출 금지). `kdef`/`ensyn`의 콤마 구분 항목을 각각 해시해서 한국어든 영어든 여러 표현을 정답으로 인정.

### 4. 퀴즈 HTML 생성
`templates/gen_quiz.py`를 `vocab{N}/`로 복사 후:
- `MOCK_NUM = "__MOCK_NUM__"` → `MOCK_NUM = "{N}"` 로 치환
- 실행: `python3 gen_quiz.py A` 그리고 `python3 gen_quiz.py B`
- 고정 사양 (변경 금지):
  - Navy(#1B2A4A)/Gold(#C9A84C) 브랜드, Inter/JetBrains Mono 폰트
  - Submit 버튼 클릭 후 일괄 채점 (실시간 채점 금지)
  - 모든 입력 필드 placeholder는 `"Type your answer"` 고정 (힌트 제공 금지)
  - Pass 기준 70%가 아니라 **80% (24/30)** — 이 스킬 한정 규칙 (학원 퀴즈 공통 규칙 70%와 다름, 혼동 금지)
  - `QUIZ_ID = "{N}A"` / `"{N}B"` 형식으로 기존 Google Sheets/Apps Script 웹앱(Mock Test 41부터 재사용 중인 것)에 결과 전송 — **새 Google 연동을 만들지 않는다.**
- JS 문법 검증 필수:
  ```bash
  python3 -c "
  import re
  html = open('vocab_quiz_a.html', encoding='utf-8').read()
  m = re.search(r'<script>(.*)</script>', html, re.S)
  open('/tmp/_extract.js','w',encoding='utf-8').write(m.group(1))
  "
  node --check /tmp/_extract.js
  ```
  (A, B 둘 다 검증. 에러 나면 수정 후 재검증 — 검증 없이 다음 단계로 넘어가지 않는다.)

### 5. 단어 리스트 PDF 생성
`templates/build_vocab_pdf.py`, `templates/render_pdf.py`를 `vocab{N}/`로 복사 후:
- `build_vocab_pdf.py`: `__MOCK_NUM__` → `{N}`, `__SOURCE__` → PDF에 적힌 출처(예: "College Board Official Question Bank"), `__JSON_FILE__` → `merged_words_mt{N}.json`
- `render_pdf.py`: `__MOCK_NUM__` → `{N}`
- 실행:
  ```bash
  python3 build_vocab_pdf.py
  python3 render_pdf.py
  ```
- 산출물: `Mock_Test_{N}_RW_Vocab_List.pdf` (전체 큐레이션 단어 — 60개 제한 없음)

### 6. 검수 (스스로 먼저 확인 — 생략 금지)
원장님 preference: "파일 생성 시 보여주기 전에 텍스트 추출·좌표 확인 등으로 스스로 먼저 검증한 뒤 전달".
```bash
pdftoppm -jpeg -r 100 Mock_Test_{N}_RW_Vocab_List.pdf page
```
- **최소한 1페이지(표지/헤더)와 마지막 페이지(끝까지 단어가 깨지지 않고 표/푸터가 제대로 닫혔는지)를 Read 도구로 직접 열어서 눈으로 확인한다.**
- 확인 항목: Mock Test 번호 일치, 단어 수 표기 일치, 한글/영어 깨짐 없음, 표 마지막 행과 footer 정상 종료.

### 7. GitHub 배포
```bash
cp vocab{N}/vocab_quiz_a.html sat-platform/vocab-quiz/mock-test-{N}-vocab-quiz-a.html
cp vocab{N}/vocab_quiz_b.html sat-platform/vocab-quiz/mock-test-{N}-vocab-quiz-b.html
git add sat-platform/vocab-quiz/mock-test-{N}-vocab-quiz-a.html sat-platform/vocab-quiz/mock-test-{N}-vocab-quiz-b.html
git commit -m "Add Mock Test {N} SAT vocab quiz A/B

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
git push origin main
```
- 레포: `kimsangjun-eng/Nobel-Prep` (구 URL `kimsangjun-eng/nobel-prep`로 push해도 자동 redirect됨 — 문제 아님)
- 경로는 **반드시 `sat-platform/vocab-quiz/` 폴더 안** (루트 금지).
- 학생용 온라인 링크 형식: `https://nobel-prep.vercel.app/vocab-quiz/mock-test-{N}-vocab-quiz-{a/b}.html`

### 8. Notion 업데이트 + 전달
- Notion 페이지 「SAT 온라인 퀴즈/자료 링크 모음」(id: `42359666-9571-81e9-8ca4-c09ed4db5912`)에 `insert_content`, position `{"type":"end"}`로 아래 형식 추가:
  ```
  ## Mock Test {N} (<출처>)
  - 단어 리스트: <개수>개 (500점대 학생 기준, 개수 제한 없음)
  - Quiz A: https://nobel-prep.vercel.app/vocab-quiz/mock-test-{N}-vocab-quiz-a.html
  - Quiz B: https://nobel-prep.vercel.app/vocab-quiz/mock-test-{N}-vocab-quiz-b.html
  ```
- `SendUserFile`로 3개 파일 전달: 단어 리스트 PDF, Quiz A HTML, Quiz B HTML
- 마지막 채팅 응답은 **한 줄 요약 + 산출물/링크/완료작업** 3블록 구조로, 과정 설명 없이 결과만 간결하게 보고.

## 절대 하지 말아야 할 것

- ❌ 단어 개수에 임의의 상한(cap)을 두는 것 — "60개만", "150개 정도만" 같은 자체 판단 금지. 지문에서 500점대 학생이 모를 만한 단어는 전부 포함.
- ❌ 지문 일부만 읽고 단어를 뽑는 것 — Module 1/2 전체, 모든 문제 유형(어휘완성/주제파악/전환어/노트통합 등) 포함해서 끝까지 읽기.
- ❌ 실시간 채점, placeholder에 힌트성 문구 넣기, 정답 평문 저장 — 전부 금지.
- ❌ 새 Google Sheets/Apps Script 웹앱을 새로 만드는 것 — 기존 것을 QUIZ_ID로만 구분해서 재사용.
- ❌ JS 문법 검증(`node --check`) 생략.
- ❌ PDF 생성 후 검수(rasterize + 육안 확인) 없이 바로 전달.
- ❌ `sat-platform/vocab-quiz/` 외의 경로에 커밋.
- ❌ 중복 단어가 있는 JSON을 그대로 사용 (항상 dedup 검증).

## 완료 판정 기준 (체크리스트)

- [ ] Module 1 + 2 전체 텍스트 추출·정독 완료
- [ ] 단어 JSON: 개수 제한 없이 큐레이션 + 중복 없음 검증 완료
- [ ] Quiz A/B 각 30문항, 겹치는 단어 없음, Pass 80%(24/30)
- [ ] Quiz A/B 둘 다 `node --check` 통과
- [ ] 단어 리스트 PDF: 전체 페이지 중 최소 첫 페이지·마지막 페이지 육안 검수 완료
- [ ] `sat-platform/vocab-quiz/`에 커밋·푸시 완료
- [ ] Notion 링크 모음 페이지 업데이트 완료
- [ ] 산출물 3종(PDF, Quiz A, Quiz B) 사용자 전달 완료

## 재사용 템플릿

`templates/` 폴더에 4개 스크립트가 있다. 새 Mock Test마다 이 템플릿들을 작업 폴더로 복사한 뒤, 위 단계별 안내대로 `__MOCK_NUM__` / `__SOURCE__` / `__JSON_FILE__` 플레이스홀더만 치환해서 쓴다. CSS·레이아웃·채점 로직 등 다른 부분은 손대지 않는다(확정 사양).

| 파일 | 역할 |
|---|---|
| `templates/gen_data.py` | 큐레이션 JSON → Quiz A/B용 해시 데이터(JSON) 생성 |
| `templates/gen_quiz.py` | 해시 데이터 → 자동채점 HTML 퀴즈(A, B 각각) 생성 |
| `templates/build_vocab_pdf.py` | 큐레이션 JSON → 단어 리스트 PDF용 HTML 생성 |
| `templates/render_pdf.py` | 위 HTML → PDF 렌더링 (Playwright) |
