"""
효과 크기 계산 스크립트
목적: 현재 데이터에서 Cohen's d 및 95% CI 계산
작성자: 김진일
날짜: 2025-12-26
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def cohens_d(group1, group2):
    """
    Cohen's d 효과 크기 계산

    Parameters:
    -----------
    group1, group2 : array-like
        비교할 두 그룹의 데이터

    Returns:
    --------
    float : Cohen's d 값
    """
    n1, n2 = len(group1), len(group2)
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)

    # Pooled standard deviation
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))

    # Cohen's d
    d = (np.mean(group1) - np.mean(group2)) / pooled_std

    return d

def cohens_d_ci(group1, group2, confidence=0.95, n_bootstrap=10000):
    """
    Bootstrap을 이용한 Cohen's d의 신뢰구간 계산

    Parameters:
    -----------
    group1, group2 : array-like
    confidence : float
        신뢰수준 (기본값 0.95)
    n_bootstrap : int
        Bootstrap 반복 횟수

    Returns:
    --------
    tuple : (lower_ci, upper_ci)
    """
    d_bootstrap = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        sample1 = np.random.choice(group1, size=len(group1), replace=True)
        sample2 = np.random.choice(group2, size=len(group2), replace=True)

        d_bootstrap.append(cohens_d(sample1, sample2))

    alpha = 1 - confidence
    lower = np.percentile(d_bootstrap, alpha/2 * 100)
    upper = np.percentile(d_bootstrap, (1 - alpha/2) * 100)

    return lower, upper

def analyze_region_effects(data_path):
    """
    Region별 효과 크기 분석

    Parameters:
    -----------
    data_path : str
        데이터 파일 경로

    Returns:
    --------
    DataFrame : 결과 테이블
    """
    # TODO: 실제 데이터 파일 형식에 맞게 수정
    # data = pd.read_csv(data_path)

    # 예시 region 리스트 (실제 데이터에 맞게 수정)
    regions = {
        'R1_Subject': '주어 (탈렌족은)',
        'R2_Modifier': '수식어 (열등한/고립된) ⭐조작',
        'R3_NounPhrase': '명사구 (민족으로)',
        'R4_Adverb': '부사구 (의식을 위해)',
        'R5_Verb': '동사',
        'R6_CriticalNoun': '핵심 명사 ⭐그럴듯함 조작',
        'R7_Spillover1': 'Spillover 1',
        'R8_Final': '문장 종결'
    }

    results = []

    for region_code, region_name in regions.items():
        # TODO: 실제 데이터에서 추출
        # hate_rt = data[data['emotion'] == 'hate'][f'{region_code}_RT']
        # neutral_rt = data[data['emotion'] == 'neutral'][f'{region_code}_RT']

        # 임시 예시 데이터 (실제 데이터로 교체 필요)
        np.random.seed(42)
        hate_rt = np.random.normal(500, 100, 50)  # 예시
        neutral_rt = np.random.normal(480, 95, 50)  # 예시

        # 기술통계
        hate_mean = np.mean(hate_rt)
        hate_sd = np.std(hate_rt, ddof=1)
        neutral_mean = np.mean(neutral_rt)
        neutral_sd = np.std(neutral_rt, ddof=1)

        # 차이
        diff_ms = hate_mean - neutral_mean
        diff_pct = (diff_ms / neutral_mean) * 100

        # 효과 크기
        d = cohens_d(hate_rt, neutral_rt)
        ci_lower, ci_upper = cohens_d_ci(hate_rt, neutral_rt)

        # t-test
        t_stat, p_val = stats.ttest_ind(hate_rt, neutral_rt)

        results.append({
            'Region': region_name,
            'Hate_M': hate_mean,
            'Hate_SD': hate_sd,
            'Neutral_M': neutral_mean,
            'Neutral_SD': neutral_sd,
            'Diff_ms': diff_ms,
            'Diff_%': diff_pct,
            "Cohen's_d": d,
            'CI_lower': ci_lower,
            'CI_upper': ci_upper,
            't': t_stat,
            'p': p_val
        })

    return pd.DataFrame(results)

def visualize_effects(df_results, output_path='effect_size_analysis.png'):
    """
    효과 크기 시각화

    Parameters:
    -----------
    df_results : DataFrame
        analyze_region_effects() 결과
    output_path : str
        저장 경로
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Panel A: RT 차이 (ms)
    ax1 = axes[0]
    x = np.arange(len(df_results))

    bars = ax1.bar(x, df_results['Diff_ms'],
                   color=['red' if 'R2' in r or 'R6' in r else 'steelblue'
                          for r in df_results['Region']],
                   alpha=0.7, edgecolor='black', linewidth=1.2)

    ax1.axhline(0, color='black', linestyle='--', linewidth=1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_results['Region'], rotation=45, ha='right', fontsize=10)
    ax1.set_ylabel('RT Difference (ms)\nHate - Neutral', fontsize=12, fontweight='bold')
    ax1.set_title('A. Reading Time Differences by Region',
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.3, linestyle=':')

    # 값 표시
    for i, (bar, val, pct) in enumerate(zip(bars, df_results['Diff_ms'], df_results['Diff_%'])):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}ms\n({pct:.1f}%)',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=8, fontweight='bold')

    # Panel B: Cohen's d with CI
    ax2 = axes[1]

    colors = ['red' if 'R2' in r or 'R6' in r else 'darkblue'
              for r in df_results['Region']]

    ax2.errorbar(x, df_results["Cohen's_d"],
                 yerr=[df_results["Cohen's_d"] - df_results['CI_lower'],
                       df_results['CI_upper'] - df_results["Cohen's_d"]],
                 fmt='o', markersize=10, capsize=6, capthick=2,
                 color='black', ecolor=colors, elinewidth=2)

    # 효과 크기 기준선
    ax2.axhline(0, color='black', linestyle='-', linewidth=1.2)
    ax2.axhline(0.2, color='gray', linestyle=':', linewidth=1,
                label='Small effect (d=0.2)', alpha=0.6)
    ax2.axhline(0.5, color='gray', linestyle='--', linewidth=1,
                label='Medium effect (d=0.5)', alpha=0.6)
    ax2.axhline(0.8, color='gray', linestyle='-.', linewidth=1,
                label='Large effect (d=0.8)', alpha=0.6)

    # 음수 기준선도 추가
    ax2.axhline(-0.2, color='gray', linestyle=':', linewidth=1, alpha=0.6)
    ax2.axhline(-0.5, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    ax2.axhline(-0.8, color='gray', linestyle='-.', linewidth=1, alpha=0.6)

    ax2.set_xticks(x)
    ax2.set_xticklabels(df_results['Region'], rotation=45, ha='right', fontsize=10)
    ax2.set_ylabel("Cohen's d\n(with 95% CI)", fontsize=12, fontweight='bold')
    ax2.set_title("B. Effect Sizes by Region",
                  fontsize=14, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax2.grid(axis='y', alpha=0.3, linestyle=':')

    # 값 표시
    for i, (d_val, p_val) in enumerate(zip(df_results["Cohen's_d"], df_results['p'])):
        sig_marker = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'
        ax2.text(i, d_val + 0.15, f'd={d_val:.2f}\n{sig_marker}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"그래프 저장 완료: {output_path}")

    return fig

def print_summary(df_results):
    """
    결과 요약 출력

    Parameters:
    -----------
    df_results : DataFrame
    """
    print("\n" + "="*80)
    print("효과 크기 분석 결과 요약".center(80))
    print("="*80 + "\n")

    # 전체 테이블
    print(df_results.to_string(index=False))

    # 핵심 region 강조
    print("\n" + "-"*80)
    print("핵심 Region 결과".center(80))
    print("-"*80 + "\n")

    # R2: Modifier
    r2 = df_results[df_results['Region'].str.contains('수식어')]
    if not r2.empty:
        r2 = r2.iloc[0]
        print(f"【R2: 수식어 Region (조작 지점)】")
        print(f"  Hate 조건:    M = {r2['Hate_M']:.1f} ms (SD = {r2['Hate_SD']:.1f})")
        print(f"  Neutral 조건: M = {r2['Neutral_M']:.1f} ms (SD = {r2['Neutral_SD']:.1f})")
        print(f"  차이:         {r2['Diff_ms']:.1f} ms ({r2['Diff_%']:.2f}%)")
        print(f"  Cohen's d =   {r2['Cohen\'s_d']:.3f} [{r2['CI_lower']:.3f}, {r2['CI_upper']:.3f}]")
        print(f"  t({50*2-2}) =  {r2['t']:.2f}, p = {r2['p']:.4f}")
        print()

    # R6: Critical noun
    r6 = df_results[df_results['Region'].str.contains('핵심 명사')]
    if not r6.empty:
        r6 = r6.iloc[0]
        print(f"【R6: 핵심 명사 Region (그럴듯함 조작 지점)】")
        print(f"  Hate 조건:    M = {r6['Hate_M']:.1f} ms (SD = {r6['Hate_SD']:.1f})")
        print(f"  Neutral 조건: M = {r6['Neutral_M']:.1f} ms (SD = {r6['Neutral_SD']:.1f})")
        print(f"  차이:         {r6['Diff_ms']:.1f} ms ({r6['Diff_%']:.2f}%)")
        print(f"  Cohen's d =   {r6['Cohen\'s_d']:.3f} [{r6['CI_lower']:.3f}, {r6['CI_upper']:.3f}]")
        print(f"  t({50*2-2}) =  {r6['t']:.2f}, p = {r6['p']:.4f}")
        print()

    print("="*80 + "\n")

    # 해석 가이드
    print("【해석 가이드】")
    print("  Cohen's d 기준:")
    print("    - Small effect:  d ≈ 0.2")
    print("    - Medium effect: d ≈ 0.5")
    print("    - Large effect:  d ≈ 0.8")
    print("\n  유의수준:")
    print("    - *   : p < .05")
    print("    - **  : p < .01")
    print("    - *** : p < .001")
    print("    - ns  : p ≥ .05 (non-significant)")
    print("\n" + "="*80 + "\n")

def main():
    """
    메인 실행 함수
    """
    print("효과 크기 계산 시작...\n")

    # TODO: 실제 데이터 경로 입력
    data_path = "../results/result_1201/[실제_파일명].csv"

    # 분석 실행
    df_results = analyze_region_effects(data_path)

    # 결과 저장
    output_csv = "effect_size_results.csv"
    df_results.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"결과 CSV 저장: {output_csv}\n")

    # 시각화
    visualize_effects(df_results, output_path='effect_size_analysis.png')

    # 요약 출력
    print_summary(df_results)

    print("\n분석 완료!")
    print("\n다음 단계:")
    print("  1. 문헌 benchmark와 비교")
    print("  2. Power analysis 실시")
    print("  3. PI 미팅 자료 준비")

if __name__ == "__main__":
    main()

"""
사용 방법:
1. 실제 데이터 파일 경로를 data_path에 입력
2. Region 이름 및 컬럼명을 실제 데이터에 맞게 수정
3. 터미널에서 실행: python effect_size_calculator.py
4. 결과 확인:
   - effect_size_results.csv (테이블)
   - effect_size_analysis.png (그래프)

필요한 패키지:
- pandas
- numpy
- scipy
- matplotlib
- seaborn

설치: pip install pandas numpy scipy matplotlib seaborn
"""
