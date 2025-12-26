"""
Detailed word-by-word reading time analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'

def load_and_parse_spr():
    """Load and parse SPR data"""
    df = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='SPR_Data')

    # Parse regions
    df['Regions_List'] = df['Regions'].apply(eval)
    df['RT_List'] = df['Region_RTs'].apply(eval)

    parsed_rows = []
    for idx, row in df.iterrows():
        regions = row['Regions_List']
        rts = row['RT_List']

        for i, (region_text, rt) in enumerate(zip(regions, rts)):
            parsed_row = {
                'Participant_ID': row['Participant_ID'],
                'Item_ID': row['Item_ID'],
                'Base': row['Base'],
                'Emotion': row['Emotion'],
                'Plausibility': row['Plausibility'],
                'Is_Filler': row['Is_Filler'],
                'Region_Index': i,
                'Region_Text': region_text,
                'RT': rt
            }
            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)

def create_detailed_visualizations():
    """Create detailed region-by-region analysis"""

    spr_parsed = load_and_parse_spr()

    # Filter experimental items only and remove outliers
    exp_data = spr_parsed[
        (spr_parsed['Is_Filler'] == 0) &
        (spr_parsed['RT'] >= 200) &
        (spr_parsed['RT'] <= 3000)
    ].copy()

    # Create figure with multiple panels
    fig = plt.figure(figsize=(20, 12))

    # Panel 1: Region-by-region RT for Emotion (H vs N), averaged across plausibility
    ax1 = plt.subplot(2, 3, 1)
    region_emotion = exp_data.groupby(['Region_Index', 'Emotion'])['RT'].agg(['mean', 'sem']).reset_index()

    for emotion, color in [('H', 'red'), ('N', 'blue')]:
        data = region_emotion[region_emotion['Emotion'] == emotion]
        ax1.plot(data['Region_Index'], data['mean'], marker='o', label=f'Emotion: {emotion}',
                color=color, linewidth=2, markersize=8)
        ax1.fill_between(data['Region_Index'],
                         data['mean'] - data['sem'],
                         data['mean'] + data['sem'],
                         alpha=0.2, color=color)

    ax1.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Reading Time (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Reading Time by Word Position: Hate vs Neutral', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Region-by-region RT for Plausibility (P vs I), averaged across emotion
    ax2 = plt.subplot(2, 3, 2)
    region_plaus = exp_data.groupby(['Region_Index', 'Plausibility'])['RT'].agg(['mean', 'sem']).reset_index()

    for plaus, color in [('P', 'green'), ('I', 'orange')]:
        data = region_plaus[region_plaus['Plausibility'] == plaus]
        ax2.plot(data['Region_Index'], data['mean'], marker='s', label=f'Plausibility: {plaus}',
                color=color, linewidth=2, markersize=8)
        ax2.fill_between(data['Region_Index'],
                         data['mean'] - data['sem'],
                         data['mean'] + data['sem'],
                         alpha=0.2, color=color)

    ax2.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Reading Time (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Reading Time by Word Position: Plausible vs Implausible', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Heatmap of mean RT by Region × Emotion
    ax3 = plt.subplot(2, 3, 3)
    heatmap_data = exp_data.groupby(['Region_Index', 'Emotion'])['RT'].mean().unstack()
    sns.heatmap(heatmap_data.T, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'RT (ms)'})
    ax3.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Emotion', fontsize=12, fontweight='bold')
    ax3.set_title('Heatmap: RT by Position × Emotion', fontsize=14, fontweight='bold')

    # Panel 4: All four conditions (2x2 design)
    ax4 = plt.subplot(2, 3, 4)
    four_way = exp_data.groupby(['Region_Index', 'Emotion', 'Plausibility'])['RT'].agg(['mean', 'sem']).reset_index()

    conditions = [
        ('H', 'P', 'red', 'Hate-Plausible', 'o-'),
        ('H', 'I', 'darkred', 'Hate-Implausible', 'o--'),
        ('N', 'P', 'blue', 'Neutral-Plausible', 's-'),
        ('N', 'I', 'darkblue', 'Neutral-Implausible', 's--')
    ]

    for emotion, plaus, color, label, style in conditions:
        data = four_way[(four_way['Emotion'] == emotion) & (four_way['Plausibility'] == plaus)]
        ax4.plot(data['Region_Index'], data['mean'], style, label=label,
                color=color, linewidth=2, markersize=6, alpha=0.8)

    ax4.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Reading Time (ms)', fontsize=12, fontweight='bold')
    ax4.set_title('All Four Conditions (Emotion × Plausibility)', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=9, loc='best')
    ax4.grid(True, alpha=0.3)

    # Panel 5: Difference scores (Hate - Neutral) by region
    ax5 = plt.subplot(2, 3, 5)
    diff_data = []
    for region in exp_data['Region_Index'].unique():
        region_data = exp_data[exp_data['Region_Index'] == region]
        hate_rt = region_data[region_data['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
        neutral_rt = region_data[region_data['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

        # Align participants
        common_participants = hate_rt.index.intersection(neutral_rt.index)
        if len(common_participants) > 0:
            hate_aligned = hate_rt.loc[common_participants]
            neutral_aligned = neutral_rt.loc[common_participants]
            diff = hate_aligned.mean() - neutral_aligned.mean()
            sem = (hate_aligned - neutral_aligned).sem()

            # t-test
            t_stat, p_val = stats.ttest_rel(hate_aligned, neutral_aligned)

            diff_data.append({
                'Region_Index': region,
                'Difference': diff,
                'SEM': sem,
                'p_value': p_val,
                'significant': p_val < 0.05
            })

    diff_df = pd.DataFrame(diff_data)

    colors = ['green' if sig else 'gray' for sig in diff_df['significant']]
    bars = ax5.bar(diff_df['Region_Index'], diff_df['Difference'], yerr=diff_df['SEM'],
                   color=colors, alpha=0.7, capsize=5)
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax5.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax5.set_ylabel('RT Difference (Hate - Neutral, ms)', fontsize=12, fontweight='bold')
    ax5.set_title('Attention Capture by Region (Green = p<.05)', fontsize=14, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')

    # Panel 6: Plausibility effect by emotion and region
    ax6 = plt.subplot(2, 3, 6)
    plaus_effect_data = []
    for region in exp_data['Region_Index'].unique():
        for emotion in ['H', 'N']:
            region_data = exp_data[(exp_data['Region_Index'] == region) & (exp_data['Emotion'] == emotion)]
            plaus_rt = region_data[region_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
            implaus_rt = region_data[region_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

            common_participants = plaus_rt.index.intersection(implaus_rt.index)
            if len(common_participants) > 0:
                plaus_aligned = plaus_rt.loc[common_participants]
                implaus_aligned = implaus_rt.loc[common_participants]
                effect = implaus_aligned.mean() - plaus_aligned.mean()

                plaus_effect_data.append({
                    'Region_Index': region,
                    'Emotion': emotion,
                    'Plausibility_Effect': effect
                })

    plaus_effect_df = pd.DataFrame(plaus_effect_data)

    for emotion, color, marker in [('H', 'red', 'o'), ('N', 'blue', 's')]:
        data = plaus_effect_df[plaus_effect_df['Emotion'] == emotion]
        ax6.plot(data['Region_Index'], data['Plausibility_Effect'],
                marker=marker, label=f'{emotion}', color=color, linewidth=2, markersize=8)

    ax6.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax6.set_xlabel('Word Position (Region Index)', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Plausibility Effect (Implaus - Plaus, ms)', fontsize=12, fontweight='bold')
    ax6.set_title('H2: Plausibility Effect by Region and Emotion', fontsize=14, fontweight='bold')
    ax6.legend(fontsize=11)
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('result_1128/detailed_region_analysis.png', dpi=300, bbox_inches='tight')
    print("\nSaved: result_1128/detailed_region_analysis.png")

    # Print statistical summary for each region
    print("\n" + "="*80)
    print("REGION-BY-REGION STATISTICAL SUMMARY")
    print("="*80)

    print("\nEmotion Effect (Hate - Neutral) by Region:")
    print(diff_df.to_string(index=False))

    print("\n\nPlausibility Effect (Implausible - Plausible) by Region and Emotion:")
    plaus_pivot = plaus_effect_df.pivot(index='Region_Index', columns='Emotion', values='Plausibility_Effect')
    plaus_pivot['Interaction'] = plaus_pivot['H'] - plaus_pivot['N']
    print(plaus_pivot.to_string())

if __name__ == "__main__":
    create_detailed_visualizations()
