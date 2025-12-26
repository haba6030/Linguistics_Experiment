"""
추가 분석:
1. H4: RT와 회상 패턴 상관분석
2. H2: Spillover vs Fact 영역 분리 분석
3. 개인차 분석 (참가자별 효과크기)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

def analyze_h4_correlations():
    """H4: RT와 회상 패턴 상관분석"""
    print("="*80)
    print("H4 추가 분석: RT와 회상 패턴 상관")
    print("="*80)

    # Load data
    spr = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='SPR_Data')
    recall = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='Recall_Data')

    # Remove practice trials
    spr = spr[~spr['Sentence_Text'].str.contains('연습', na=False)]

    # Calculate per-participant hate modifier RT
    hate_modifier_rt = []

    for idx, row in spr.iterrows():
        if row['Is_Filler'] == 1 or row['Emotion'] != 'H':
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        if len(regions) >= 2:
            hate_modifier_rt.append({
                'Participant_ID': row['Participant_ID'],
                'Modifier_RT': rts[1]  # Second position
            })

    hate_rt_df = pd.DataFrame(hate_modifier_rt)
    hate_rt_summary = hate_rt_df.groupby('Participant_ID')['Modifier_RT'].mean().reset_index()

    # Recall patterns
    background_facts = ['중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
                        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
                        '허브', '노래', '짧은', '반복', '유목', '정착']

    negative_words = ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡']

    recall_patterns = []
    for idx, row in recall.iterrows():
        text = row['Recall_Text']
        fact_count = sum(1 for fact in background_facts if fact in text)
        negative_count = sum(text.count(word) for word in negative_words)

        recall_patterns.append({
            'Participant_ID': row['Participant_ID'],
            'Fact_Count': fact_count,
            'Negative_Count': negative_count,
            'Text_Length': len(text)
        })

    recall_df = pd.DataFrame(recall_patterns)

    # Merge
    merged = hate_rt_summary.merge(recall_df, on='Participant_ID')

    print(f"\n참가자별 혐오 수식어 RT와 회상 패턴:")
    print(merged.to_string(index=False))

    # Correlations
    print("\n\n=== 상관분석 ===")

    corr1, p1 = stats.pearsonr(merged['Modifier_RT'], merged['Fact_Count'])
    print(f"\n1. 혐오 수식어 RT × 사실 포함 개수:")
    print(f"   r = {corr1:.3f}, p = {p1:.3f}")
    print(f"   해석: RT 높을수록 사실 {'많이' if corr1 > 0 else '적게'} 회상")

    corr2, p2 = stats.pearsonr(merged['Modifier_RT'], merged['Negative_Count'])
    print(f"\n2. 혐오 수식어 RT × 부정 표현 사용:")
    print(f"   r = {corr2:.3f}, p = {p2:.3f}")
    print(f"   해석: RT 높을수록 부정 표현 {'많이' if corr2 > 0 else '적게'} 사용")

    print(f"\n주의: N=6으로 상관분석은 통계적 검정력이 매우 낮음 (탐색적 분석)")

    return merged

def analyze_h2_regions_separate():
    """H2: Spillover vs Fact 영역 분리 분석"""
    print("\n\n" + "="*80)
    print("H2 추가 분석: Spillover vs Fact 영역 분리")
    print("="*80)

    spr = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='SPR_Data')
    spr = spr[~spr['Sentence_Text'].str.contains('연습', na=False)]

    # Remove trial outliers
    Q1 = spr['Total_Reading_Time_ms'].quantile(0.25)
    Q3 = spr['Total_Reading_Time_ms'].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 2.5 * IQR
    spr = spr[spr['Total_Reading_Time_ms'] <= upper]

    # Parse separately
    spillover_data = []
    fact_data = []

    for idx, row in spr.iterrows():
        if row['Is_Filler'] == 1:
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        if len(regions) >= 4:
            # Spillover (position 2)
            if 200 <= rts[2] <= 3000:
                spillover_data.append({
                    'Participant_ID': row['Participant_ID'],
                    'Emotion': row['Emotion'],
                    'Plausibility': row['Plausibility'],
                    'RT': rts[2],
                    'Region': 'Spillover'
                })

            # Fact (average of rest)
            fact_rts = [rt for rt in rts[3:] if 200 <= rt <= 3000]
            if fact_rts:
                fact_data.append({
                    'Participant_ID': row['Participant_ID'],
                    'Emotion': row['Emotion'],
                    'Plausibility': row['Plausibility'],
                    'RT': np.mean(fact_rts),
                    'Region': 'Fact'
                })

    spillover_df = pd.DataFrame(spillover_data)
    fact_df = pd.DataFrame(fact_data)

    print("\n=== Spillover 영역 ===")
    print("\nEmotion × Plausibility:")
    spill_summary = spillover_df.groupby(['Emotion', 'Plausibility'])['RT'].agg(['mean', 'std', 'count'])
    print(spill_summary)

    print("\n그럴듯함 효과:")
    for emotion in ['H', 'N']:
        e_data = spillover_df[spillover_df['Emotion'] == emotion]
        p_rt = e_data[e_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        i_rt = e_data[e_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        common = p_rt.index.intersection(i_rt.index)
        if len(common) > 0:
            effect = i_rt.loc[common].mean() - p_rt.loc[common].mean()
            t_stat, p_val = stats.ttest_rel(i_rt.loc[common], p_rt.loc[common])
            print(f"  {emotion}: {effect:.1f}ms (t={t_stat:.2f}, p={p_val:.3f})")

    print("\n\n=== Fact 영역 ===")
    print("\nEmotion × Plausibility:")
    fact_summary = fact_df.groupby(['Emotion', 'Plausibility'])['RT'].agg(['mean', 'std', 'count'])
    print(fact_summary)

    print("\n그럴듯함 효과:")
    for emotion in ['H', 'N']:
        e_data = fact_df[fact_df['Emotion'] == emotion]
        p_rt = e_data[e_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        i_rt = e_data[e_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        common = p_rt.index.intersection(i_rt.index)
        if len(common) > 0:
            effect = i_rt.loc[common].mean() - p_rt.loc[common].mean()
            t_stat, p_val = stats.ttest_rel(i_rt.loc[common], p_rt.loc[common])
            print(f"  {emotion}: {effect:.1f}ms (t={t_stat:.2f}, p={p_val:.3f})")

    return spillover_df, fact_df

def analyze_individual_differences():
    """개인차 분석"""
    print("\n\n" + "="*80)
    print("개인차 분석: 참가자별 H1 효과크기")
    print("="*80)

    spr = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='SPR_Data')
    spr = spr[~spr['Sentence_Text'].str.contains('연습', na=False)]

    Q1 = spr['Total_Reading_Time_ms'].quantile(0.25)
    Q3 = spr['Total_Reading_Time_ms'].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 2.5 * IQR
    spr = spr[spr['Total_Reading_Time_ms'] <= upper]

    # Extract modifier RTs
    modifier_data = []
    for idx, row in spr.iterrows():
        if row['Is_Filler'] == 1:
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        if len(regions) >= 2 and 200 <= rts[1] <= 3000:
            modifier_data.append({
                'Participant_ID': row['Participant_ID'],
                'Emotion': row['Emotion'],
                'RT': rts[1]
            })

    mod_df = pd.DataFrame(modifier_data)

    # By participant
    participant_effects = []

    for pid in mod_df['Participant_ID'].unique():
        p_data = mod_df[mod_df['Participant_ID'] == pid]

        h_rt = p_data[p_data['Emotion'] == 'H']['RT'].mean()
        n_rt = p_data[p_data['Emotion'] == 'N']['RT'].mean()

        h_std = p_data[p_data['Emotion'] == 'H']['RT'].std()

        diff = h_rt - n_rt
        cohens_d = diff / h_std if h_std > 0 else 0

        participant_effects.append({
            'Participant_ID': pid,
            'Hate_RT': h_rt,
            'Neutral_RT': n_rt,
            'Difference': diff,
            'Cohens_d': cohens_d,
            'Direction': 'H>N' if diff > 0 else 'N>H'
        })

    effects_df = pd.DataFrame(participant_effects).sort_values('Difference', ascending=False)

    print("\n참가자별 H1 효과 (혐오 - 중립):")
    print(effects_df.to_string(index=False))

    print(f"\n\n일관성 있는 방향 (H>N): {sum(effects_df['Difference'] > 0)}/6 참가자")
    print(f"평균 효과크기 (Cohen's d): {effects_df['Cohens_d'].mean():.3f}")

    return effects_df

def main():
    """메인 함수"""
    print("추가 분석 실행\n")

    # 1. H4 correlations
    h4_merged = analyze_h4_correlations()

    # 2. H2 regions
    spillover_df, fact_df = analyze_h2_regions_separate()

    # 3. Individual differences
    individual_df = analyze_individual_differences()

    # Save results
    h4_merged.to_csv('result_1128/h4_correlations.csv', index=False)
    individual_df.to_csv('result_1128/individual_differences.csv', index=False)

    print("\n\n" + "="*80)
    print("추가 분석 완료")
    print("="*80)
    print("\n저장된 파일:")
    print("  - result_1128/h4_correlations.csv")
    print("  - result_1128/individual_differences.csv")

if __name__ == "__main__":
    main()
