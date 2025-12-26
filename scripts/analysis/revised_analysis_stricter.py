"""
Stricter outlier criteria analysis (200-1600ms)
Comparing with previous analysis (200-3000ms)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

# Font settings - Korean support for modifier words
plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# Outlier criteria
WORD_RT_LOWER = 200
WORD_RT_UPPER_STRICT = 1600  # NEW: stricter upper bound
WORD_RT_UPPER_ORIGINAL = 3000  # OLD: original upper bound

def load_data():
    """데이터 로드"""
    xl = pd.ExcelFile('result_1128/ExpLing_Project.xlsx')
    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name=sheet)
    return data

def remove_practice_trials(df):
    """연습 문장 제거"""
    before = len(df)
    df_clean = df[~df['Sentence_Text'].str.contains('연습', na=False)].copy()
    after = len(df_clean)
    print(f"\n연습 문장 제거: {before}개 → {after}개 ({before-after}개 제거)")
    return df_clean

def identify_outlier_trials(df, method='iqr', k=2.5):
    """Trial-level outlier 식별"""
    total_rts = df['Total_Reading_Time_ms'].values

    if method == 'iqr':
        Q1 = np.percentile(total_rts, 25)
        Q3 = np.percentile(total_rts, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        criterion = f"IQR method (k={k})"

    outliers = (total_rts < lower_bound) | (total_rts > upper_bound)

    print(f"\n=== Trial-level Outlier 제거 ===")
    print(f"기준: {criterion}")
    print(f"상한: {upper_bound:.0f} ms")
    print(f"제거된 trial: {outliers.sum()}개 / {len(df)}개 ({outliers.sum()/len(df)*100:.1f}%)")

    return df[~outliers].copy(), criterion, lower_bound, upper_bound

def parse_sentence_structure(df, upper_bound):
    """문장 구조 파싱 with stricter word-level outlier removal"""
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
            if WORD_RT_LOWER <= rts[0] <= upper_bound:
                parsed_rows.append({**base_info, 'Region_Type': 'Subject', 'Region_Text': regions[0], 'RT': rts[0]})

            # Modifier
            if WORD_RT_LOWER <= rts[1] <= upper_bound:
                parsed_rows.append({**base_info, 'Region_Type': 'Modifier', 'Region_Text': regions[1], 'RT': rts[1]})

            # Spillover
            if WORD_RT_LOWER <= rts[2] <= upper_bound:
                parsed_rows.append({**base_info, 'Region_Type': 'Spillover', 'Region_Text': regions[2], 'RT': rts[2]})

            # Fact (average)
            fact_rts = rts[3:]
            valid_rts = [rt for rt in fact_rts if WORD_RT_LOWER <= rt <= upper_bound]
            if len(valid_rts) > 0:
                avg_fact_rt = np.mean(valid_rts)
                parsed_rows.append({**base_info, 'Region_Type': 'Fact', 'Region_Text': ' '.join(regions[3:]), 'RT': avg_fact_rt})

    return pd.DataFrame(parsed_rows)

def compare_analyses(data):
    """Compare original vs stricter criteria"""
    print("\n" + "="*80)
    print("COMPARISON: Original (200-3000ms) vs Stricter (200-1600ms)")
    print("="*80)

    spr_data = data['SPR_Data']
    spr_clean = remove_practice_trials(spr_data)
    spr_clean, _, _, _ = identify_outlier_trials(spr_clean, method='iqr', k=2.5)

    # Parse with both criteria
    print(f"\n=== Parsing with ORIGINAL criteria (200-{WORD_RT_UPPER_ORIGINAL}ms) ===")
    parsed_original = parse_sentence_structure(spr_clean, WORD_RT_UPPER_ORIGINAL)
    n_original = len(parsed_original)
    print(f"Total observations: {n_original}")

    print(f"\n=== Parsing with STRICTER criteria (200-{WORD_RT_UPPER_STRICT}ms) ===")
    parsed_strict = parse_sentence_structure(spr_clean, WORD_RT_UPPER_STRICT)
    n_strict = len(parsed_strict)
    print(f"Total observations: {n_strict}")

    print(f"\n=== DIFFERENCE ===")
    print(f"Observations removed: {n_original - n_strict} ({(n_original-n_strict)/n_original*100:.2f}%)")

    # Compare H1 results
    print(f"\n{'='*80}")
    print("H1 COMPARISON: Modifier RT")
    print("="*80)

    results_comparison = []

    for label, parsed in [("Original (200-3000ms)", parsed_original),
                          ("Stricter (200-1600ms)", parsed_strict)]:
        modifier_data = parsed[parsed['Region_Type'] == 'Modifier'].copy()

        hate_rt = modifier_data[modifier_data['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
        neutral_rt = modifier_data[modifier_data['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

        mean_h = hate_rt.mean()
        mean_n = neutral_rt.mean()
        diff = mean_h - mean_n

        t_stat, p_val = stats.ttest_rel(hate_rt, neutral_rt)
        cohens_d = diff / hate_rt.std()

        results_comparison.append({
            'Criterion': label,
            'Mean_Hate': mean_h,
            'Mean_Neutral': mean_n,
            'Difference': diff,
            't_stat': t_stat,
            'p_value': p_val,
            'cohens_d': cohens_d,
            'N_obs': len(modifier_data)
        })

        print(f"\n{label}:")
        print(f"  Hate RT: {mean_h:.1f} ms")
        print(f"  Neutral RT: {mean_n:.1f} ms")
        print(f"  Difference: {diff:.1f} ms")
        print(f"  t({len(hate_rt)-1}) = {t_stat:.3f}, p = {p_val:.4f}")
        print(f"  Cohen's d = {cohens_d:.3f}")
        print(f"  N observations: {len(modifier_data)}")

    comparison_df = pd.DataFrame(results_comparison)

    # Save comparison
    comparison_df.to_csv('result_1128/outlier_criteria_comparison.csv', index=False)
    print(f"\n\nComparison saved to: result_1128/outlier_criteria_comparison.csv")

    return parsed_original, parsed_strict, comparison_df

def run_full_analysis_strict(parsed_data, label):
    """Run full analysis with given parsed data"""
    print(f"\n\n{'='*80}")
    print(f"FULL ANALYSIS: {label}")
    print("="*80)

    # H1
    print(f"\n{'='*80}")
    print("H1: Attention Capture at Hate Modifier")
    print("="*80)

    modifier_data = parsed_data[parsed_data['Region_Type'] == 'Modifier'].copy()

    print("\nModifier Region RT by Emotion:")
    h1_desc = modifier_data.groupby('Emotion')['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(h1_desc)

    hate_rt = modifier_data[modifier_data['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
    neutral_rt = modifier_data[modifier_data['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

    t_stat, p_val = stats.ttest_rel(hate_rt, neutral_rt)
    cohens_d = (hate_rt.mean() - neutral_rt.mean()) / hate_rt.std()

    print(f"\nPaired t-test: t({len(hate_rt)-1}) = {t_stat:.3f}, p = {p_val:.4f}")
    print(f"Mean difference: {hate_rt.mean() - neutral_rt.mean():.1f} ms")
    print(f"Cohen's d: {cohens_d:.3f}")

    # H2
    print(f"\n{'='*80}")
    print("H2: Attention Narrowing & Shallow Integration")
    print("="*80)

    critical_data = parsed_data[parsed_data['Region_Type'].isin(['Spillover', 'Fact'])].copy()

    print("\nCritical Region RT (Emotion × Plausibility):")
    h2_desc = critical_data.groupby(['Emotion', 'Plausibility'])['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(h2_desc)

    print("\n\nPlausibility Effect (Implausible - Plausible):")
    for emotion in ['H', 'N']:
        emotion_data = critical_data[critical_data['Emotion'] == emotion]
        plaus_rt = emotion_data[emotion_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        implaus_rt = emotion_data[emotion_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        common_p = plaus_rt.index.intersection(implaus_rt.index)
        if len(common_p) > 0:
            p_aligned = plaus_rt.loc[common_p]
            i_aligned = implaus_rt.loc[common_p]

            effect = i_aligned.mean() - p_aligned.mean()
            t_stat, p_val = stats.ttest_rel(i_aligned, p_aligned)

            print(f"  {emotion}: {effect:.1f} ms (t={t_stat:.3f}, p={p_val:.4f})")

    return modifier_data, critical_data

def create_comparison_visualization(parsed_original, parsed_strict, manip_data):
    """Create side-by-side comparison visualizations"""

    print("\n\nCreating comparison visualizations...")

    # Figure 1: H1 Comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, (parsed, label) in zip(axes, [(parsed_original, "Original (200-3000ms)"),
                                           (parsed_strict, "Stricter (200-1600ms)")]):
        modifier_data = parsed[parsed['Region_Type'] == 'Modifier']
        sns.barplot(data=modifier_data, x='Emotion', y='RT', errorbar='se', ax=ax, palette='Set1')
        ax.set_xlabel('Emotion Condition', fontsize=12, fontweight='bold')
        ax.set_ylabel('Reading Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title(f'H1: {label}', fontsize=13, fontweight='bold')
        ax.set_xticklabels(['Hate (H)', 'Neutral (N)'])

        # Add mean values
        h_mean = modifier_data[modifier_data['Emotion']=='H']['RT'].mean()
        n_mean = modifier_data[modifier_data['Emotion']=='N']['RT'].mean()
        ax.text(0, h_mean + 30, f'{h_mean:.0f}ms', ha='center', fontsize=10, fontweight='bold')
        ax.text(1, n_mean + 30, f'{n_mean:.0f}ms', ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('result_1128/Comparison_H1.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/Comparison_H1.png")
    plt.close()

    # Figure 2: Word-by-word ratings with Korean font
    fig, ax = plt.subplots(figsize=(10, 8))
    word_means = manip_data.groupby(['Modifier_Text', 'Modifier_Category'])['Negativity_Rating'].mean().reset_index()
    word_means_sorted = word_means.sort_values('Negativity_Rating', ascending=False)
    colors = ['red' if cat=='hate' else 'blue' for cat in word_means_sorted['Modifier_Category']]
    ax.barh(word_means_sorted['Modifier_Text'], word_means_sorted['Negativity_Rating'], color=colors, alpha=0.7)
    ax.set_xlabel('Mean Negativity Rating', fontsize=13, fontweight='bold')
    ax.set_ylabel('Modifier Word (Korean)', fontsize=13, fontweight='bold')
    ax.set_title('Word-by-Word Negativity Ratings (Korean Font Fixed)', fontsize=15, fontweight='bold')
    ax.axvline(x=2.5, color='gray', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.savefig('result_1128/Figure_ManipulationCheck_Korean.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/Figure_ManipulationCheck_Korean.png")
    plt.close()

def main():
    """Main analysis pipeline"""
    print("="*80)
    print("STRICTER OUTLIER CRITERIA ANALYSIS")
    print("="*80)

    # Load data
    data = load_data()
    manip_data = data['Manipulation_Check']

    # Compare analyses
    parsed_original, parsed_strict, comparison_df = compare_analyses(data)

    # Run full analysis with stricter criteria
    modifier_strict, critical_strict = run_full_analysis_strict(parsed_strict, "STRICTER (200-1600ms)")

    # Create comparison visualizations
    create_comparison_visualization(parsed_original, parsed_strict, manip_data)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nKey findings:")
    print(f"1. Stricter criteria removed {len(parsed_original) - len(parsed_strict)} additional observations")
    print(f"2. See result_1128/outlier_criteria_comparison.csv for detailed comparison")
    print(f"3. Korean font issue fixed in Figure_ManipulationCheck_Korean.png")

    return comparison_df

if __name__ == "__main__":
    results = main()
