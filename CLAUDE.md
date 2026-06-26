# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nobel Prep 학원의 콘텐츠 및 도구 모음. 퀴즈, 화학 시뮬레이션, 네이버 카페 블로그 콘텐츠로 구성.

**Deployment:** GitHub Pages — `kimsangjun-eng.github.io` (모든 HTML은 단일 파일로 자체 실행)

## Project Structure

```
Nobel-Prep/
├── Quiz/
│   ├── IB-Chem/      # IB HL Chemistry 퀴즈
│   └── AP-Chem/      # AP Chemistry 퀴즈
├── Simulation/        # 화학 개념 시각화 (HTML/JS 단일 파일)
├── Cafe/              # 네이버 카페 콘텐츠 (한국어 블로그)
└── Skills/            # 작업별 스킬/프롬프트 파일
```

## Brand

| Token | Value |
|-------|-------|
| Navy  | `#1B2A4A` |
| Gold  | `#C9A84C` |
| Teal  | `#1A7A8A` |

**Language rule:** Quiz/Simulation → 영어, Cafe 콘텐츠 → 한국어

## Quiz Rules (IB-Chem & AP-Chem 공통)

- **채점 방식:** Submit 버튼 클릭 후 일괄 채점 (실시간 채점 금지)
- **보안:** 정답은 SHA-256 해시로 저장, 평문 노출 금지
- **힌트 금지:** 모든 입력 필드 placeholder는 `"Type your answer"` 고정 — 단서 제공 금지
- **MCQ 정답 분산:** A/B/C/D 균등 분산 (특정 선지에 몰리지 않도록)
- **Pass 기준:** 70%
- **Google Sheets 연동:** 점수 및 제출 데이터 기록

## IB HL Chemistry

- **커리큘럼:** 2023 신과정 (Structure & Reactivity 체계)
- **화학식 표기:** 유니코드 직접 사용 — `H₂O`, `CO₂`, `NH₄⁺` 등 (`<sub>`, `<sup>` 태그 사용 금지)
- **파일명 규칙:** `ib-hl-chem-[topic]-quiz-[a/b].html`

## AP Chemistry

- **커리큘럼:** College Board AP Chemistry
- **파일명 규칙:** `ap-chem-[topic]-quiz-[a/b].html`

## Simulation

- HTML + JS 단일 파일로 작성 (외부 의존성 최소화)
- GitHub Pages에서 별도 서버 없이 단독 실행 가능해야 함

## Cafe 콘텐츠

- **주제:** 미국 대학 입시, SAT, GPA, AP 과목
- **대상 독자:** 학부모 및 고등학생
- **톤:** 강남 학원 원장 관점 — 전문적이고 신뢰감 있는 Nobel Prep 브랜드 톤 유지
