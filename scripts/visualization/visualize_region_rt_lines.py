"""
Line graph visualization of Region RT by condition
Divides lines by:
1. Emotion (Hate vs Neutral)
2. Plausibility (Plausible vs Implausible)
3. All four conditions (HP, HI, NP, NI)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def load_data():
    """Load data from Excel file"""
    xl = pd.ExcelFile('result_1201/ExpLing_Project.xlsx')
    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel('result_1201/ExpLing_Project.xlsx', sheet_name=sheet)
    return data

def remove_practice_trials(df):
    """Remove practice trials"""
    before = len(df)
    df_clean = df[~df['Sentence_Text'].str.contains('연습', na=False)].copy()
    after = len(df_clean)
    print(f"Practice trials removed: {before} → {after} ({before-after} removed)")
    return df_clean

def identify_outlier_trials(df, method='iqr', k=2.5):
    """Identify and remove trial-level outliers"""
    total_rts = df['Total_Reading_Time_ms'].values

    if method == 'iqr':
        Q1 = np.percentile(total_rts, 25)
        Q3 = np.percentile(total_rts, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
    else:  # sd method
        mean_rt = np.mean(total_rts)
        sd_rt = np.std(total_rts)
        lower_bound = mean_rt - k * sd_rt
        upper_bound = mean_rt + k * sd_rt

    outliers = (total_rts < lower_bound) | (total_rts > upper_bound)
    print(f"Outlier trials removed: {outliers.sum()} / {len(df)} ({outliers.sum()/len(df)*100:.1f}%)")

    return df[~outliers].copy()

def parse_sentence_structure(df):
    """Parse sentence structure: Subject - Modifier - Spillover - Fact"""
    parsed_rows = []

    for idx, row in df.iterrows():
        if row['Is_Filler'] == 1:  # Skip fillers
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
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Subject',
                'Region_Text': regions[0],
                'RT': rts[0],
                'Region_Position': 0
            })

            # Modifier
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Modifier',
                'Region_Text': regions[1],
                'RT': rts[1],
                'Region_Position': 1
            })

            # Spillover
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Spillover',
                'Region_Text': regions[2],
                'RT': rts[2],
                'Region_Position': 2
            })

            # Fact region (average)
            fact_regions = regions[3:]
            fact_rts = rts[3:]

            # Word-level outlier removal (200-3000ms)
            valid_rts = [rt for rt in fact_rts if 200 <= rt <= 3000]
            if len(valid_rts) > 0:
                avg_fact_rt = np.mean(valid_rts)
                parsed_rows.append({
                    **base_info,
                    'Region_Type': 'Fact',
                    'Region_Text': ' '.join(fact_regions),
                    'RT': avg_fact_rt,
                    'Region_Position': 3
                })

    return pd.DataFrame(parsed_rows)

def remove_word_outliers(df, lower=200, upper=3000):
    """Remove word-level outliers"""
    before = len(df)
    df_clean = df[(df['RT'] >= lower) & (df['RT'] <= upper)].copy()
    after = len(df_clean)
    removed = before - after
    print(f"Word-level outliers removed (200-3000ms): {removed} / {before} ({removed/before*100:.1f}%)")
    return df_clean

def create_line_plots(parsed_data, output_dir='result_1201'):
    """Create line graph visualizations"""

    # Region order and labels
    region_order = ['Subject', 'Modifier', 'Spillover', 'Fact']
    region_labels = ['Subject', 'Modifier', 'Spillover', 'Fact']

    # Calculate means and SEM for each condition
    # We'll compute both participant-level means and overall means

    # =================================================================
    # Figure 1: Split by Emotion (Hate vs Neutral)
    # =================================================================
    fig, ax = plt.subplots(figsize=(12, 7))

    for emotion, color, marker in [('H', '#d62728', 'o'), ('N', '#1f77b4', 's')]:
        emotion_data = parsed_data[parsed_data['Emotion'] == emotion]

        # Aggregate by participant first, then take mean and SEM
        region_means = []
        region_sems = []

        for region in region_order:
            region_data = emotion_data[emotion_data['Region_Type'] == region]
            participant_means = region_data.groupby('Participant_ID')['RT'].mean()

            region_means.append(participant_means.mean())
            region_sems.append(participant_means.sem())

        # Plot line with error bars
        ax.errorbar(range(len(region_order)), region_means, yerr=region_sems,
                   marker=marker, markersize=12, linewidth=3, capsize=8,
                   label='Hate' if emotion=='H' else 'Neutral',
                   color=color, alpha=0.9)

    ax.set_xticks(range(len(region_order)))
    ax.set_xticklabels(region_labels, fontsize=13)
    ax.set_xlabel('Sentence Region', fontsize=14, fontweight='bold')
    ax.set_ylabel('Mean Reading Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('Reading Time by Region: Hate vs Neutral', fontsize=16, fontweight='bold')
    ax.legend(fontsize=13, loc='best', frameon=True, shadow=True)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_RegionRT_by_Emotion_Lines.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/Figure_RegionRT_by_Emotion_Lines.png")
    plt.close()

    # =================================================================
    # Figure 2: Split by Plausibility (Plausible vs Implausible)
    # =================================================================
    fig, ax = plt.subplots(figsize=(12, 7))

    for plaus, color, marker in [('P', '#2ca02c', 'o'), ('I', '#ff7f0e', '^')]:
        plaus_data = parsed_data[parsed_data['Plausibility'] == plaus]

        region_means = []
        region_sems = []

        for region in region_order:
            region_data = plaus_data[plaus_data['Region_Type'] == region]
            participant_means = region_data.groupby('Participant_ID')['RT'].mean()

            region_means.append(participant_means.mean())
            region_sems.append(participant_means.sem())

        ax.errorbar(range(len(region_order)), region_means, yerr=region_sems,
                   marker=marker, markersize=12, linewidth=3, capsize=8,
                   label='Plausible' if plaus=='P' else 'Implausible',
                   color=color, alpha=0.9)

    ax.set_xticks(range(len(region_order)))
    ax.set_xticklabels(region_labels, fontsize=13)
    ax.set_xlabel('Sentence Region', fontsize=14, fontweight='bold')
    ax.set_ylabel('Mean Reading Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('Reading Time by Region: Plausible vs Implausible', fontsize=16, fontweight='bold')
    ax.legend(fontsize=13, loc='best', frameon=True, shadow=True)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_RegionRT_by_Plausibility_Lines.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/Figure_RegionRT_by_Plausibility_Lines.png")
    plt.close()

    # =================================================================
    # Figure 3: All four conditions (HP, HI, NP, NI)
    # =================================================================
    fig, ax = plt.subplots(figsize=(14, 8))

    conditions = [
        ('H', 'P', 'HP: Hate-Plausible', '#ff9999', 'o'),
        ('H', 'I', 'HI: Hate-Implausible', '#ff0000', '^'),
        ('N', 'P', 'NP: Neutral-Plausible', '#9999ff', 's'),
        ('N', 'I', 'NI: Neutral-Implausible', '#0000ff', 'D')
    ]

    for emotion, plaus, label, color, marker in conditions:
        cond_data = parsed_data[(parsed_data['Emotion'] == emotion) &
                                (parsed_data['Plausibility'] == plaus)]

        region_means = []
        region_sems = []

        for region in region_order:
            region_data = cond_data[cond_data['Region_Type'] == region]
            participant_means = region_data.groupby('Participant_ID')['RT'].mean()

            region_means.append(participant_means.mean())
            region_sems.append(participant_means.sem())

        ax.errorbar(range(len(region_order)), region_means, yerr=region_sems,
                   marker=marker, markersize=10, linewidth=2.5, capsize=6,
                   label=label, color=color, alpha=0.85)

    ax.set_xticks(range(len(region_order)))
    ax.set_xticklabels(region_labels, fontsize=13)
    ax.set_xlabel('Sentence Region', fontsize=14, fontweight='bold')
    ax.set_ylabel('Mean Reading Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('Reading Time by Region: All Four Conditions', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='best', frameon=True, shadow=True, ncol=2)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_RegionRT_All_Conditions_Lines.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/Figure_RegionRT_All_Conditions_Lines.png")
    plt.close()

    # =================================================================
    # Figure 4: Faceted view (2x2 subplot) - Emotion x Plausibility
    # =================================================================
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True, sharey=True)

    subplot_configs = [
        (0, 0, 'H', 'P', 'Hate-Plausible', '#ff9999'),
        (0, 1, 'H', 'I', 'Hate-Implausible', '#ff0000'),
        (1, 0, 'N', 'P', 'Neutral-Plausible', '#9999ff'),
        (1, 1, 'N', 'I', 'Neutral-Implausible', '#0000ff')
    ]

    for row, col, emotion, plaus, title, color in subplot_configs:
        ax = axes[row, col]
        cond_data = parsed_data[(parsed_data['Emotion'] == emotion) &
                                (parsed_data['Plausibility'] == plaus)]

        region_means = []
        region_sems = []

        for region in region_order:
            region_data = cond_data[cond_data['Region_Type'] == region]
            participant_means = region_data.groupby('Participant_ID')['RT'].mean()

            region_means.append(participant_means.mean())
            region_sems.append(participant_means.sem())

        ax.errorbar(range(len(region_order)), region_means, yerr=region_sems,
                   marker='o', markersize=10, linewidth=3, capsize=8,
                   color=color, alpha=0.9)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(region_labels, fontsize=11)
        ax.grid(alpha=0.3)

        if col == 0:
            ax.set_ylabel('Reading Time (ms)', fontsize=12, fontweight='bold')
        if row == 1:
            ax.set_xlabel('Sentence Region', fontsize=12, fontweight='bold')

    fig.suptitle('Reading Time by Region: Faceted by Condition',
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_RegionRT_Faceted_Lines.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/Figure_RegionRT_Faceted_Lines.png")
    plt.close()

def main():
    """Main pipeline"""
    print("="*80)
    print("Creating Line Graph Visualizations for Region RT")
    print("="*80)

    # Load data
    print("\nLoading data...")
    data = load_data()
    spr_data = data['SPR_Data']

    # Remove practice trials
    print("\nRemoving practice trials...")
    spr_clean = remove_practice_trials(spr_data)

    # Remove trial-level outliers
    print("\nRemoving trial-level outliers...")
    spr_clean = identify_outlier_trials(spr_clean, method='iqr', k=2.5)

    # Parse sentence structure
    print("\nParsing sentence structure...")
    parsed_data = parse_sentence_structure(spr_clean)
    print(f"Parsed observations: {len(parsed_data)}")

    # Remove word-level outliers
    print("\nRemoving word-level outliers...")
    parsed_data = remove_word_outliers(parsed_data)

    # Create line plots
    print("\n" + "="*80)
    print("Creating line graph visualizations...")
    print("="*80)
    create_line_plots(parsed_data)

    print("\n" + "="*80)
    print("Visualization complete!")
    print("="*80)

if __name__ == "__main__":
    main()
