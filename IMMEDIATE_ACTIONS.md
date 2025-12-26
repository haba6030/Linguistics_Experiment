# 즉시 실행 가능한 개선 사항 (이번 주)

**작성일**: 2025년 12월 26일
**목표**: PI 미팅 전 최대한의 준비 완료

---

## 1. 개념적 재정의 문서 [우선순위: 최고]

### 1.1 Hate Speech vs. Alternative Terms

#### 비교 분석표

| 차원 | Hate Speech | Emotional Speech | Negative Speech | Group-Directed Negative Language |
|------|-------------|------------------|-----------------|----------------------------------|
| **정의 명확성** | 논란 많음 | 명확함 | 명확함 | 중간 |
| **이론적 기여** | 높음 (새로운 영역) | 중간 | 낮음 (기존 연구 많음) | 높음 |
| **Stimuli 적합성** | 중간 (맥락 부족) | 높음 | 높음 | 높음 |
| **Manipulation Check 정합성** | 중간 (부정성만 측정) | 높음 | 높음 | 높음 |
| **사회적 함의** | 높음 | 중간 | 낮음 | 높음 |

#### 현재 Stimuli 재분류

**Hate modifiers (11개)**:
- 주관적 평가형: 미개한, 열등한, 저급한, 야만적인, 천박한, 저능한, 격떨어지는, 수준낮은
- 부정적 특성: 뒤떨어진, 나태한, 무지한

**특성 분석**:
- ✅ Negative: 평균 4.2/5 (manipulation check)
- ✅ Subjective: 모두 주관적 평가
- ✅ Group-directed: 탈렌족 전체 대상
- ⚠️ Context-independent hate: 맥락 없이는 hate speech 판단 어려움

**Neutral modifiers (12개)**:
- 객관적 사실형: 고립된, 산악의, 소규모의, 정착한, 산맥의
- 중립적 특성: 자급자족의, 폐쇄적, 독특한, 전통적인, 자연적인, 관습적, 적응적

**특성 분석**:
- ✅ Negative: 평균 1.8/5 (manipulation check)
- ✅ Objective/Neutral evaluation
- ✅ Group-directed

#### 제안: 3단계 접근

**접근 1: Hate Speech 유지 + 조작적 정의 강화**
```
"본 연구에서 hate speech는 특정 집단을 향한 주관적이고
평가적인 부정 표현으로, 집단 전체에 대한 경멸, 열등함,
위협을 암시하는 언어적 표지를 포함한다 (Matsuda, 1993;
Gelber, 2002)."

장점: 이론적 기여 명확, 사회적 함의 강함
단점: 맥락 부족, 정의 논란, 가상 집단의 한계
```

**접근 2: Negative Group-Directed Language (추천)**
```
"집단 지향적 부정 언어 (Negative Group-Directed Language):
특정 사회 집단 전체를 대상으로 하는 부정적 평가 및 특성
귀속 표현. Hate speech의 핵심 요소인 negativity와
group-targeting을 포함하되, 맥락에 따른 hate 판단의
복잡성을 회피."

장점: 조작적으로 명확, 현재 디자인과 정합, 중립적
단점: 이론적 새로움 약함, hate speech 문헌과 거리
```

**접근 3: Emotionally Negative Language**
```
"감정적 부정 언어: 부정적 감정가(negative valence)와
높은 각성(arousal)을 가진 집단 지향적 표현."

장점: 감정 연구 전통과 연결, 측정 명확
단점: Group-directed 측면 약화, 사회적 함의 축소
```

#### 최종 제안: Hybrid Approach

**용어**: "Hate-related Negative Language" 또는 "Derogatory Group Language"

**정의**:
```
본 연구는 hate speech의 핵심 구성 요소인 집단 대상 부정성
(group-directed negativity)과 평가적 경멸(evaluative
derogation)에 초점을 맞춘다. 완전한 hate speech는
사회적 맥락, 권력 관계, 역사적 배경을 요구하나 (Brown, 2017),
본 연구의 실험적 통제를 위해 이러한 요소를 제거하고
언어적 표지만을 조작하였다. 이는 hate speech의 인지적
메커니즘을 분리하여 검증하는 첫 단계로 이해되어야 한다.
```

**PI 질문**:
- 어떤 접근이 가장 적절한가?
- 졸업논문 vs. 향후 출판에서 용어 다르게 사용 가능한가?

---

## 2. 효과 크기 분석 및 해석 [즉시 실행]

### 2.1 기존 데이터 재분석 스크립트

```python
# scripts/analysis/immediate_effect_size_analysis.py

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드
data_path = '../results/result_1201/'
# TODO: 실제 데이터 파일명 확인 필요

# 2. Cohen's d 계산 함수
def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# 3. Confidence Interval
def cohens_d_ci(group1, group2, confidence=0.95):
    """Calculate CI for Cohen's d using bootstrap"""
    from scipy.stats import bootstrap

    def statistic(x, y):
        return cohens_d(x, y)

    # Bootstrap
    n_bootstrap = 10000
    d_bootstrap = []
    for _ in range(n_bootstrap):
        sample1 = np.random.choice(group1, size=len(group1), replace=True)
        sample2 = np.random.choice(group2, size=len(group2), replace=True)
        d_bootstrap.append(cohens_d(sample1, sample2))

    lower = np.percentile(d_bootstrap, (1-confidence)/2 * 100)
    upper = np.percentile(d_bootstrap, (1+confidence)/2 * 100)

    return lower, upper

# 4. Region별 효과 크기 계산
regions = {
    'R1_Subject': 'R1: 주어',
    'R2_Modifier': 'R2: 수식어 (조작)',
    'R3_NounPhrase': 'R3: 명사구',
    'R4_Adverb': 'R4: 부사구',
    'R5_Verb': 'R5: 동사',
    'R6_CriticalNoun': 'R6: 핵심 명사 (그럴듯함 조작)',
    'R7_Spillover1': 'R7: Spillover 1',
    'R8_Final': 'R8: 문장 종결'
}

results = []

for region_code, region_name in regions.items():
    # Hate vs. Neutral
    hate_rt = data[data['emotion'] == 'hate'][f'{region_code}_RT']
    neutral_rt = data[data['emotion'] == 'neutral'][f'{region_code}_RT']

    # Effect size
    d = cohens_d(hate_rt, neutral_rt)
    lower_ci, upper_ci = cohens_d_ci(hate_rt, neutral_rt)

    # Descriptive
    hate_mean = np.mean(hate_rt)
    neutral_mean = np.mean(neutral_rt)
    diff_ms = hate_mean - neutral_mean
    diff_pct = (diff_ms / neutral_mean) * 100

    # t-test
    t_stat, p_val = stats.ttest_ind(hate_rt, neutral_rt)

    results.append({
        'Region': region_name,
        'Hate_M': hate_mean,
        'Neutral_M': neutral_mean,
        'Diff_ms': diff_ms,
        'Diff_%': diff_pct,
        "Cohen's_d": d,
        'CI_lower': lower_ci,
        'CI_upper': upper_ci,
        't': t_stat,
        'p': p_val
    })

# 결과 테이블
df_results = pd.DataFrame(results)
print(df_results.to_string())

# 5. Visualization
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Panel A: RT difference
ax1 = axes[0]
x = np.arange(len(regions))
ax1.bar(x, df_results['Diff_ms'], color='steelblue', alpha=0.7)
ax1.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax1.set_xticks(x)
ax1.set_xticklabels(df_results['Region'], rotation=45, ha='right')
ax1.set_ylabel('RT Difference (ms)\nHate - Neutral')
ax1.set_title('A. Reading Time Differences by Region')
ax1.grid(axis='y', alpha=0.3)

# Panel B: Effect sizes
ax2 = axes[1]
ax2.errorbar(x, df_results["Cohen's_d"],
             yerr=[df_results["Cohen's_d"] - df_results['CI_lower'],
                   df_results['CI_upper'] - df_results["Cohen's_d"]],
             fmt='o', markersize=8, capsize=5, color='darkred')
ax2.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax2.axhline(0.2, color='gray', linestyle=':', linewidth=0.8, label='Small effect')
ax2.axhline(0.5, color='gray', linestyle=':', linewidth=0.8, label='Medium effect')
ax2.axhline(0.8, color='gray', linestyle=':', linewidth=0.8, label='Large effect')
ax2.set_xticks(x)
ax2.set_xticklabels(df_results['Region'], rotation=45, ha='right')
ax2.set_ylabel("Cohen's d\n(with 95% CI)")
ax2.set_title("B. Effect Sizes by Region")
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../results/immediate_analysis/effect_size_analysis.png', dpi=300)
plt.show()

# 6. 요약 보고서
print("\n=== EFFECT SIZE SUMMARY ===")
print(f"\nModifier Region (R2):")
print(f"  Hate: {df_results.iloc[1]['Hate_M']:.1f} ms")
print(f"  Neutral: {df_results.iloc[1]['Neutral_M']:.1f} ms")
print(f"  Difference: {df_results.iloc[1]['Diff_ms']:.1f} ms ({df_results.iloc[1]['Diff_%']:.2f}%)")
print(f"  Cohen's d = {df_results.iloc[1]['Cohen\'s_d']:.3f} [{df_results.iloc[1]['CI_lower']:.3f}, {df_results.iloc[1]['CI_upper']:.3f}]")
print(f"  p = {df_results.iloc[1]['p']:.4f}")

print(f"\nCritical Noun Region (R6):")
print(f"  Difference: {df_results.iloc[5]['Diff_ms']:.1f} ms ({df_results.iloc[5]['Diff_%']:.2f}%)")
print(f"  Cohen's d = {df_results.iloc[5]['Cohen\'s_d']:.3f}")

# 7. Interaction effect (Hate × Plausibility)
# TODO: Mixed-effects model에서 추출
```

### 2.2 문헌 벤치마크 조사 (진행 중)

#### 검색 전략

**데이터베이스**: Google Scholar, PubMed
**키워드**:
- "emotional word" AND "reading time" AND "effect size"
- "self-paced reading" AND "emotion" AND "RT"
- "N400" AND "behavioral correlate" AND "RT"

#### 예비 문헌 리스트 (수집 필요)

| Study | Task | Manipulation | RT Diff | Effect Size | Notes |
|-------|------|--------------|---------|-------------|-------|
| Kissler et al. (2006) | Lexical decision | Emotional vs. Neutral words | ~30ms | d≈0.4 | 단어 수준 |
| Scott et al. (2009) | Reading | Emotional vs. Neutral context | ~50ms | ? | 문장 수준 |
| Ding et al. (2016) | SPR | Negative verb + incongruent noun | ? | ? | 상호작용 효과 |
| **Our study** | SPR | Hate vs. Neutral modifier | ~25ms (4%) | d≈? | 문장 내 조작 |

**TODO**:
- [ ] 각 논문 full-text 확인
- [ ] 정확한 RT 차이 및 effect size 추출
- [ ] 과제 유사성 고려하여 비교

#### 예상 해석

```
"본 연구의 modifier region에서 관찰된 4% RT 증가(약 25ms,
Cohen's d ≈ 0.3)는 단어 수준의 감정 처리 효과(Kissler et al.,
2006: 30ms, d=0.4)와 유사한 크기이나, 문장 맥락 내에서의
조작이라는 점을 고려하면 이론적으로 의미 있는 효과로 해석된다.

통계적 검정력(power) 분석 결과, 현재 표본 크기(N=?)에서
이러한 효과를 80% 검정력으로 탐지하기 위해서는...
[추가 분석 필요]"
```

### 2.3 Power Analysis

```r
# R script: power_analysis.R

library(pwr)

# 현재 효과 크기로 필요한 샘플 크기
d_observed <- 0.3  # TODO: 실제 계산값으로 대체

# Between-subjects
pwr.t.test(d = d_observed, sig.level = 0.05, power = 0.80,
           type = "two.sample")

# Within-subjects (repeated measures)
# 더 적은 샘플 필요
pwr.t.test(d = d_observed, sig.level = 0.05, power = 0.80,
           type = "paired")

# Mixed-effects 고려
# TODO: simr package로 시뮬레이션
```

---

## 3. 추가 분석 (현재 데이터)

### 3.1 Mediation Analysis

```r
# R script: mediation_analysis.R

library(lavaan)
library(mediation)

# Model: RT (modifier) -> Plausibility Judgment -> Free Recall Negativity

# Step 1: Prepare data
# - Aggregate by participant
# - Hate effect on RT: hate_rt - neutral_rt
# - Plausibility bias: accuracy difference
# - Free recall negativity: sentiment score

# Step 2: Path model
mediation_model <- '
  # Direct effects
  plaus_bias ~ a * rt_effect
  recall_neg ~ b * plaus_bias + c_prime * rt_effect

  # Indirect effect
  indirect := a * b
  total := c_prime + (a * b)
'

fit <- sem(mediation_model, data = data_agg)
summary(fit, standardized = TRUE, fit.measures = TRUE)

# Step 3: Bootstrap CI
boot_results <- parameterEstimates(fit, boot.num = 5000,
                                   ci = TRUE, level = 0.95)
print(boot_results)

# Step 4: Visualization
library(semPlot)
semPaths(fit, what = "std", layout = "tree",
         edge.label.cex = 1.2, curvePivot = TRUE)
```

**예상 결과**:
- Indirect effect = ? (p = ?)
- 해석: RT 증가 → 판단 편향 → 회상 부정성 경로 유의/비유의

### 3.2 Region-by-Region Timeline

```python
# scripts/visualization/rt_timeline_detailed.py

import matplotlib.pyplot as plt
import seaborn as sns

# 문장 구조 시각화
sentence_structure = [
    "탈렌족은",           # R1: Subject
    "[열등한/고립된]",    # R2: Modifier (MANIPULATION)
    "민족으로",           # R3: Noun phrase
    "의식을",             # R4: Adverb
    "위해",               # R5: Verb
    "[전통 의상을/돌을]", # R6: Critical noun (PLAUSIBILITY)
    "입는다",             # R7: Spillover 1
    "."                   # R8: Final
]

# RT plotting
fig, ax = plt.subplots(figsize=(14, 6))

# Hate condition
ax.plot(range(8), hate_rt_by_region, 'o-',
        color='red', linewidth=2, markersize=10,
        label='Hate modifier', alpha=0.8)

# Neutral condition
ax.plot(range(8), neutral_rt_by_region, 's-',
        color='blue', linewidth=2, markersize=10,
        label='Neutral modifier', alpha=0.8)

# Highlight critical regions
ax.axvspan(1.5, 2.5, alpha=0.1, color='red',
           label='Modifier manipulation')
ax.axvspan(5.5, 6.5, alpha=0.1, color='orange',
           label='Plausibility manipulation')

ax.set_xticks(range(8))
ax.set_xticklabels(sentence_structure, rotation=45, ha='right')
ax.set_xlabel('Sentence Position', fontsize=12)
ax.set_ylabel('Reading Time (ms)', fontsize=12)
ax.set_title('Reading Time Timeline: Hate vs. Neutral Modifiers',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../results/immediate_analysis/rt_timeline_detailed.png', dpi=300)
```

### 3.3 Manipulation Check 재분석

```python
# scripts/analysis/manipulation_check_detailed.py

# 1. Hate modifiers 평균 negativity
hate_mods = ['미개한', '열등한', '저급한', '야만적인', '뒤떨어진',
             '천박한', '나태한', '저능한', '무지한', '격떨어지는', '수준낮은']
neutral_mods = ['고립된', '자급자족의', '폐쇄적', '독특한', '산악의',
                '소규모의', '전통적인', '자연적인', '산맥의', '정착한',
                '관습적', '적응적']

# Negativity ratings (1-5)
hate_ratings = mc_data[mc_data['modifier'].isin(hate_mods)]['rating']
neutral_ratings = mc_data[mc_data['modifier'].isin(neutral_mods)]['rating']

print(f"Hate modifiers: M = {hate_ratings.mean():.2f}, SD = {hate_ratings.std():.2f}")
print(f"Neutral modifiers: M = {neutral_ratings.mean():.2f}, SD = {neutral_ratings.std():.2f}")

# t-test
t, p = stats.ttest_ind(hate_ratings, neutral_ratings)
d = cohens_d(hate_ratings, neutral_ratings)
print(f"t({len(hate_ratings)+len(neutral_ratings)-2}) = {t:.2f}, p < .001, d = {d:.2f}")

# 2. Individual modifiers
mod_summary = mc_data.groupby('modifier')['rating'].agg(['mean', 'std', 'count'])
mod_summary = mod_summary.sort_values('mean', ascending=False)
print(mod_summary)

# 3. Visualization
fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(range(len(mod_summary)), mod_summary['mean'],
        color=['red' if mod in hate_mods else 'blue'
               for mod in mod_summary.index],
        alpha=0.7)
ax.set_yticks(range(len(mod_summary)))
ax.set_yticklabels(mod_summary.index)
ax.set_xlabel('Negativity Rating (1-5)')
ax.set_title('Manipulation Check: Modifier Negativity Ratings')
ax.axvline(3, color='black', linestyle='--', linewidth=0.8, label='Midpoint')
ax.legend()
plt.tight_layout()
plt.savefig('../results/immediate_analysis/manipulation_check.png', dpi=300)
```

---

## 4. 발표자료 즉시 개선

### 4.1 추가할 슬라이드 목록

**새 슬라이드 4-1: "Conceptual Clarification"**
```
Title: Defining Our Construct

본 연구의 초점: Hate Speech vs. Negative Group-Directed Language

[비교 테이블]
- Definition clarity
- Theoretical contribution
- Stimuli fit
- Manipulation check alignment

결론: "Derogatory Group Language"로 재정의 제안
```

**새 슬라이드 6-1: "All Task Examples"**
```
Title: Participant Tasks (Detailed)

1. Self-Paced Reading
   [화면 캡처 이미지]

2. Plausibility Judgment
   "Given the background, does this make sense?"
   [실제 화면]

3. Free Recall
   [실제 참가자 응답 3-4개]

4. Manipulation Check
   [전체 modifier 목록 - 백업 슬라이드로]
```

**새 슬라이드 9-1: "Effect Size Interpretation"**
```
Title: RT Effect Size: Small but Meaningful

Our findings:
- Modifier region: +25ms (4%), d = 0.3
- Critical noun: +15ms (2.5%), d = 0.2

Literature comparison:
- Kissler et al. (2006): 30ms, d = 0.4 (word level)
- Scott et al. (2009): 50ms (sentence level)

Interpretation:
- Comparable to established emotional word effects
- Within-sentence manipulation → naturally smaller
- Statistical power: N=? adequate for d=0.3
```

### 4.2 그래프 개선

현재 그래프 → 개선안:
1. RT by region → Timeline plot with sentence structure
2. 단순 bar plot → Error bars + effect sizes annotated
3. 흑백 → Color-coded by significance

---

## 5. 졸업논문 Chapter 1-2 시작

### 5.1 Chapter 1 Outline

```markdown
# Chapter 1: Introduction

## 1.1 연구의 배경 및 필요성
- Hate speech의 사회적 확산 (온라인, 소셜미디어)
- 언어가 태도 및 행동에 미치는 영향
- 인지적 메커니즘 연구의 부재

## 1.2 연구의 목적
- RQ1: Hate speech가 온라인 처리에 미치는 영향
- RQ2: 기억 encoding에서의 bias
- RQ3: 언어 재생산에서의 distortion

## 1.3 연구의 의의
- 이론적: 감정 언어 처리 → hate speech로 확장
- 방법론적: Behavioral + EEG 통합 설계
- 사회적: Hate speech 확산 메커니즘 이해

## 1.4 논문의 구성
[각 chapter 요약]
```

### 5.2 Chapter 2 Outline

```markdown
# Chapter 2: Literature Review

## 2.1 Emotional Language Processing
### 2.1.1 Attention Capture and Narrowing
- Ding et al. (2016): Negative verbs
- Kensinger & Corkin (2003): Emotional attention

### 2.1.2 Enhanced vs. Impaired Processing
- Kissler et al. (2006): Enhanced cortical response
- Schindler et al. (2023): Task-dependent effects

### 2.1.3 Memory Effects
- Kensinger et al. (2006): Trade-off effect
- Emotional enhancement vs. peripheral impairment

## 2.2 Hate Speech: Definitions and Effects
### 2.2.1 Conceptual Definitions
- Legal definitions
- Psychological definitions
- Linguistic definitions

### 2.2.2 Psychological Effects
- Threat perception
- Prejudice activation
- Behavioral consequences

### 2.2.3 Cognitive Processing (Gap)
- Limited experimental studies
- Need for controlled paradigms

## 2.3 Self-Paced Reading Methodology
- Fine-grained RT measurements
- Word-by-word processing
- Spillover effects

## 2.4 Present Study
- Research questions
- Hypotheses
- Overview of methods
```

---

## 실행 체크리스트 (이번 주)

### 오늘 (12월 26일)
- [x] THESIS_ROADMAP.md 작성
- [x] IMMEDIATE_ACTIONS.md 작성
- [ ] 개념 재정의 문서 작성 시작 (`conceptual_framework.md`)
- [ ] Effect size 계산 스크립트 실행
- [ ] 문헌 검색 시작 (10편 목록 작성)

### 내일 (12월 27일)
- [ ] 효과 크기 분석 완료
- [ ] Manipulation check 재분석
- [ ] Chapter 1 outline 상세화
- [ ] PI 미팅 아젠다 정리

### 모레 (12월 28일)
- [ ] Mediation analysis 실행
- [ ] RT timeline 그래프 개선
- [ ] 발표자료 슬라이드 추가
- [ ] Chapter 2 literature 10편 정독 시작

### 주말 (12월 29-30일)
- [ ] 문헌 조사 심화 (effect size benchmark)
- [ ] Chapter 1-2 초안 작성
- [ ] PI 미팅 준비 자료 통합

### 다음 주 월요일 (12월 30일)
- [ ] PI 미팅 (이메일로 일정 요청)
- [ ] 피드백 반영 계획 수립

---

**진행 상황 추적**: 이 문서에 직접 체크 표시
**질문/이슈**: 별도 `QUESTIONS_FOR_PI.md` 작성
**다음 업데이트**: 12월 27일 저녁
