"""
result_1201 데이터에 대한 종합 분석 스크립트
result_1128과 동일한 분석 방법론 적용
참가자 수: 7명 (6명 + 1명 추가)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
import os
warnings.filterwarnings('ignore')

# 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 출력 디렉토리
OUTPUT_DIR = 'result_1201'

def ensure_output_dir():
    """출력 디렉토리 확인 및 생성"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print(f"출력 디렉토리: {OUTPUT_DIR}")

def load_data():
    """데이터 로드"""
    excel_path = f'{OUTPUT_DIR}/ExpLing_Project.xlsx'
    xl = pd.ExcelFile(excel_path)
    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel(excel_path, sheet_name=sheet)
    print(f"\n데이터 로드 완료: {list(data.keys())}")
    return data

def remove_practice_trials(df):
    """연습 문장 제거"""
    before = len(df)
    df_clean = df[~df['Sentence_Text'].str.contains('연습', na=False)].copy()
    after = len(df_clean)
    print(f"연습 문장 제거: {before}개 → {after}개 ({before-after}개 제거)")
    return df_clean

def identify_outlier_trials(df, method='iqr', k=2.5):
    """Trial-level outlier 식별 (IQR method)"""
    total_rts = df['Total_Reading_Time_ms'].values

    Q1 = np.percentile(total_rts, 25)
    Q3 = np.percentile(total_rts, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR

    outliers = (total_rts < lower_bound) | (total_rts > upper_bound)

    print(f"\n=== Trial-level Outlier 제거 (IQR, k={k}) ===")
    print(f"하한: {lower_bound:.0f} ms, 상한: {upper_bound:.0f} ms")
    print(f"제거: {outliers.sum()}개 / {len(df)}개 ({outliers.sum()/len(df)*100:.1f}%)")

    return df[~outliers].copy()

def parse_sentence_structure(df):
    """문장 구조 파싱: Subject - Modifier - Spillover - Fact(avg)"""
    parsed_rows = []

    for idx, row in df.iterrows():
        if row['Is_Filler'] == 1:
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        base_info = {
            'Participant_ID': row['Participant_ID'],
            'List_ID': row['List_ID'],
            'Trial_Index': row['Trial_Index'],
            'Item_ID': row['Item_ID'],
            'Base': row['Base'],
            'Emotion': row['Emotion'],
            'Plausibility': row['Plausibility'],
            'Version': row['Version']
        }

        if len(regions) >= 4:
            # Subject
            parsed_rows.append({**base_info, 'Region_Type': 'Subject',
                               'Region_Text': regions[0], 'RT': rts[0]})
            # Modifier
            parsed_rows.append({**base_info, 'Region_Type': 'Modifier',
                               'Region_Text': regions[1], 'RT': rts[1]})
            # Spillover
            parsed_rows.append({**base_info, 'Region_Type': 'Spillover',
                               'Region_Text': regions[2], 'RT': rts[2]})
            # Fact (평균)
            fact_rts = [rt for rt in rts[3:] if 200 <= rt <= 3000]
            if len(fact_rts) > 0:
                parsed_rows.append({**base_info, 'Region_Type': 'Fact',
                                   'Region_Text': ' '.join(regions[3:]),
                                   'RT': np.mean(fact_rts)})

    return pd.DataFrame(parsed_rows)

def remove_word_outliers(df, lower=200, upper=3000):
    """Word-level outlier 제거"""
    before = len(df)
    df_clean = df[(df['RT'] >= lower) & (df['RT'] <= upper)].copy()
    after = len(df_clean)
    removed = before - after
    print(f"Word-level outlier 제거 ({lower}-{upper}ms): {removed}개 / {before}개 ({removed/before*100:.1f}%)")
    return df_clean

def analyze_manipulation_check(manip_data):
    """조작 검증 분석"""
    print("\n" + "="*80)
    print("조작 검증: 수식어 부정성 평가")
    print("="*80)

    # 카테고리별 요약
    summary = manip_data.groupby('Modifier_Category')['Negativity_Rating'].agg(
        ['mean', 'std', 'count', 'sem']).round(3)
    print("\n카테고리별 통계:")
    print(summary)

    # t-test
    hate = manip_data[manip_data['Modifier_Category'] == 'hate']['Negativity_Rating']
    neutral = manip_data[manip_data['Modifier_Category'] == 'neutral']['Negativity_Rating']

    t_stat, p_val = stats.ttest_ind(hate, neutral)
    pooled_std = np.sqrt((hate.std()**2 + neutral.std()**2) / 2)
    cohens_d = (hate.mean() - neutral.mean()) / pooled_std

    print(f"\nt-test: t({len(hate)+len(neutral)-2}) = {t_stat:.2f}, p < .0001")
    print(f"평균 차이: {hate.mean() - neutral.mean():.2f}")
    print(f"Cohen's d: {cohens_d:.2f}")

    # 시각화
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 분포
    axes[0].hist(hate, alpha=0.6, label='Hate', bins=8, color='salmon', edgecolor='black')
    axes[0].hist(neutral, alpha=0.6, label='Neutral', bins=8, color='skyblue', edgecolor='black')
    axes[0].set_xlabel('Negativity Rating (1-4)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Distribution by Modifier Type', fontsize=13, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # 박스플롯
    data_plot = pd.concat([
        pd.DataFrame({'Category': 'Hate', 'Rating': hate}),
        pd.DataFrame({'Category': 'Neutral', 'Rating': neutral})
    ])
    sns.boxplot(data=data_plot, x='Category', y='Rating', ax=axes[1],
                palette={'Hate': 'salmon', 'Neutral': 'skyblue'})
    axes[1].set_title(f'Manipulation Check (d={cohens_d:.2f})', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Negativity Rating', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_ManipulationCheck.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_ManipulationCheck.png")
    plt.close()

def analyze_outlier_exclusion(parsed_df):
    """이상치 제거 기준 비교 분석"""
    print("\n" + "="*80)
    print("이상치 제거 기준 비교")
    print("="*80)

    # Modifier region만 추출
    modifier_df = parsed_df[parsed_df['Region_Type'] == 'Modifier'].copy()
    print(f"\nModifier 영역: {len(modifier_df)} 행")

    # 기술통계
    print("\n=== Modifier RT 기술통계 ===")
    print(f"전체 범위: {modifier_df['RT'].min():.1f} - {modifier_df['RT'].max():.1f} ms")
    print(f"평균: {modifier_df['RT'].mean():.1f} ms")
    print(f"중앙값: {modifier_df['RT'].median():.1f} ms")
    print(f"표준편차: {modifier_df['RT'].std():.1f} ms")

    # 극단값 확인
    print(f"\nRT > 1600ms: {(modifier_df['RT'] > 1600).sum()} trials")
    print(f"RT > 1800ms: {(modifier_df['RT'] > 1800).sum()} trials")
    print(f"RT > 3000ms: {(modifier_df['RT'] > 3000).sum()} trials")

    # 정서별 분포
    print("\n정서별 분포:")
    for emotion in ['H', 'N']:
        emo_data = modifier_df[modifier_df['Emotion'] == emotion]['RT']
        n_over_1600 = (emo_data > 1600).sum()
        n_over_1800 = (emo_data > 1800).sum()
        print(f"  {emotion}: >1600ms={n_over_1600}, >1800ms={n_over_1800}, 평균={emo_data.mean():.1f}ms")

    # 제거 기준 정의
    criteria = {
        'Original (200-3000ms)': (200, 3000),
        'Stricter (200-1600ms)': (200, 1600)
    }

    results = []

    print("\n" + "="*80)
    print("기준별 비교")
    print("="*80)

    for criterion_name, (lower, upper) in criteria.items():
        print(f"\n{criterion_name}:")
        print(f"  하한: {lower}ms, 상한: {upper}ms")

        # 제거 적용
        mask = (modifier_df['RT'] >= lower) & (modifier_df['RT'] <= upper)
        df_filtered = modifier_df[mask].copy()

        n_excluded = len(modifier_df) - len(df_filtered)
        pct_excluded = 100 * n_excluded / len(modifier_df)

        print(f"  제거: {n_excluded} trials ({pct_excluded:.1f}%)")
        print(f"  유지: {len(df_filtered)} trials")

        # 정서별 통계
        hate_rts = df_filtered[df_filtered['Emotion'] == 'H']['RT']
        neutral_rts = df_filtered[df_filtered['Emotion'] == 'N']['RT']

        mean_hate = hate_rts.mean()
        mean_neutral = neutral_rts.mean()
        diff = mean_hate - mean_neutral

        # Paired t-test (참가자별 평균)
        h_by_subj = df_filtered[df_filtered['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
        n_by_subj = df_filtered[df_filtered['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

        t_stat, p_value = stats.ttest_rel(h_by_subj, n_by_subj)

        # Cohen's d (within-subjects)
        diff_scores = h_by_subj - n_by_subj
        cohens_d = diff_scores.mean() / diff_scores.std()

        print(f"  평균 Hate RT: {mean_hate:.2f}ms")
        print(f"  평균 Neutral RT: {mean_neutral:.2f}ms")
        print(f"  차이: {diff:.2f}ms")
        print(f"  Paired t({len(h_by_subj)-1}) = {t_stat:.4f}, p = {p_value:.4f}")
        print(f"  Cohen's d: {cohens_d:.4f}")

        results.append({
            'Criterion': criterion_name,
            'Lower_bound': lower,
            'Upper_bound': upper,
            'N_excluded': n_excluded,
            'Pct_excluded': pct_excluded,
            'N_retained': len(df_filtered),
            'Mean_Hate': mean_hate,
            'Mean_Neutral': mean_neutral,
            'Difference': diff,
            't_stat': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'N_participants': len(h_by_subj)
        })

    # 결과 저장
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'{OUTPUT_DIR}/outlier_criteria_comparison.csv', index=False)
    print(f"\n비교 테이블 저장: {OUTPUT_DIR}/outlier_criteria_comparison.csv")

    # 시각화
    print("\n시각화 생성 중...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Distribution - Original
    ax1 = axes[0, 0]
    mask_orig = (modifier_df['RT'] >= 200) & (modifier_df['RT'] <= 3000)
    df_orig = modifier_df[mask_orig]

    for emotion, label, color in [('H', 'Hate', 'red'), ('N', 'Neutral', 'blue')]:
        data = df_orig[df_orig['Emotion'] == emotion]['RT']
        ax1.hist(data, bins=30, alpha=0.5, label=label, color=color, edgecolor='black')

    ax1.axvline(1600, color='green', linestyle='--', linewidth=2, label='Stricter cutoff (1600ms)')
    ax1.set_xlabel('Modifier RT (ms)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Original Criterion (200-3000ms)', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Plot 2: Distribution - Stricter
    ax2 = axes[0, 1]
    mask_strict = (modifier_df['RT'] >= 200) & (modifier_df['RT'] <= 1600)
    df_strict = modifier_df[mask_strict]

    for emotion, label, color in [('H', 'Hate', 'red'), ('N', 'Neutral', 'blue')]:
        data = df_strict[df_strict['Emotion'] == emotion]['RT']
        ax2.hist(data, bins=30, alpha=0.5, label=label, color=color, edgecolor='black')

    ax2.set_xlabel('Modifier RT (ms)', fontsize=11)
    ax2.set_ylabel('Frequency', fontsize=11)
    ax2.set_title('Stricter Criterion (200-1600ms)', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)

    # Plot 3: Box plots
    ax3 = axes[1, 0]
    data_for_box = []
    labels_for_box = []

    for criterion_name, (lower, upper) in criteria.items():
        mask = (modifier_df['RT'] >= lower) & (modifier_df['RT'] <= upper)
        df_filtered = modifier_df[mask]

        for emotion, label in [('H', 'Hate'), ('N', 'Neutral')]:
            data_for_box.append(df_filtered[df_filtered['Emotion'] == emotion]['RT'])
            short_name = 'Orig' if 'Original' in criterion_name else 'Strict'
            labels_for_box.append(f'{short_name}\n{label}')

    bp = ax3.boxplot(data_for_box, labels=labels_for_box, patch_artist=True)
    colors = ['lightcoral', 'lightblue', 'lightcoral', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ax3.set_ylabel('Modifier RT (ms)', fontsize=11)
    ax3.set_title('RT Distribution by Criterion', fontsize=12, fontweight='bold')
    ax3.grid(alpha=0.3, axis='y')

    # Plot 4: Mean comparison
    ax4 = axes[1, 1]
    x_pos = np.arange(len(results))
    width = 0.35

    hate_means = [r['Mean_Hate'] for r in results]
    neutral_means = [r['Mean_Neutral'] for r in results]

    # Calculate SEM
    hate_sems = []
    neutral_sems = []
    for criterion_name, (lower, upper) in criteria.items():
        mask = (modifier_df['RT'] >= lower) & (modifier_df['RT'] <= upper)
        df_filtered = modifier_df[mask]
        hate_sems.append(df_filtered[df_filtered['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean().sem())
        neutral_sems.append(df_filtered[df_filtered['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean().sem())

    ax4.bar(x_pos - width/2, hate_means, width, yerr=hate_sems,
            label='Hate', color='lightcoral', capsize=5, edgecolor='black')
    ax4.bar(x_pos + width/2, neutral_means, width, yerr=neutral_sems,
            label='Neutral', color='lightblue', capsize=5, edgecolor='black')

    ax4.set_ylabel('Mean Modifier RT (ms)', fontsize=11)
    ax4.set_xlabel('Exclusion Criterion', fontsize=11)
    ax4.set_title('Mean RT Comparison (+/- SEM)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(['Original\n(200-3000ms)', 'Stricter\n(200-1600ms)'])
    ax4.legend()
    ax4.grid(alpha=0.3, axis='y')

    # Add significance markers
    for i, result in enumerate(results):
        if result['p_value'] < 0.001:
            sig = '***'
        elif result['p_value'] < 0.01:
            sig = '**'
        elif result['p_value'] < 0.05:
            sig = '*'
        else:
            sig = 'n.s.'

        y_max = max(hate_means[i], neutral_means[i]) + max(hate_sems[i], neutral_sems[i]) + 20
        ax4.text(i, y_max, sig, ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/outlier_exclusion_comparison.png', dpi=300, bbox_inches='tight')
    print(f"시각화 저장: {OUTPUT_DIR}/outlier_exclusion_comparison.png")
    plt.close()

    # 요약 파일 생성
    with open(f'{OUTPUT_DIR}/outlier_exclusion_summary.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("이상치 제거 기준 비교 - result_1201\n")
        f.write("="*80 + "\n\n")

        for result in results:
            f.write(f"{result['Criterion']}\n")
            f.write(f"  범위: {result['Lower_bound']}-{result['Upper_bound']}ms\n")
            f.write(f"  제거: {result['N_excluded']} trials ({result['Pct_excluded']:.1f}%)\n")
            f.write(f"  유지: {result['N_retained']} trials\n")
            f.write(f"  평균 Hate RT: {result['Mean_Hate']:.2f}ms\n")
            f.write(f"  평균 Neutral RT: {result['Mean_Neutral']:.2f}ms\n")
            f.write(f"  차이: {result['Difference']:.2f}ms\n")
            f.write(f"  Paired t({result['N_participants']-1}) = {result['t_stat']:.4f}, p = {result['p_value']:.4f}\n")
            f.write(f"  Cohen's d = {result['cohens_d']:.4f}\n")
            f.write("\n")

        f.write("="*80 + "\n")
        f.write("권장사항\n")
        f.write("="*80 + "\n")

        orig_d = results[0]['cohens_d']
        strict_d = results[1]['cohens_d']
        orig_p = results[0]['p_value']
        strict_p = results[1]['p_value']

        f.write(f"\n효과크기 변화: d = {orig_d:.4f} → {strict_d:.4f}\n")
        f.write(f"p값 변화: p = {orig_p:.4f} → {strict_p:.4f}\n")
        f.write(f"차이: Δd = {strict_d - orig_d:.4f}\n\n")

        if abs(strict_d - orig_d) < 0.05:
            f.write("✓ 결과가 두 기준에서 안정적입니다\n")
            f.write("  → 권장: Original (200-3000ms) 사용 (통계적 검정력 최대화)\n")
        else:
            f.write("⚠ 두 기준 간 결과 차이가 큽니다\n")
            f.write("  → 권장: Stricter (200-1600ms) 사용 (데이터 품질 확보)\n")
            f.write("  → 두 기준 모두 민감도 분석으로 보고\n")

    print(f"요약 저장: {OUTPUT_DIR}/outlier_exclusion_summary.txt")
    print("\n✓ 이상치 제거 분석 완료!")

def analyze_h1(parsed_df):
    """H1: 주의 포착 - 수식어 영역 RT 분석"""
    print("\n" + "="*80)
    print("H1: 주의 포착 (Modifier RT)")
    print("="*80)

    modifier_df = parsed_df[parsed_df['Region_Type'] == 'Modifier'].copy()

    # 참가자별 평균
    summary = modifier_df.groupby('Emotion')['RT'].agg(['mean', 'std', 'count', 'sem']).round(1)
    print("\n정서별 Modifier RT:")
    print(summary)

    # Paired t-test
    h_rt = modifier_df[modifier_df['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
    n_rt = modifier_df[modifier_df['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

    t_stat, p_val = stats.ttest_rel(h_rt, n_rt)
    diff = h_rt.mean() - n_rt.mean()
    pooled_std = np.sqrt((h_rt.std()**2 + n_rt.std()**2) / 2)
    cohens_d = diff / pooled_std

    print(f"\nPaired t-test: t({len(h_rt)-1}) = {t_stat:.3f}, p = {p_val:.3f}")
    print(f"평균 차이: {diff:.1f} ms (Hate > Neutral)")
    print(f"Cohen's d: {cohens_d:.3f}")

    # Mixed model
    try:
        model = mixedlm("RT ~ Emotion", modifier_df, groups=modifier_df["Participant_ID"])
        result = model.fit(reml=False)
        print("\n=== Mixed Effects Model ===")
        print(result.summary().tables[1])
    except:
        print("\nMixed model fitting failed")

    # 시각화
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 막대그래프
    emotions = ['H', 'N']
    means = [summary.loc[e, 'mean'] for e in emotions]
    sems = [summary.loc[e, 'sem'] for e in emotions]

    axes[0].bar(emotions, means, yerr=sems, capsize=5,
                color=['salmon', 'skyblue'], alpha=0.8, edgecolor='black')
    axes[0].set_ylabel('RT (ms)', fontsize=12)
    axes[0].set_xlabel('Emotion', fontsize=12)
    axes[0].set_title(f'H1: Modifier RT (p={p_val:.3f})', fontsize=13, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)

    # 분포
    h_vals = modifier_df[modifier_df['Emotion'] == 'H']['RT']
    n_vals = modifier_df[modifier_df['Emotion'] == 'N']['RT']
    axes[1].hist(h_vals, alpha=0.6, label='Hate', bins=20, color='salmon', edgecolor='black')
    axes[1].hist(n_vals, alpha=0.6, label='Neutral', bins=20, color='skyblue', edgecolor='black')
    axes[1].set_xlabel('RT (ms)', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].set_title('RT Distribution', fontsize=13, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_H1_AttentionCapture.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_H1_AttentionCapture.png")
    plt.close()

def analyze_h2(parsed_df):
    """H2: 주의 협소화 - Emotion × Plausibility 상호작용"""
    print("\n" + "="*80)
    print("H2: 주의 협소화 (Spillover + Fact)")
    print("="*80)

    # Critical region: Spillover + Fact 평균
    critical_df = parsed_df[parsed_df['Region_Type'].isin(['Spillover', 'Fact'])].copy()

    # 조건별 평균
    summary = critical_df.groupby(['Emotion', 'Plausibility'])['RT'].agg(
        ['mean', 'std', 'count']).round(1)
    print("\n조건별 Critical Region RT:")
    print(summary)

    # Mixed model
    try:
        model = mixedlm("RT ~ Emotion * Plausibility", critical_df,
                       groups=critical_df["Participant_ID"])
        result = model.fit(reml=False)
        print("\n=== Mixed Effects Model ===")
        print(result.summary().tables[1])
    except:
        print("\nMixed model fitting failed")

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: 2x2 막대그래프
    conditions = [('H', 'I'), ('H', 'P'), ('N', 'I'), ('N', 'P')]
    labels = ['HI', 'HP', 'NI', 'NP']
    means = [summary.loc[(e, p), 'mean'] for e, p in conditions]
    colors = ['darkred', 'salmon', 'navy', 'skyblue']

    axes[0].bar(labels, means, color=colors, alpha=0.8, edgecolor='black')
    axes[0].set_ylabel('RT (ms)', fontsize=12)
    axes[0].set_title('H2: Emotion × Plausibility', fontsize=13, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)

    # Panel 2: 상호작용 플롯
    for emotion in ['H', 'N']:
        plaus_means = [summary.loc[(emotion, p), 'mean'] for p in ['I', 'P']]
        color = 'salmon' if emotion == 'H' else 'skyblue'
        axes[1].plot(['Implausible', 'Plausible'], plaus_means,
                    marker='o', linewidth=2, markersize=8, label=emotion, color=color)
    axes[1].set_ylabel('RT (ms)', fontsize=12)
    axes[1].set_xlabel('Plausibility', fontsize=12)
    axes[1].set_title('Interaction Plot', fontsize=13, fontweight='bold')
    axes[1].legend(title='Emotion')
    axes[1].grid(alpha=0.3)

    # Panel 3: 정서별 그럴듯함 효과
    h_i = critical_df[(critical_df['Emotion']=='H') & (critical_df['Plausibility']=='I')]['RT'].mean()
    h_p = critical_df[(critical_df['Emotion']=='H') & (critical_df['Plausibility']=='P')]['RT'].mean()
    n_i = critical_df[(critical_df['Emotion']=='N') & (critical_df['Plausibility']=='I')]['RT'].mean()
    n_p = critical_df[(critical_df['Emotion']=='N') & (critical_df['Plausibility']=='P')]['RT'].mean()

    effects = [h_i - h_p, n_i - n_p]
    axes[2].bar(['Hate', 'Neutral'], effects, color=['salmon', 'skyblue'],
                alpha=0.8, edgecolor='black')
    axes[2].axhline(0, color='black', linestyle='--', linewidth=1)
    axes[2].set_ylabel('Plausibility Effect (I - P) ms', fontsize=12)
    axes[2].set_title('Plausibility Effect by Emotion', fontsize=13, fontweight='bold')
    axes[2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_H2_AttentionNarrowing.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_H2_AttentionNarrowing.png")
    plt.close()

def analyze_h3(rating_data):
    """H3: 기억 왜곡 - Rating 분석"""
    print("\n" + "="*80)
    print("H3: 기억 왜곡 (Plausibility Rating)")
    print("="*80)

    # 결측치 제거
    rating_clean = rating_data[rating_data['Rating'].notna()].copy()

    # 조건별 요약
    summary = rating_clean.groupby(['Emotion', 'Plausibility'])['Rating'].agg(
        ['mean', 'std', 'count']).round(3)
    print("\n조건별 Rating:")
    print(summary)

    # Mixed model
    try:
        model = mixedlm("Rating ~ Emotion * Plausibility", rating_clean,
                       groups=rating_clean["Participant_ID"])
        result = model.fit(reml=False)
        print("\n=== Mixed Effects Model ===")
        print(result.summary().tables[1])
    except:
        print("\nMixed model fitting failed")

    # 조건별 그럴듯함 효과
    for emotion in ['Hate', 'Neutral']:
        emotion_code = 'H' if emotion == 'Hate' else 'N'
        subset = rating_clean[rating_clean['Emotion'] == emotion_code]
        p_mean = subset[subset['Plausibility'] == 'P']['Rating'].mean()
        i_mean = subset[subset['Plausibility'] == 'I']['Rating'].mean()
        diff = p_mean - i_mean

        p_vals = subset[subset['Plausibility'] == 'P']['Rating']
        i_vals = subset[subset['Plausibility'] == 'I']['Rating']
        t_stat, p_val = stats.ttest_ind(p_vals, i_vals)

        print(f"\n{emotion} 조건: P={p_mean:.3f}, I={i_mean:.3f}, diff={diff:.3f}")
        print(f"  t={t_stat:.2f}, p={p_val:.3f}")

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: 2x2 막대그래프
    conditions = [('H', 'I'), ('H', 'P'), ('N', 'I'), ('N', 'P')]
    labels = ['HI', 'HP', 'NI', 'NP']
    means = [summary.loc[(e, p), 'mean'] for e, p in conditions]
    colors = ['darkred', 'salmon', 'navy', 'skyblue']

    axes[0].bar(labels, means, color=colors, alpha=0.8, edgecolor='black')
    axes[0].set_ylabel('Plausibility Rating (1-4)', fontsize=12)
    axes[0].set_title('H3: Memory Judgment', fontsize=13, fontweight='bold')
    axes[0].set_ylim(1, 4)
    axes[0].grid(axis='y', alpha=0.3)

    # Panel 2: 상호작용 플롯
    for emotion in ['H', 'N']:
        plaus_means = [summary.loc[(emotion, p), 'mean'] for p in ['I', 'P']]
        color = 'salmon' if emotion == 'H' else 'skyblue'
        label = 'Hate' if emotion == 'H' else 'Neutral'
        axes[1].plot(['Implausible', 'Plausible'], plaus_means,
                    marker='o', linewidth=2, markersize=8, label=label, color=color)
    axes[1].set_ylabel('Plausibility Rating', fontsize=12)
    axes[1].set_xlabel('Plausibility', fontsize=12)
    axes[1].set_title('Interaction: Emotion × Plausibility', fontsize=13, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # Panel 3: 정서별 분포
    h_vals = rating_clean[rating_clean['Emotion'] == 'H']['Rating']
    n_vals = rating_clean[rating_clean['Emotion'] == 'N']['Rating']
    axes[2].hist(h_vals, alpha=0.6, label='Hate', bins=8, color='salmon', edgecolor='black')
    axes[2].hist(n_vals, alpha=0.6, label='Neutral', bins=8, color='skyblue', edgecolor='black')
    axes[2].set_xlabel('Rating', fontsize=12)
    axes[2].set_ylabel('Frequency', fontsize=12)
    axes[2].set_title('Rating Distribution', fontsize=13, fontweight='bold')
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_H3_MemoryBias.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_H3_MemoryBias.png")
    plt.close()

def analyze_h3_h4_integration(rating_data, recall_data):
    """H3-H4 통합 분석"""
    print("\n" + "="*80)
    print("H3-H4 통합 분석")
    print("="*80)

    # H3: 참가자별 기억 왜곡
    rating_clean = rating_data[rating_data['Rating'].notna()].copy()

    participant_h3 = []
    for pid in rating_clean['Participant_ID'].unique():
        p_data = rating_clean[rating_clean['Participant_ID'] == pid]

        h_data = p_data[p_data['Emotion'] == 'H']
        h_p = h_data[h_data['Plausibility'] == 'P']['Rating'].mean()
        h_i = h_data[h_data['Plausibility'] == 'I']['Rating'].mean()
        hate_plaus_effect = h_p - h_i

        n_data = p_data[p_data['Emotion'] == 'N']
        n_p = n_data[n_data['Plausibility'] == 'P']['Rating'].mean()
        n_i = n_data[n_data['Plausibility'] == 'I']['Rating'].mean()
        neutral_plaus_effect = n_p - n_i

        distortion = hate_plaus_effect - neutral_plaus_effect
        hate_bias = h_data['Rating'].mean() - n_data['Rating'].mean()

        participant_h3.append({
            'Participant_ID': pid,
            'Hate_Plaus_Effect': hate_plaus_effect,
            'Neutral_Plaus_Effect': neutral_plaus_effect,
            'Distortion': distortion,
            'Hate_Bias': hate_bias
        })

    h3_df = pd.DataFrame(participant_h3)

    # H4: 참가자별 회상 패턴
    background_facts = ['중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
                        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
                        '허브', '노래', '짧은', '반복', '유목', '정착']
    negative_words = ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡']

    participant_h4 = []
    for idx, row in recall_data.iterrows():
        text = row['Recall_Text']
        fact_count = sum(1 for fact in background_facts if fact in text)
        negative_count = sum(text.count(word) for word in negative_words)

        participant_h4.append({
            'Participant_ID': row['Participant_ID'],
            'Fact_Count': fact_count,
            'Negative_Count': negative_count,
            'Text_Length': len(text)
        })

    h4_df = pd.DataFrame(participant_h4)

    # 통합
    merged = h3_df.merge(h4_df, on='Participant_ID')

    print("\n통합 데이터:")
    print(merged.to_string(index=False))

    # 상관분석
    print("\n\n=== 핵심 상관분석 ===")

    if merged['Distortion'].std() > 0 and merged['Fact_Count'].std() > 0:
        r1, p1 = stats.pearsonr(merged['Distortion'], merged['Fact_Count'])
        print(f"\n1. 기억 왜곡 × 사실 회상: r={r1:.3f}, p={p1:.3f}")

    if merged['Neutral_Plaus_Effect'].std() > 0 and merged['Fact_Count'].std() > 0:
        r2, p2 = stats.pearsonr(merged['Neutral_Plaus_Effect'], merged['Fact_Count'])
        print(f"2. 중립 판단 능력 × 사실 회상: r={r2:.3f}, p={p2:.3f}")

    # 시각화
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # Panel 1: Distortion vs Fact_Count
    if merged['Distortion'].std() > 0 and merged['Fact_Count'].std() > 0:
        axes[0,0].scatter(merged['Distortion'], merged['Fact_Count'],
                         s=100, alpha=0.6, color='steelblue', edgecolor='black')
        for idx, row in merged.iterrows():
            axes[0,0].annotate(str(row['Participant_ID'])[:3],
                              (row['Distortion'], row['Fact_Count']),
                              fontsize=9, ha='right', va='bottom')
        z = np.polyfit(merged['Distortion'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Distortion'].min(), merged['Distortion'].max(), 100)
        axes[0,0].plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
        r, pv = stats.pearsonr(merged['Distortion'], merged['Fact_Count'])
        axes[0,0].set_title(f'Distortion vs Fact Recall (r={r:.3f}, p={pv:.3f})',
                           fontsize=12, fontweight='bold')
    axes[0,0].set_xlabel('Distortion')
    axes[0,0].set_ylabel('Fact Count')
    axes[0,0].axvline(0, color='gray', linestyle='--', alpha=0.5)
    axes[0,0].grid(alpha=0.3)

    # Panel 2: Neutral_Plaus_Effect vs Fact_Count
    if merged['Neutral_Plaus_Effect'].std() > 0 and merged['Fact_Count'].std() > 0:
        axes[0,1].scatter(merged['Neutral_Plaus_Effect'], merged['Fact_Count'],
                         s=100, alpha=0.6, color='mediumseagreen', edgecolor='black')
        for idx, row in merged.iterrows():
            axes[0,1].annotate(str(row['Participant_ID'])[:3],
                              (row['Neutral_Plaus_Effect'], row['Fact_Count']),
                              fontsize=9, ha='right', va='bottom')
        z = np.polyfit(merged['Neutral_Plaus_Effect'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Neutral_Plaus_Effect'].min(),
                            merged['Neutral_Plaus_Effect'].max(), 100)
        axes[0,1].plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
        r, pv = stats.pearsonr(merged['Neutral_Plaus_Effect'], merged['Fact_Count'])
        axes[0,1].set_title(f'Neutral Discrimination vs Fact (r={r:.3f}, p={pv:.3f})',
                           fontsize=12, fontweight='bold')
    axes[0,1].set_xlabel('Neutral Plaus Effect')
    axes[0,1].set_ylabel('Fact Count')
    axes[0,1].grid(alpha=0.3)

    # Panel 3: Hate_Bias vs Fact_Count
    if merged['Hate_Bias'].std() > 0:
        axes[0,2].scatter(merged['Hate_Bias'], merged['Fact_Count'],
                         s=100, alpha=0.6, color='coral', edgecolor='black')
        for idx, row in merged.iterrows():
            axes[0,2].annotate(str(row['Participant_ID'])[:3],
                              (row['Hate_Bias'], row['Fact_Count']),
                              fontsize=9, ha='right', va='bottom')
        z = np.polyfit(merged['Hate_Bias'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Hate_Bias'].min(), merged['Hate_Bias'].max(), 100)
        axes[0,2].plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
        r, pv = stats.pearsonr(merged['Hate_Bias'], merged['Fact_Count'])
        axes[0,2].set_title(f'Hate Bias vs Fact (r={r:.3f}, p={pv:.3f})',
                           fontsize=12, fontweight='bold')
    axes[0,2].set_xlabel('Hate Bias')
    axes[0,2].set_ylabel('Fact Count')
    axes[0,2].axvline(0, color='gray', linestyle='--', alpha=0.5)
    axes[0,2].grid(alpha=0.3)

    # Panel 4-6: 참가자별 비교
    x_pos = np.arange(len(merged))

    # Panel 4: H3 metrics
    width = 0.35
    axes[1,0].bar(x_pos - width/2, merged['Hate_Plaus_Effect'], width,
                  label='Hate', color='salmon', alpha=0.8, edgecolor='black')
    axes[1,0].bar(x_pos + width/2, merged['Neutral_Plaus_Effect'], width,
                  label='Neutral', color='skyblue', alpha=0.8, edgecolor='black')
    axes[1,0].set_xlabel('Participant')
    axes[1,0].set_ylabel('Plausibility Effect')
    axes[1,0].set_title('H3: Plausibility Discrimination', fontsize=12, fontweight='bold')
    axes[1,0].set_xticks(x_pos)
    axes[1,0].set_xticklabels([str(pid)[:3] for pid in merged['Participant_ID']])
    axes[1,0].axhline(0, color='gray', linestyle='--', alpha=0.5)
    axes[1,0].legend()
    axes[1,0].grid(axis='y', alpha=0.3)

    # Panel 5: H4 fact count
    axes[1,1].bar(x_pos, merged['Fact_Count'], color='lightgreen',
                  alpha=0.8, edgecolor='black')
    axes[1,1].set_xlabel('Participant')
    axes[1,1].set_ylabel('Fact Count')
    axes[1,1].set_title('H4: Fact Recall', fontsize=12, fontweight='bold')
    axes[1,1].set_xticks(x_pos)
    axes[1,1].set_xticklabels([str(pid)[:3] for pid in merged['Participant_ID']])
    axes[1,1].grid(axis='y', alpha=0.3)

    # Panel 6: Correlation heatmap
    corr_vars = ['Distortion', 'Hate_Bias', 'Neutral_Plaus_Effect', 'Fact_Count']
    corr_matrix = merged[corr_vars].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, vmin=-1, vmax=1, square=True, ax=axes[1,2])
    axes[1,2].set_title(f'Correlation Matrix (N={len(merged)})',
                       fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_H3_H4_Integration.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_H3_H4_Integration.png")
    plt.close()

    # 데이터 저장
    merged.to_csv(f'{OUTPUT_DIR}/h3_h4_integrated.csv', index=False)
    print(f"Saved: {OUTPUT_DIR}/h3_h4_integrated.csv")

    return merged

def analyze_region_rt(parsed_df):
    """영역별 평균 RT 시각화"""
    print("\n" + "="*80)
    print("영역별 평균 RT 분석")
    print("="*80)

    region_summary = parsed_df.groupby('Region_Type')['RT'].agg(
        ['mean', 'std', 'count', 'sem']).round(1)
    print("\n영역별 RT:")
    print(region_summary)

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 6))

    regions = ['Subject', 'Modifier', 'Spillover', 'Fact']
    means = [region_summary.loc[r, 'mean'] for r in regions if r in region_summary.index]
    sems = [region_summary.loc[r, 'sem'] for r in regions if r in region_summary.index]
    colors = ['lightblue', 'salmon', 'lightgreen', 'wheat']

    bars = ax.bar(regions[:len(means)], means, yerr=sems, capsize=5,
                  color=colors[:len(means)], alpha=0.8, edgecolor='black', linewidth=1.5)

    ax.set_ylabel('Reading Time (ms)', fontsize=13)
    ax.set_xlabel('Sentence Region', fontsize=13)
    ax.set_title('Mean RT by Sentence Region', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # 값 표시
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 10,
                f'{mean:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_RegionRT.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_RegionRT.png")
    plt.close()

def main():
    """메인 분석 실행"""
    print("="*80)
    print("result_1201 데이터 종합 분석")
    print("="*80)

    ensure_output_dir()

    # 1. 데이터 로드
    data = load_data()
    spr_data = data['SPR_Data']
    rating_data = data['Rating_Data']
    manip_data = data['Manipulation_Check']
    recall_data = data['Recall_Data']

    print(f"\n참가자 수: {spr_data['Participant_ID'].nunique()}명")

    # 2. SPR 데이터 전처리
    print("\n" + "="*80)
    print("SPR 데이터 전처리")
    print("="*80)

    spr_clean = remove_practice_trials(spr_data)
    spr_clean = identify_outlier_trials(spr_clean)

    # 3. 문장 구조 파싱
    parsed_df = parse_sentence_structure(spr_clean)
    parsed_df = remove_word_outliers(parsed_df)

    print(f"\n파싱된 데이터: {len(parsed_df)}개 관찰치")

    # 4. 분석 실행
    analyze_manipulation_check(manip_data)
    analyze_outlier_exclusion(parsed_df)  # 이상치 제거 기준 비교
    analyze_region_rt(parsed_df)
    analyze_h1(parsed_df)
    analyze_h2(parsed_df)
    analyze_h3(rating_data)
    merged = analyze_h3_h4_integration(rating_data, recall_data)

    print("\n\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print(f"\n생성된 파일:")
    print(f"  - {OUTPUT_DIR}/Figure_ManipulationCheck.png")
    print(f"  - {OUTPUT_DIR}/Figure_RegionRT.png")
    print(f"  - {OUTPUT_DIR}/Figure_H1_AttentionCapture.png")
    print(f"  - {OUTPUT_DIR}/Figure_H2_AttentionNarrowing.png")
    print(f"  - {OUTPUT_DIR}/Figure_H3_MemoryBias.png")
    print(f"  - {OUTPUT_DIR}/Figure_H3_H4_Integration.png")
    print(f"  - {OUTPUT_DIR}/h3_h4_integrated.csv")

if __name__ == "__main__":
    main()
