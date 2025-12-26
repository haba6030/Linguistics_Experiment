# Hate Speech의 인지적 처리 및 재생산 효과 연구

**학부 졸업논문 프로젝트** | 서울대학교 언어학과 | 김진일

---

## 🎯 프로젝트 개요

### 연구 주제
부정적 집단 지향 언어(Negative Group-Directed Language)가 문장 처리, 기억 encoding, 언어 재생산에 미치는 인지적 영향

### 연구 방법
- **패러다임**: Self-Paced Reading (SPR)
- **설계**: 2×2 within-subjects design
  - Factor 1: Modifier (Hate/Derogatory vs. Neutral)
  - Factor 2: Plausibility (Plausible vs. Implausible)
- **자극**: 가상 민족 "탈렌족" (fictional group)
- **측정**: Reading time, Plausibility judgment, Free recall, Manipulation check

### 주요 가설
- **H1**: Hate modifier → 더 긴 reading time (attention capture)
- **H2**: Hate → Plausibility effect 감소 (attention narrowing)
- **H3**: Hate → 중립 사실 기억 저하 + hate-consistent false alarm (biased encoding)
- **H4**: Hate → Free recall에서 부정적 표현 증가 (reproduction bias)

---

## 📂 프로젝트 구조 (재조직 완료, 2025-12-26)

```
lingThesis/
│
├── 📄 핵심 문서 (시작점) ⭐
│   ├── EXECUTIVE_SUMMARY.md        # 전체 프로젝트 요약 (읽기 시작)
│   ├── THESIS_ROADMAP.md           # 상세 연구 계획 (3단계)
│   ├── IMMEDIATE_ACTIONS.md        # 즉시 실행 항목
│   ├── QUESTIONS_FOR_PI.md         # PI 미팅 질문 목록
│   ├── ADVISOR_EMAIL_DRAFT.md      # 지도요청 메일 초안
│   ├── README.md                   # 이 파일
│   └── INDEX.md                    # 디렉토리 구조 가이드
│
├── 🧪 experiment/                  # 웹 기반 SPR 실험
│   ├── index.html                 # 본 실험
│   ├── index_pilot.html           # 파일럿
│   ├── js/                        # 실험 로직
│   │   ├── experiment.js
│   │   ├── experiment_pilot.js
│   │   └── plugins/jspsych-spr.js
│   ├── css/style.css
│   ├── server.js                  # 로컬 서버
│   ├── google-apps-script.js      # Google Sheets 연동
│   └── package.json
│
├── 📝 stimuli/                     # 자극 및 생성
│   ├── MasterSPR.csv              # 전체 자극 목록
│   ├── List1-4.csv                # Latin Square lists
│   ├── make_list.py               # 리스트 생성 스크립트
│   ├── convert_csv_to_json.py
│   └── json/                      # 웹 실험용 JSON
│       └── list1-4.json
│
├── 🔬 scripts/                     # Python 분석 코드
│   ├── analysis/                  # 주요 통계 분석
│   │   ├── Hypothesis_Check.py
│   │   ├── analyze_results.py
│   │   ├── analyze_result_1201.py
│   │   └── ...
│   ├── hypothesis_specific/       # 가설별 분석
│   │   ├── analyze_h3_memory.py
│   │   ├── analyze_h4_detailed.py
│   │   └── analyze_h3_h4_integrated.py
│   ├── visualization/             # 시각화
│   │   ├── Visualizations.py
│   │   ├── create_presentation_figures.py
│   │   └── ...
│   └── preprocessing/             # 전처리
│       ├── apply_outlier_exclusion_1201.py
│       ├── manipulation_check.py
│       └── detailed_region_analysis.py
│
├── 📊 results/                     # 분석 결과
│   ├── result_1128/               # 1차 분석 (11/28)
│   │   ├── *.png                  # 시각화
│   │   ├── *.md, *.pdf            # 보고서
│   │   └── *.csv, *.xlsx          # 데이터
│   └── result_1201/               # 최종 분석 (12/1)
│       ├── COMPLETE_ANALYSIS_REPORT.md
│       ├── H4_DETAILED_FINDINGS.pdf
│       ├── h4_presentation_plots/
│       └── outlier_comparison_plots/
│
├── 📚 documentation/               # 문서
│   ├── deployment/                # 배포 가이드
│   ├── technical/                 # 기술 문서
│   └── research/                  # 연구 문서
│
├── 🎤 presentations/               # 발표 자료
│   ├── JinilKim_TermProject.pdf   # 최종 발표
│   ├── JinilKim_TermProject.pptx
│   └── latex_sources/             # LaTeX 소스
│
├── 🖼️ images/                      # 시각 자극
│   ├── 2024Hate.jpeg
│   ├── fakenews.png
│   └── hatespeech.png
│
├── 📖 thesis/                      # 졸업논문 (작성 중)
│   ├── chapter1_introduction.md
│   ├── chapter2_literature.md
│   ├── chapter3_methods.md
│   ├── chapter4_results.md
│   └── chapter5_discussion.md
│
└── 🔧 immediate_analysis/          # 즉시 분석 (이번 주)
    ├── effect_size_calculator.py  # 효과 크기 계산
    └── [추가 스크립트 예정]
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 프로젝트 파악 (5분)
```bash
# 전체 개요 읽기
cat EXECUTIVE_SUMMARY.md

# 상세 계획 확인
cat THESIS_ROADMAP.md
```

### 2. 실험 실행 (실험 참가자용)
```bash
# 브라우저에서 실험 열기
open experiment/index.html?list=1

# 또는 로컬 서버 실행
cd experiment
npm install
node server.js
# → http://localhost:3000?list=1
```

### 3. 데이터 분석 (연구자용)
```bash
# 효과 크기 계산
cd immediate_analysis
python effect_size_calculator.py

# 주요 분석 실행
cd ../scripts/analysis
python Hypothesis_Check.py
```

### 4. PI 미팅 준비
```bash
# 질문 목록 검토
cat QUESTIONS_FOR_PI.md

# 메일 초안 확인
cat ADVISOR_EMAIL_DRAFT.md
```

---

## 📅 현재 진행 상황 (2025-12-26)

### ✅ 완료
- [x] 행동실험 데이터 수집
- [x] H1-H4 기초 분석
- [x] 학기말 발표 (Daniel 교수 피드백 수령)
- [x] 프로젝트 구조 재조직
- [x] 졸업논문 계획 수립
- [x] PI 지도요청 준비

### 🔄 진행 중 (이번 주)
- [ ] 개념적 프레이밍 문서 작성
- [ ] 효과 크기 재분석
- [ ] 문헌 조사 (RT benchmark)
- [ ] Chapter 1-2 초안
- [ ] PI 미팅 일정 조율

### ⏳ 대기 중
- [ ] PI 미팅 및 방향 결정
- [ ] 추가 데이터 수집 (필요 시)
- [ ] EEG 실험 (장기 계획)

---

## 🎓 졸업논문 타임라인

| 기간 | 단계 | 주요 작업 | 마일스톤 |
|------|------|-----------|----------|
| **12월 하순** | Phase 0 | 프로젝트 정리, PI 컨택 | ✅ 완료 |
| **1월** | Phase 1 | 즉시 개선, PI 미팅, 방향 결정 | 개념 확정, Chapter 1-2 |
| **2-3월** | Phase 2a | 추가 데이터(필요 시), Chapter 3-4 | 실험 완료 |
| **4월** | Phase 2b | 전체 분석, Chapter 5 | 분석 완료 |
| **5월** | Phase 2c | 통합 및 교정 | 논문 초안 |
| **6월** | 제출 | 최종 검토 및 제출 | 🎯 졸업 |

---

## 📊 주요 연구 결과 (예비)

### H1: Attention Capture
- **결과**: Hate modifier → +25ms (4%), Cohen's d ≈ 0.3, p ≈ .08 (marginal)
- **해석**: 부정적 수식어가 주의를 포착하는 경향, 효과 크기는 작지만 문헌과 비교 가능

### H2: Attention Narrowing
- **결과**: Plausibility effect 감소 경향 (상호작용 부분적)
- **해석**: Hate 조건에서 후속 정보 통합 저하 가능성

### H3: Biased Memory
- **결과**: 혼합적 (중립 사실 기억 저하, false alarm 증가 경향)
- **해석**: 추가 분석 필요

### H4: Reproduction Bias ⭐ 강한 효과
- **결과**: Free recall에서 부정적 표현 유의미하게 증가, p < .01
- **해석**: Hate speech 노출 → 언어 재생산 편향 명확

---

## 🔑 핵심 이슈 및 결정 사항

### 1. 개념적 프레이밍
- **이슈**: "Hate speech" vs. "Negative group-directed language"
- **현재 입장**: 용어 재검토 중, PI 의견 필요
- **문서**: `IMMEDIATE_ACTIONS.md` 섹션 1

### 2. 효과 크기
- **이슈**: d=0.3 (4% RT 증가)의 과학적 의미
- **계획**: 문헌 benchmark, power analysis
- **스크립트**: `immediate_analysis/effect_size_calculator.py`

### 3. 실험 재설계
- **옵션**:
  - A. Objectivity 차원 추가 (2×2×2)
  - B. Context 조작 추가
  - C. 현재 유지 + 참가자 증원
- **권장**: Option C (졸업 일정 고려)

---

## 💻 기술 스택

### 실험
- jsPsych 7.3.4
- HTML/CSS/JavaScript
- Node.js (로컬 서버)
- Google Apps Script (데이터 수집)

### 분석
- Python 3.x
  - pandas, numpy, scipy
  - matplotlib, seaborn
  - statsmodels (mixed-effects)
- R (선택적)
  - lme4 (mixed models)
  - lavaan (mediation)

### 문서
- Markdown
- LaTeX (발표자료)
- Microsoft Office (최종 제출용)

---

## 📖 참고 문헌 (핵심)

### 이론적 배경
1. **Ding et al. (2016)** - Negative emotional verbs and attention narrowing
2. **Kissler et al. (2006)** - Emotional word processing
3. **Kensinger et al. (2006)** - Emotional memory trade-off
4. **Schindler et al. (2023)** - Task-dependent emotion effects

### 방법론
- **Jegerski (2014)** - Self-paced reading methodology
- **Barr et al. (2013)** - Mixed-effects models
- **Luck (2014)** - ERP/EEG methods (future)

---

## 👥 연락처

**연구자**
- 김진일
- Email: haba6030@snu.ac.kr
- 전화: 010-5264-9444

**지도교수** (예정)
- [PI 이름 - 미정]

**참고 교수**
- Daniel Plesniak (ExpLing 강의, 피드백 제공)

---

## 📝 다음 단계 (이번 주)

### 우선순위 작업
1. ⭐ **개념적 프레임워크 문서 작성** (용어 정의, 이론적 위치)
2. ⭐ **효과 크기 재계산 및 문헌 비교**
3. ⭐ **PI 미팅 일정 조율 (메일 발송)**
4. 📚 문헌 조사 (10편 정독)
5. ✍️ Chapter 1-2 outline 작성

### 체크리스트
- [ ] `conceptual_framework.md` 작성
- [ ] `effect_size_calculator.py` 실행
- [ ] 문헌 benchmark table 완성
- [ ] PI에게 메일 발송
- [ ] Chapter 1 outline 작성
- [ ] 주간 진행 상황 업데이트

---

## 🆘 도움이 필요하면

### 문서 찾기
- **전체 계획 확인**: `EXECUTIVE_SUMMARY.md` 또는 `THESIS_ROADMAP.md`
- **즉시 작업**: `IMMEDIATE_ACTIONS.md`
- **PI 미팅 준비**: `QUESTIONS_FOR_PI.md`
- **디렉토리 구조**: `INDEX.md`

### 분석 실행
```bash
# 효과 크기 계산
python immediate_analysis/effect_size_calculator.py

# 주요 분석
python scripts/analysis/Hypothesis_Check.py

# 시각화
python scripts/visualization/Visualizations.py
```

### 이슈 추적
- Todo list 확인: (이 README 상단 참조)
- 진행 상황 업데이트: `THESIS_ROADMAP.md` 하단

---

## 📜 라이선스 및 윤리

### IRB
- [서울대 IRB 승인 여부 확인 필요]
- 가상 집단 사용으로 윤리적 이슈 최소화

### 데이터
- 개인정보 비식별화
- 연구 목적으로만 사용
- 졸업 후 데이터 보관/폐기 계획 수립 예정

### 코드
- 연구 목적 사용
- 출처 명시 시 재사용 가능

---

## 🎯 최종 목표

**단기 (6개월)**
- ✅ 학부 졸업논문 완성 및 제출
- ✅ 발표 및 심사 통과

**중기 (1년)**
- 🔬 EEG 실험 통합
- 📝 학술 논문 작성
- 🎤 학회 발표 (CUNY, AMLaP 등)

**장기 (2년+)**
- 📰 학술지 출판 (*Cognition and Emotion*, *Language, Cognition and Neuroscience*)
- 🎓 석사 진학 (고려 중)
- 🌍 Hate speech 인지 메커니즘 연구 확장

---

**Last Updated**: 2025-12-26
**Next Review**: After PI meeting (early January 2025)

---

Built with ❤️ for understanding how language shapes minds and societies.
