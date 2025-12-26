# 졸업논문 연구 로드맵: Hate Speech의 인지적 처리 및 재생산 효과

**연구자**: 김진일
**목표**: 학부 졸업논문 (2025년 하반기 완성)
**장기 목표**: EEG 통합 연구 → 출판 가능 논문

---

## Executive Summary

### 현재 상태 (2025년 12월)
- ✅ 행동실험 1차 완료 (SPR + Plausibility + Free Recall + Manipulation Check)
- ✅ 데이터 수집 완료 (N=참가자 수 확인 필요)
- ✅ 기초 분석 완료 (H1-H4 검증)
- ⚠️ **Daniel 교수 피드백 반영 필요**

### 주요 피드백 이슈
1. **Hate speech 정의 불명확** → 조작적 정의 또는 재프레이밍 필요
2. **RT 효과 크기(~4%) 해석** → 과학적 의미 검증 필요
3. **맥락(context) 부재** → 가상 집단에서 hate speech 판단 근거 약함
4. **프레젠테이션 개선** → 과제 예시 및 결과 상세화

---

## Phase 1: 즉시 개선 (1-2주, 현재 → 2025년 1월 중순)

### 🎯 목표: Daniel 교수 피드백 반영 + 현재 데이터 최대 활용

### Todo List

#### A. 개념적/이론적 정리 [우선순위: 최고]

- [ ] **1.1 문헌 조사: Hate Speech 정의**
  - [ ] 선행연구 10편 이상 검토 (언어학, 심리학, 법학)
  - [ ] 조작적 정의 작성: "본 연구에서 hate speech란..."
  - [ ] 대안적 프레이밍 검토: "Emotional speech", "Negative group-directed language"
  - [ ] 결정: Hate speech 유지 vs. 용어 변경
  - **담당**: 본인
  - **기한**: 1월 5일
  - **산출물**: `literature_review_hate_speech_definition.md`

- [ ] **1.2 용어 및 개념 재정의 문서 작성**
  - [ ] Hate speech vs. Emotional speech vs. Negative speech 구분
  - [ ] 본 연구 stimuli의 특성 분석:
    - Negativity (부정성)
    - Subjectivity (주관성)
    - Emotionality (감정성)
    - Group-directedness (집단 대상성)
  - [ ] Manipulation check 데이터와 용어 정합성 검토
  - **기한**: 1월 7일
  - **산출물**: `conceptual_framework.md`

#### B. 효과 크기 분석 및 벤치마킹 [우선순위: 높음]

- [ ] **1.3 기존 데이터 효과 크기 재계산**
  - [ ] Cohen's d 계산 (Hate vs. Neutral at each region)
  - [ ] Partial η² 계산
  - [ ] 95% CI 추가
  - [ ] Region별 효과 크기 비교 테이블 작성
  - **기한**: 1월 6일
  - **산출물**: `effect_size_analysis.xlsx`, Python script

- [ ] **1.4 문헌 기반 RT effect size 벤치마크 조사**
  - [ ] Emotional word processing:
    - Kissler et al. (2006): 감정 단어 RT 차이
    - Schindler et al. (2023): 과제별 RT 차이
  - [ ] Semantic processing:
    - Ding et al. (2016): Negative emotion verb RT
    - 기타 N400 관련 행동 연구
  - [ ] 비교 테이블 작성:
    | Study | Effect | RT difference | Effect size | Our study |
    |-------|--------|---------------|-------------|-----------|
  - **기한**: 1월 8일
  - **산출물**: `rt_effect_benchmark.md`

- [ ] **1.5 효과 크기 해석 섹션 작성**
  - [ ] 4% RT 증가의 의미 논의
  - [ ] 문헌과 비교한 상대적 크기
  - [ ] Statistical significance vs. Scientific significance
  - [ ] Power analysis: 더 많은 참가자 필요 여부
  - **기한**: 1월 10일
  - **산출물**: 논문 Discussion 섹션 초안

#### C. 추가 분석 (현재 데이터 활용) [우선순위: 중간]

- [ ] **1.6 Mediation Analysis 실시**
  - [ ] 경로: RT (modifier) → Plausibility judgment → Free recall negativity
  - [ ] lavaan (R) 또는 PROCESS macro 사용
  - [ ] Bootstrap 95% CI 계산
  - [ ] Visualization: mediation diagram
  - **기한**: 1월 12일
  - **산출물**: `mediation_analysis.Rmd`

- [ ] **1.7 Individual Differences 탐색적 분석**
  - [ ] Manipulation check 개인차 → RT/judgment 상관
  - [ ] Free recall negativity 극단 집단 비교
  - [ ] 탐색적 결과만 보고 (조심스럽게)
  - **기한**: 1월 13일

- [ ] **1.8 Region-by-region 상세 분석**
  - [ ] 각 region별 Hate × Plausibility interaction
  - [ ] Spillover effect 시각화 개선
  - [ ] Timeline: modifier → critical noun → spillover 1 → spillover 2
  - **기한**: 1월 14일
  - **산출물**: 개선된 RT line graph

#### D. 발표자료 및 문서 개선 [우선순위: 중간]

- [ ] **1.9 프레젠테이션 슬라이드 개선**
  - [ ] Plausibility judgment 과제 예시 추가 (실제 화면 캡처)
  - [ ] Free recall 응답 예시 3-4개 추가 (실제 데이터)
  - [ ] Manipulation check modifier 전체 목록 백업 슬라이드
  - [ ] 결과 섹션 확장: 각 hypothesis별 상세 설명
  - [ ] 효과 크기 및 문헌 비교 슬라이드 추가
  - **기한**: 1월 15일
  - **산출물**: `JinilKim_TermProject_v2.pptx`

- [ ] **1.10 Methods 섹션 상세화**
  - [ ] 모든 과제 절차 step-by-step 기술
  - [ ] Stimuli 예시 확장 (현재 4개 → 8개 이상)
  - [ ] Region 정의 명확화
  - [ ] 데이터 전처리 절차 상세 기술
  - **기한**: 1월 16일

#### E. 졸업논문 Chapter 1-2 초안 [우선순위: 높음]

- [ ] **1.11 Chapter 1: Introduction**
  - [ ] 1.1 연구 배경 및 동기
  - [ ] 1.2 Hate speech의 사회적/심리적 영향
  - [ ] 1.3 연구 목적 및 의의
  - [ ] 1.4 논문 구성
  - **기한**: 1월 18일
  - **산출물**: `thesis/chapter1_introduction.md`

- [ ] **1.12 Chapter 2: Literature Review**
  - [ ] 2.1 Emotional language processing
    - [ ] 2.1.1 Attention narrowing (Ding et al., 2016)
    - [ ] 2.1.2 Enhanced processing (Kissler et al., 2006)
    - [ ] 2.1.3 Memory effects (Kensinger et al., 2006)
  - [ ] 2.2 Hate speech: Definitions and effects
  - [ ] 2.3 Self-paced reading methodology
  - [ ] 2.4 Research gaps and present study
  - **기한**: 1월 20일
  - **산출물**: `thesis/chapter2_literature.md`

---

## Phase 2: 중기 개선 (2-4개월, 2025년 2-4월)

### 🎯 목표: 실험 재설계 + EEG 준비 + 졸업논문 완성

### Todo List

#### F. 실험 개선 및 추가 데이터 수집 [우선순위: 최고]

- [ ] **2.1 Stimuli 재설계**
  - [ ] **Option A: 객관성 차원 추가 (2×2×2 design)**
    - [ ] Factor 1: Objectivity (Objective vs. Subjective)
    - [ ] Factor 2: Valence (Negative vs. Neutral)
    - [ ] Factor 3: Plausibility (Plausible vs. Implausible)
    - [ ] 새로운 stimuli 32개 제작
  - [ ] **Option B: 맥락 조작 추가**
    - [ ] Background passage 3 versions:
      - [ ] Neutral/academic context (현재)
      - [ ] Conflict/threat context (경쟁, 위협 상황)
      - [ ] Positive/empathic context (문화 존중)
    - [ ] Between-subjects design 고려
  - [ ] **PI 상담 필요**: 어떤 접근이 더 적절한가?
  - **기한**: 2월 15일

- [ ] **2.2 Norming Study 실시**
  - [ ] 모든 modifier의 valence, arousal, objectivity ratings
  - [ ] 참가자 30명 이상 온라인 설문
  - [ ] ANEW-KR 또는 유사 도구 활용
  - [ ] 결과로 stimuli 균형 조정
  - **기한**: 2월 28일
  - **산출물**: `norming_study_report.pdf`

- [ ] **2.3 개선된 실험 파일럿 (N=10-15)**
  - [ ] 새로운 디자인 테스트
  - [ ] 과제 난이도 및 시간 확인
  - [ ] 예비 데이터 분석
  - [ ] 필요시 수정
  - **기한**: 3월 15일

- [ ] **2.4 본 실험 데이터 수집 (N=40-60)**
  - [ ] IRB 승인 (필요시)
  - [ ] 온라인 실험 배포
  - [ ] 데이터 품질 모니터링
  - [ ] 주 2회 진행 상황 점검
  - **기한**: 4월 15일

- [ ] **2.5 개선된 데이터 분석**
  - [ ] Pre-registered analysis plan 작성
  - [ ] Mixed-effects models
  - [ ] Effect size 및 power 보고
  - [ ] Mediation/moderation 분석
  - **기한**: 4월 30일

#### G. EEG 실험 준비 [우선순위: 중간]

- [ ] **2.6 EEG 연구실 접촉 및 협력 논의**
  - [ ] 서울대 내 EEG facility 확인
  - [ ] 공동연구 가능성 타진
  - [ ] 장비 사용 일정 협의
  - **기한**: 2월 28일

- [ ] **2.7 EEG 실험 프로토콜 설계**
  - [ ] N400/P600 측정을 위한 timeline 조정
  - [ ] Epoch: -200 to 800 ms
  - [ ] 전극 배치: 최소 32 channels
  - [ ] Artifact rejection 기준
  - **기한**: 3월 15일
  - **산출물**: `eeg_protocol.md`

- [ ] **2.8 EEG 파일럿 (N=5-10)**
  - [ ] 기술적 이슈 확인
  - [ ] Signal quality 검증
  - [ ] Preliminary ERP waveforms
  - **기한**: 4월 30일 (여유 있게)
  - **참고**: 졸업논문에는 행동 데이터만 포함, EEG는 향후 연구로

#### H. 졸업논문 완성 [우선순위: 최고]

- [ ] **2.9 Chapter 3: Methods**
  - [ ] 3.1 Participants
  - [ ] 3.2 Materials (Stimuli 상세)
  - [ ] 3.3 Procedure
  - [ ] 3.4 Data Analysis
  - **기한**: 3월 31일
  - **산출물**: `thesis/chapter3_methods.md`

- [ ] **2.10 Chapter 4: Results**
  - [ ] 4.1 Descriptive statistics
  - [ ] 4.2 Manipulation check
  - [ ] 4.3 H1: Attention capture
  - [ ] 4.4 H2: Attention narrowing
  - [ ] 4.5 H3: Biased memory
  - [ ] 4.6 H4: Reproduction bias
  - [ ] 4.7 Mediation analysis
  - **기한**: 4월 15일
  - **산출물**: `thesis/chapter4_results.md`

- [ ] **2.11 Chapter 5: Discussion**
  - [ ] 5.1 Summary of findings
  - [ ] 5.2 Theoretical implications
  - [ ] 5.3 Methodological contributions
  - [ ] 5.4 Limitations
  - [ ] 5.5 Future directions (EEG integration)
  - **기한**: 4월 30일
  - **산출물**: `thesis/chapter5_discussion.md`

- [ ] **2.12 Abstract, References, Appendices**
  - [ ] Abstract (국문, 영문)
  - [ ] References (APA 7th)
  - [ ] Appendix A: Full stimuli list
  - [ ] Appendix B: Additional analyses
  - **기한**: 5월 10일

- [ ] **2.13 전체 통합 및 교정**
  - [ ] 일관성 검토
  - [ ] 영문 교정
  - [ ] 그림/표 번호 및 캡션
  - [ ] 최종 포맷팅
  - **기한**: 5월 20일

- [ ] **2.14 논문 제출**
  - [ ] 지도교수 최종 승인
  - [ ] 학과 제출
  - **기한**: 6월 1일 (학사 일정 확인 필요)

---

## Phase 3: 장기 발전 (6개월 이후, 2025년 하반기~)

### 🎯 목표: 석사 진학 또는 출판 준비

### Todo List

#### I. EEG 본 실험 [출판용]

- [ ] **3.1 EEG 본 실험 (N=30-40)**
  - [ ] 충분한 trial 수 확보 (조건당 30+ trials)
  - [ ] High-quality EEG recording
  - [ ] 행동 데이터 동시 수집

- [ ] **3.2 EEG 데이터 분석**
  - [ ] Preprocessing: filtering, ICA, artifact rejection
  - [ ] ERP analysis: N400, P600 components
  - [ ] Time-window 및 electrode selection
  - [ ] Statistical analysis: cluster-based permutation test

- [ ] **3.3 행동-EEG 통합 분석**
  - [ ] RT와 N400 amplitude 상관
  - [ ] Judgment accuracy와 P600 관계
  - [ ] Individual differences in ERP effects

#### J. 통합 논문 작성 [출판용]

- [ ] **3.4 통합 논문 작성**
  - [ ] 행동 + EEG 결과 통합
  - [ ] 종합적 discussion
  - [ ] 목표 저널 선정:
    - Cognition and Emotion
    - Journal of Experimental Psychology: Learning, Memory, and Cognition
    - Language, Cognition and Neuroscience
  - [ ] 투고 전 영문 교정

- [ ] **3.5 학회 발표**
  - [ ] CUNY (March)
  - [ ] AMLaP (September)
  - [ ] 한국심리학회

---

## 즉시 수정/개선 가능 항목 (이번 주 내)

### ✅ 지금 당장 할 수 있는 것

#### 1. 개념 정리 문서 작성
```markdown
파일명: conceptual_refinement.md

내용:
- Hate speech vs. Emotional/Negative speech 비교표
- 본 연구 stimuli 재분류:
  * High subjective, High negative: 열등한, 미개한
  * Low subjective, High negative: 생고기를 먹는 (객관적 부정)
  * High subjective, Low negative: 독특한, 신비로운
- Manipulation check 데이터 재해석
- 최종 용어 제안: "Negative Group-Directed Language" 고려
```

**즉시 작성 가능 - 데이터/실험 불필요**

#### 2. 효과 크기 재계산 스크립트
```python
# scripts/analysis/calculate_effect_sizes.py

import pandas as pd
import numpy as np
from scipy import stats

# Cohen's d 계산
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
    s_pooled = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / s_pooled

# 각 region별 효과 크기 계산
regions = ['modifier', 'critical_noun', 'spillover1', 'spillover2']
for region in regions:
    hate_rt = data[data['emotion']=='hate'][region+'_rt']
    neutral_rt = data[data['emotion']=='neutral'][region+'_rt']

    d = cohens_d(hate_rt, neutral_rt)
    print(f"{region}: Cohen's d = {d:.3f}")
```

**즉시 실행 가능 - 기존 데이터 활용**

#### 3. 문헌 조사 시작
```
검색 키워드:
- "hate speech" AND "cognitive processing"
- "emotional language" AND "reading time"
- "negative language" AND "memory bias"
- "group-based threat" AND "attention"

데이터베이스:
- PubMed
- Google Scholar
- PsycINFO
- Web of Science

목표: 20편 이상 수집, 10편 정독
```

**즉시 시작 가능**

#### 4. 기존 결과 재정리

**현재 있는 분석 파일 확인:**
```bash
ls results/result_1201/
```

**추가 분석 실행:**
- Manipulation check 재분석: Hate vs. Neutral modifiers 평균 차이
- Region별 상세 breakdown
- 참가자별 효과 크기 histogram

**즉시 가능**

---

## PI 상담 아젠다 (우선순위순)

### 🔴 긴급 결정 필요

1. **용어 선택: Hate speech vs. Emotional/Negative speech**
   - 현재 데이터/방법론과의 정합성
   - 이론적 기여 vs. 명확성 trade-off
   - PI 의견: ?

2. **중기 실험 재설계 방향**
   - Option A: Objectivity 차원 추가 (2×2×2)
   - Option B: Context 조작 (background passage)
   - Option C: 현재 디자인 유지 + 참가자 증원
   - PI 의견: ?

3. **졸업논문 범위**
   - 행동 데이터만 vs. EEG 파일럿 포함 여부
   - 제출 시한과 EEG 실험 일정 고려
   - PI 의견: ?

### 🟡 상담 필요

4. **Effect size 해석 전략**
   - 4% RT 증가를 어떻게 defend할 것인가
   - 추가 참가자 모집 필요성
   - Benchmark 문헌 충분성

5. **Mediation analysis 타당성**
   - 현재 디자인에서 인과관계 주장 가능 범위
   - Cross-sectional data의 한계

6. **EEG 협력 연구 가능성**
   - 서울대 내 연구실 추천
   - 공동 저자 체계
   - 예산 및 일정

### 🟢 정보 공유

7. **학사 일정 확인**
   - 논문 제출 마감: ?
   - 심사 일정: ?
   - 발표 요구사항: ?

8. **출판 목표 논의**
   - 졸업 후 학술지 투고 계획
   - 석사 진학 고려 여부

---

## 리스크 관리

### 잠재적 문제 및 대응 방안

| 리스크 | 확률 | 영향 | 대응 방안 |
|--------|------|------|-----------|
| RT 효과 크기 작아서 reject 우려 | 중 | 고 | 문헌 벤치마크, power analysis, 참가자 증원 |
| Hate speech 정의 논란 | 고 | 중 | 용어 변경, 조작적 정의 강화 |
| EEG 실험 일정 지연 | 고 | 중 | 졸업논문에서 제외, 후속 연구로 |
| 논문 제출 마감 촉박 | 중 | 고 | 주간 진행 점검, 백업 계획 |
| 추가 데이터 수집 실패 | 저 | 고 | 온라인 실험, 인센티브 확대 |

---

## 주간 체크리스트 템플릿

```markdown
### Week of [날짜]

#### Completed
- [ ] 항목 1
- [ ] 항목 2

#### In Progress
- [ ] 항목 3 (50% 완료)

#### Blocked
- [ ] 항목 4 (이유: PI 피드백 대기)

#### Next Week Priorities
1.
2.
3.

#### Notes
-
```

---

## 현재 프로젝트 상태 Summary

### 완료 ✅
- 행동실험 1차 데이터 수집
- H1-H4 기초 분석
- 프레젠테이션 발표

### 진행 중 🔄
- Daniel 교수 피드백 반영
- 효과 크기 분석
- 문헌 조사

### 대기 중 ⏸️
- PI 지도 (용어, 디자인 결정)
- 추가 데이터 수집
- EEG 실험

### 다음 마일스톤 🎯
- **1월 20일**: Phase 1 완료 (즉시 개선)
- **5월 1일**: Phase 2 완료 (졸업논문 초안)
- **6월 1일**: 논문 제출

---

## 참고 자료

### 핵심 논문
1. Ding et al. (2016) - Negative emotional verbs
2. Kissler et al. (2006) - Emotional word processing
3. Kensinger et al. (2006) - Emotional memory
4. Schindler et al. (2023) - Task-dependent emotion effects

### 방법론 참고
- Self-paced reading: Jegerski (2014)
- Mixed-effects models: Barr et al. (2013)
- EEG/ERP: Luck (2014)
- Mediation: Hayes (2013) PROCESS

### 데이터 관리
- Raw data: `results/result_1201/`
- Scripts: `scripts/analysis/`, `scripts/visualization/`
- Documentation: `documentation/research/`
- Thesis: `thesis/` (새로 생성)

---

**최종 업데이트**: 2025년 12월 26일
**다음 검토 예정**: 2025년 1월 5일 (PI 미팅 후)
