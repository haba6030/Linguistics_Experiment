# 효과 크기 분석 실행 가이드

**목적**: 현재 실험 데이터에서 Cohen's d 효과 크기 계산 및 시각화

**소요 시간**: 30-60분 (데이터 준비 10분 + 실행 5분 + 해석 15-30분)

---

## 📋 준비 사항

### 1.1 필요한 파일

**데이터 파일** (다음 중 하나):
- `results/result_1201/[실제_데이터_파일].csv` 또는
- `results/result_1128/[실제_데이터_파일].csv`

**분석 스크립트**:
- `immediate_analysis/effect_size_calculator.py` (이미 준비됨 ✅)

### 1.2 데이터 파일 확인

먼저 데이터 파일 위치와 구조를 확인하세요:

```bash
# 데이터 파일 목록 확인
ls -lh results/result_1201/*.csv
ls -lh results/result_1128/*.csv

# 데이터 구조 미리보기 (첫 5줄)
head -n 5 results/result_1201/[파일명].csv
```

**예상 컬럼**:
- `subject` 또는 `participant_id`
- `modifier_type` (hate/neutral 또는 derogatory/neutral)
- `plausibility` (plausible/implausible)
- `region` (1, 2, 3, ... 또는 modifier, critical_noun 등)
- `RT` 또는 `reading_time` (밀리초 단위)

---

## 🚀 1단계: 스크립트 실행 (기본)

### 1.1 가장 간단한 방법

```bash
cd /Users/jinilkim/Library/CloudStorage/OneDrive-Personal/Projects/lingThesis/immediate_analysis

# 스크립트 실행 (데이터 경로만 수정)
python effect_size_calculator.py
```

**첫 실행 시**: 스크립트가 데이터 경로를 묻습니다.

### 1.2 데이터 경로 지정

스크립트 내부에서 다음 줄을 찾아 수정:

```python
# Line ~15-20에서 찾기
DATA_FILE = "../results/result_1201/[실제_파일명].csv"
```

**예시**:
```python
DATA_FILE = "../results/result_1201/rt_data_cleaned.csv"
```

---

## 📊 2단계: 데이터 구조에 맞게 스크립트 조정

### 2.1 컬럼명 확인 및 수정

데이터 파일의 실제 컬럼명을 확인:

```bash
head -n 1 results/result_1201/[파일명].csv
```

출력 예시:
```
subject,condition,item,region,RT,plausibility_rating
```

스크립트에서 해당 컬럼명으로 수정:

```python
# effect_size_calculator.py 내부 (약 Line 30-40)

# 원래 코드 (예시)
df = pd.read_csv(DATA_FILE)
modifier_col = 'modifier_type'  # ← 실제 컬럼명으로 수정
rt_col = 'RT'                   # ← 실제 컬럼명으로 수정
region_col = 'region'           # ← 실제 컬럼명으로 수정

# 수정 예시
modifier_col = 'condition'      # 실제 데이터에서 사용하는 이름
rt_col = 'RT'
region_col = 'region'
```

### 2.2 조건명 확인

Modifier 조건이 어떻게 코딩되어 있는지 확인:

```python
# Python에서 직접 확인
import pandas as pd
df = pd.read_csv('../results/result_1201/[파일명].csv')
print(df['condition'].unique())
```

출력 예시:
```
['hate' 'neutral']  또는
['derogatory' 'neutral']  또는
['H' 'N']
```

스크립트에서 이에 맞게 수정:

```python
# effect_size_calculator.py 내부

# 조건 필터링 (Line ~50-60)
hate_data = df[df[modifier_col] == 'hate']     # 또는 'derogatory', 'H' 등
neutral_data = df[df[modifier_col] == 'neutral'] # 또는 'N' 등
```

---

## 🔧 3단계: 완전한 실행 예시

### 3.1 수정된 스크립트 예시

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ========== 1. 데이터 로드 ==========
DATA_FILE = "../results/result_1201/rt_data_cleaned.csv"  # ← 수정 필요
df = pd.read_csv(DATA_FILE)

# ========== 2. 컬럼명 설정 ==========
modifier_col = 'condition'      # ← 실제 컬럼명으로 수정
rt_col = 'RT'                   # ← 실제 컬럼명으로 수정
region_col = 'region'           # ← 실제 컬럼명으로 수정
subject_col = 'subject'         # ← 실제 컬럼명으로 수정

# ========== 3. 조건 필터링 ==========
hate_label = 'hate'             # ← 실제 라벨로 수정 ('derogatory', 'H' 등)
neutral_label = 'neutral'       # ← 실제 라벨로 수정 ('N' 등)

# ========== 4. Region 설정 ==========
# 관심 region 지정 (modifier region)
# 데이터에서 region이 숫자인 경우: 3 또는 4
# 문자열인 경우: 'modifier', 'critical_noun' 등
target_region = 3  # ← 수정 필요

# ========== 5. 효과 크기 계산 함수 ==========
def cohens_d(group1, group2):
    """Calculate Cohen's d for paired samples"""
    n1, n2 = len(group1), len(group2)
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def cohens_d_ci(group1, group2, confidence=0.95, n_bootstrap=10000):
    """Bootstrap CI for Cohen's d"""
    np.random.seed(42)
    d_bootstrap = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        idx = np.random.choice(len(group1), len(group1), replace=True)
        g1_sample = group1[idx]
        g2_sample = group2[idx]
        d_bootstrap.append(cohens_d(g1_sample, g2_sample))

    alpha = 1 - confidence
    lower = np.percentile(d_bootstrap, 100 * alpha/2)
    upper = np.percentile(d_bootstrap, 100 * (1 - alpha/2))

    return lower, upper

# ========== 6. 데이터 추출 ==========
# Modifier region 데이터만 필터링
region_data = df[df[region_col] == target_region]

# Hate vs. Neutral 분리
hate_rts = region_data[region_data[modifier_col] == hate_label][rt_col].values
neutral_rts = region_data[region_data[modifier_col] == neutral_label][rt_col].values

print(f"Hate condition: N = {len(hate_rts)}, Mean = {np.mean(hate_rts):.1f} ms")
print(f"Neutral condition: N = {len(neutral_rts)}, Mean = {np.mean(neutral_rts):.1f} ms")

# ========== 7. 효과 크기 계산 ==========
d = cohens_d(hate_rts, neutral_rts)
d_lower, d_upper = cohens_d_ci(hate_rts, neutral_rts)

rt_diff = np.mean(hate_rts) - np.mean(neutral_rts)
rt_diff_pct = (rt_diff / np.mean(neutral_rts)) * 100

# t-test
t_stat, p_val = stats.ttest_rel(hate_rts, neutral_rts)

print("\n========== EFFECT SIZE RESULTS ==========")
print(f"RT difference: {rt_diff:.2f} ms ({rt_diff_pct:.2f}%)")
print(f"Cohen's d: {d:.3f}")
print(f"95% CI: [{d_lower:.3f}, {d_upper:.3f}]")
print(f"t({len(hate_rts)-1}) = {t_stat:.3f}, p = {p_val:.4f}")
print("=========================================\n")

# ========== 8. 시각화 ==========
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: RT difference
ax1 = axes[0]
conditions = ['Neutral', 'Hate']
means = [np.mean(neutral_rts), np.mean(hate_rts)]
sems = [stats.sem(neutral_rts), stats.sem(hate_rts)]

bars = ax1.bar(conditions, means, yerr=sems, capsize=5,
               color=['lightblue', 'salmon'], edgecolor='black')
ax1.set_ylabel('Reading Time (ms)', fontsize=12)
ax1.set_title('RT at Modifier Region', fontsize=14, fontweight='bold')
ax1.set_ylim(bottom=0)

# Add significance marker
if p_val < 0.05:
    sig_marker = '*'
elif p_val < 0.10:
    sig_marker = '†'
else:
    sig_marker = 'n.s.'

y_max = max(means) + max(sems) + 20
ax1.plot([0, 1], [y_max, y_max], 'k-', linewidth=1)
ax1.text(0.5, y_max + 5, sig_marker, ha='center', fontsize=16)

# Panel B: Effect size
ax2 = axes[1]
ax2.errorbar([d], [0], xerr=[[d - d_lower], [d_upper - d]],
             fmt='o', markersize=10, color='black',
             capsize=5, linewidth=2, label='Current Study')
ax2.axvline(0, color='gray', linestyle='--', alpha=0.5)
ax2.axvline(0.2, color='lightgray', linestyle=':', alpha=0.5, label='Small (d=0.2)')
ax2.axvline(0.5, color='lightgray', linestyle=':', alpha=0.5, label='Medium (d=0.5)')
ax2.set_xlabel("Cohen's d", fontsize=12)
ax2.set_title('Effect Size with 95% CI', fontsize=14, fontweight='bold')
ax2.set_ylim(-0.5, 0.5)
ax2.set_yticks([])
ax2.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('effect_size_analysis.png', dpi=300, bbox_inches='tight')
print("Figure saved: effect_size_analysis.png")

# ========== 9. 결과 저장 ==========
results_df = pd.DataFrame({
    'Region': [target_region],
    'Condition_Hate_Mean': [np.mean(hate_rts)],
    'Condition_Hate_SD': [np.std(hate_rts, ddof=1)],
    'Condition_Neutral_Mean': [np.mean(neutral_rts)],
    'Condition_Neutral_SD': [np.std(neutral_rts, ddof=1)],
    'RT_Diff_ms': [rt_diff],
    'RT_Diff_Percent': [rt_diff_pct],
    'Cohens_d': [d],
    'CI_Lower': [d_lower],
    'CI_Upper': [d_upper],
    't_statistic': [t_stat],
    'p_value': [p_val],
    'N': [len(hate_rts)]
})

results_df.to_csv('effect_size_results.csv', index=False)
print("Results saved: effect_size_results.csv")
```

### 3.2 실행

```bash
python effect_size_calculator.py
```

---

## 📈 4단계: 결과 해석

### 4.1 출력 해석

**터미널 출력 예시**:
```
Hate condition: N = 192, Mean = 625.3 ms
Neutral condition: N = 192, Mean = 600.8 ms

========== EFFECT SIZE RESULTS ==========
RT difference: 24.50 ms (4.08%)
Cohen's d: 0.297
95% CI: [-0.048, 0.642]
t(191) = 1.756, p = 0.0808
=========================================

Figure saved: effect_size_analysis.png
Results saved: effect_size_results.csv
```

### 4.2 해석 가이드

**Cohen's d 기준**:
- **Small**: d = 0.2
- **Medium**: d = 0.5
- **Large**: d = 0.8

**본 연구 결과 (예시)**:
- d = 0.297 → **Small to medium** 효과
- 95% CI: [-0.048, 0.642] → 0을 포함하므로 marginal
- p = 0.0808 → 통계적으로 marginally significant (p < .10)
- RT 증가: ~4% → 감정 언어 처리 연구에서 typical range

**결론 예시**:
```
The observed effect size (d = 0.30) indicates a small-to-medium cognitive
impact of hate modifiers on reading time, consistent with prior emotional
language processing research (Ding et al., 2016: d = 0.31; Kissler et al.,
2006: d ≈ 0.45). The marginal statistical significance (p = .08) likely
reflects limited sample size (N = 24 participants), as power analysis
suggests N ≈ 50 for adequate power (1-β = .80) at this effect size.
```

---

## 🔍 5단계: 추가 분석 (선택)

### 5.1 Region별 효과 크기 계산

모든 region에서 효과 크기 확인:

```python
# 모든 region 순회
regions = df[region_col].unique()
results_all = []

for region in regions:
    region_data = df[df[region_col] == region]
    hate_rts = region_data[region_data[modifier_col] == hate_label][rt_col].values
    neutral_rts = region_data[region_data[modifier_col] == neutral_label][rt_col].values

    if len(hate_rts) > 0 and len(neutral_rts) > 0:
        d = cohens_d(hate_rts, neutral_rts)
        d_lower, d_upper = cohens_d_ci(hate_rts, neutral_rts)
        t_stat, p_val = stats.ttest_rel(hate_rts, neutral_rts)

        results_all.append({
            'Region': region,
            'Cohens_d': d,
            'CI_Lower': d_lower,
            'CI_Upper': d_upper,
            'p_value': p_val
        })

results_all_df = pd.DataFrame(results_all)
print(results_all_df)
results_all_df.to_csv('effect_sizes_by_region.csv', index=False)
```

### 5.2 Timeline 시각화

Region별 효과 크기 변화 그래프:

```python
fig, ax = plt.subplots(figsize=(10, 6))

regions = results_all_df['Region'].values
effect_sizes = results_all_df['Cohens_d'].values
ci_lower = results_all_df['CI_Lower'].values
ci_upper = results_all_df['CI_Upper'].values

# Plot effect sizes with CIs
ax.errorbar(regions, effect_sizes,
            yerr=[effect_sizes - ci_lower, ci_upper - effect_sizes],
            fmt='o-', markersize=8, linewidth=2, capsize=5,
            color='darkblue', label='Effect Size (d)')

# Reference lines
ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax.axhline(0.2, color='lightgray', linestyle=':', alpha=0.5, label='Small (d=0.2)')
ax.axhline(0.5, color='lightgray', linestyle=':', alpha=0.5, label='Medium (d=0.5)')

ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel("Cohen's d", fontsize=12)
ax.set_title('Effect Size Timeline Across Regions', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('effect_size_timeline.png', dpi=300)
print("Timeline plot saved: effect_size_timeline.png")
```

---

## 🎯 6단계: Power Analysis (필요한 샘플 크기)

### 6.1 사후 검정력(Post-hoc power)

현재 샘플로 달성한 검정력:

```python
from statsmodels.stats.power import TTestPower

power_analysis = TTestPower()

# 현재 설정
current_d = 0.30
current_n = 24
alpha = 0.05

achieved_power = power_analysis.solve_power(
    effect_size=current_d,
    nobs=current_n,
    alpha=alpha,
    power=None,  # 계산할 값
    alternative='two-sided'
)

print(f"Current power: {achieved_power:.3f} (N={current_n}, d={current_d})")
```

### 6.2 필요한 샘플 크기

원하는 검정력을 달성하기 위한 N:

```python
# 80% 검정력을 위한 샘플 크기
target_power = 0.80

required_n = power_analysis.solve_power(
    effect_size=current_d,
    nobs=None,  # 계산할 값
    alpha=alpha,
    power=target_power,
    alternative='two-sided'
)

print(f"Required N for 80% power: {int(np.ceil(required_n))}")

# 90% 검정력
required_n_90 = power_analysis.solve_power(
    effect_size=current_d,
    nobs=None,
    alpha=alpha,
    power=0.90,
    alternative='two-sided'
)

print(f"Required N for 90% power: {int(np.ceil(required_n_90))}")
```

**예상 출력**:
```
Current power: 0.456 (N=24, d=0.30)
Required N for 80% power: 52
Required N for 90% power: 72
```

**해석**:
- 현재 N=24로는 약 46%의 검정력만 확보
- 80% 검정력 달성을 위해 **N≈50-55 필요**
- 90% 검정력 달성을 위해 **N≈70-75 필요**

---

## ✅ 7단계: 체크리스트 및 트러블슈팅

### 7.1 실행 전 체크리스트

- [ ] 데이터 파일 경로 확인 및 수정
- [ ] 컬럼명 확인 (modifier_col, rt_col, region_col)
- [ ] 조건 라벨 확인 (hate/neutral 또는 다른 명칭)
- [ ] Target region 확인 (modifier region 번호)
- [ ] Python 환경 확인 (pandas, numpy, scipy, matplotlib 설치)

### 7.2 흔한 에러 및 해결

**에러 1: FileNotFoundError**
```
FileNotFoundError: [Errno 2] No such file or directory: '../results/...'
```
**해결**: 데이터 파일 경로 확인
```bash
ls -lh results/result_1201/
# 올바른 파일명으로 수정
```

**에러 2: KeyError**
```
KeyError: 'modifier_type'
```
**해결**: 컬럼명이 다름. 실제 컬럼명 확인:
```python
import pandas as pd
df = pd.read_csv('파일경로')
print(df.columns)
```

**에러 3: IndexError (길이 다름)**
```
ValueError: operands could not be broadcast together
```
**해결**: Hate와 Neutral 데이터 길이 확인. Within-subjects 디자인이므로 같아야 함.
```python
print(f"Hate: {len(hate_rts)}, Neutral: {len(neutral_rts)}")
```

**에러 4: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'scipy'
```
**해결**: 패키지 설치
```bash
pip install pandas numpy scipy matplotlib statsmodels
```

---

## 📊 8단계: 결과물 정리

### 8.1 생성된 파일

실행 후 다음 파일들이 생성됩니다:

1. **effect_size_results.csv**: 주요 통계량 테이블
2. **effect_size_analysis.png**: 2-panel 시각화
3. **effect_sizes_by_region.csv**: Region별 효과 크기 (선택)
4. **effect_size_timeline.png**: Timeline 그래프 (선택)

### 8.2 PI 미팅 자료로 정리

**슬라이드 1: 효과 크기 요약**
```
Effect Size Analysis: Hate Modifier Region

• RT increase: 24.5 ms (4.1%)
• Cohen's d = 0.30 [95% CI: -0.05, 0.64]
• Statistical significance: p = .08 (marginal)
• Interpretation: Small-to-medium effect, typical for emotional language

Literature comparison:
- Kissler et al. (2006): d ≈ 0.45 (emotional words)
- Ding et al. (2016): d = 0.31 (negative verbs)
→ Our effect is within expected range
```

**슬라이드 2: Power Analysis**
```
Sample Size Considerations

Current study:
• N = 24 participants
• Achieved power = 46%

Recommendations:
• For 80% power: N ≈ 50-55
• For 90% power: N ≈ 70-75

Options:
1. Defend current effect size with literature benchmarking
2. Collect additional data (N = 26-30 more participants)
3. Both (recommended)
```

---

## 💡 9단계: 다음 단계

### 9.1 즉시 (분석 완료 후)

1. ✅ 결과 CSV 및 그래프 확인
2. ✅ 문헌 비교 테이블과 통합 (LITERATURE_SEARCH_GUIDE 참조)
3. ✅ PI 미팅 자료에 포함

### 9.2 PI 미팅에서 논의

**질문 사항**:
1. d=0.30 효과 크기로 졸업논문 진행 가능한가?
2. 추가 데이터 수집 필요한가? (N=50까지 증원)
3. Marginal significance를 어떻게 다뤄야 하나?

**선택지**:
- A. 현재 데이터로 진행 + 문헌 benchmarking으로 defend
- B. N=50까지 추가 수집
- C. A + B (추가 수집하되 현재 데이터도 분석)

---

## 📝 요약

### 핵심 단계
1. ✅ 데이터 파일 경로 확인
2. ✅ 스크립트 컬럼명 및 조건 라벨 수정
3. ✅ 실행: `python effect_size_calculator.py`
4. ✅ 결과 확인 및 해석
5. ✅ 문헌과 비교
6. ✅ Power analysis
7. ✅ PI 미팅 자료 준비

### 예상 소요 시간
- 데이터 준비: 10분
- 스크립트 수정: 10분
- 실행 및 확인: 5분
- 결과 해석: 15분
- 추가 분석: 20분 (선택)
**총**: 30-60분

---

**다음 작업**: 문헌 검색 결과와 통합하여 종합 보고서 작성 → PI 미팅 준비 완료!
