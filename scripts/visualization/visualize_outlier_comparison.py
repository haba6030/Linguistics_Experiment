"""
Visualization script for comparing different outlier exclusion strategies
Shows robustness of findings across no exclusion, standard exclusion, and stricter exclusion
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

def load_and_prepare_data(data_file):
    """Load SPR data and prepare for analysis"""
    df = pd.read_csv(data_file)

    # Ensure necessary columns exist
    required_cols = ['participant', 'item_id', 'emotion', 'plausibility', 'region', 'RT']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    return df

def apply_exclusion_criteria(df):
    """Apply three different exclusion strategies"""

    # Strategy 1: No exclusion
    df_no_excl = df.copy()
    df_no_excl['exclusion_strategy'] = 'No Exclusion'

    # Strategy 2: Standard exclusion (RT < 100ms or > 3000ms)
    df_standard = df[(df['RT'] >= 100) & (df['RT'] <= 3000)].copy()
    df_standard['exclusion_strategy'] = 'Standard (100-3000ms)'

    # Strategy 3: Stricter exclusion (±2.5 SD per participant per condition)
    df_strict = []
    for (participant, emotion, plausibility, region), group in df.groupby(['participant', 'emotion', 'plausibility', 'region']):
        mean_rt = group['RT'].mean()
        sd_rt = group['RT'].std()
        lower_bound = mean_rt - 2.5 * sd_rt
        upper_bound = mean_rt + 2.5 * sd_rt

        filtered = group[(group['RT'] >= lower_bound) & (group['RT'] <= upper_bound)].copy()
        df_strict.append(filtered)

    df_strict = pd.concat(df_strict, ignore_index=True)
    df_strict['exclusion_strategy'] = 'Stricter (±2.5 SD)'

    # Combine all strategies
    df_combined = pd.concat([df_no_excl, df_standard, df_strict], ignore_index=True)

    # Calculate exclusion statistics
    n_original = len(df)
    n_standard = len(df_standard)
    n_strict = len(df_strict)

    print(f"\n=== Exclusion Statistics ===")
    print(f"Original data points: {n_original}")
    print(f"After standard exclusion: {n_standard} ({100*n_standard/n_original:.1f}% retained)")
    print(f"After stricter exclusion: {n_strict} ({100*n_strict/n_original:.1f}% retained)")

    return df_combined

def plot_h1_modifier_rt_comparison(df, output_dir):
    """
    H1: Attention capture at modifier region
    Compare RT for Hate vs. Neutral modifiers across exclusion strategies
    """

    # Filter for modifier region only
    df_modifier = df[df['region'] == 'modifier'].copy()

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    strategies = ['No Exclusion', 'Standard (100-3000ms)', 'Stricter (±2.5 SD)']

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_modifier[df_modifier['exclusion_strategy'] == strategy]

        # Violin plot with box plot overlay
        sns.violinplot(data=data, x='emotion', y='RT', ax=ax,
                      palette={'H': '#d62728', 'N': '#2ca02c'},
                      inner=None, alpha=0.6)
        sns.boxplot(data=data, x='emotion', y='RT', ax=ax,
                   palette={'H': '#d62728', 'N': '#2ca02c'},
                   width=0.3, boxprops=dict(alpha=0.7))

        # Add mean markers
        means = data.groupby('emotion')['RT'].mean()
        ax.plot([0, 1], [means['H'], means['N']], 'D', color='black',
               markersize=8, label='Mean', zorder=10)

        ax.set_title(f'{strategy}\n(n={len(data)} observations)', fontsize=11, fontweight='bold')
        ax.set_xlabel('Modifier Type', fontsize=10)
        ax.set_ylabel('Reaction Time (ms)' if idx == 0 else '', fontsize=10)
        ax.set_xticklabels(['Hate', 'Neutral'])

        # Add statistics
        mean_h = means['H']
        mean_n = means['N']
        diff = mean_h - mean_n

        y_max = data['RT'].max()
        ax.text(0.5, y_max * 0.95, f'Δ = {diff:.0f} ms',
               ha='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.suptitle('H1: Attention Capture at Modifier Region\n(Hate vs. Neutral)',
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()

    output_file = Path(output_dir) / 'H1_modifier_RT_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()

def plot_h2_interaction_comparison(df, output_dir):
    """
    H2: Emotion × Plausibility interaction at critical noun region
    Show plausibility effect reduction in hate context
    """

    # Filter for critical noun region
    df_noun = df[df['region'] == 'critical_noun'].copy()

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    strategies = ['No Exclusion', 'Standard (100-3000ms)', 'Stricter (±2.5 SD)']

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_noun[df_noun['exclusion_strategy'] == strategy]

        # Calculate means and confidence intervals
        summary = data.groupby(['emotion', 'plausibility'])['RT'].agg(['mean', 'sem']).reset_index()
        summary['ci95'] = 1.96 * summary['sem']

        # Plot interaction
        for emotion, color, label in [('H', '#d62728', 'Hate'), ('N', '#2ca02c', 'Neutral')]:
            emotion_data = summary[summary['emotion'] == emotion]

            x_pos = [0, 1]  # Plausible, Implausible
            y_vals = [emotion_data[emotion_data['plausibility'] == 'P']['mean'].values[0],
                     emotion_data[emotion_data['plausibility'] == 'I']['mean'].values[0]]
            ci_vals = [emotion_data[emotion_data['plausibility'] == 'P']['ci95'].values[0],
                      emotion_data[emotion_data['plausibility'] == 'I']['ci95'].values[0]]

            ax.errorbar(x_pos, y_vals, yerr=ci_vals, marker='o', markersize=10,
                       linewidth=2.5, capsize=5, capthick=2, color=color,
                       label=f'{label} context', alpha=0.8)

        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Plausible', 'Implausible'])
        ax.set_xlabel('Noun Plausibility', fontsize=10)
        ax.set_ylabel('Mean RT (ms)' if idx == 0 else '', fontsize=10)
        ax.set_title(f'{strategy}\n(n={len(data)} observations)', fontsize=11, fontweight='bold')
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Calculate and display plausibility effects
        neutral_plaus = summary[(summary['emotion'] == 'N') & (summary['plausibility'] == 'P')]['mean'].values[0]
        neutral_implaus = summary[(summary['emotion'] == 'N') & (summary['plausibility'] == 'I')]['mean'].values[0]
        hate_plaus = summary[(summary['emotion'] == 'H') & (summary['plausibility'] == 'P')]['mean'].values[0]
        hate_implaus = summary[(summary['emotion'] == 'H') & (summary['plausibility'] == 'I')]['mean'].values[0]

        neutral_effect = neutral_implaus - neutral_plaus
        hate_effect = hate_implaus - hate_plaus
        reduction = neutral_effect - hate_effect

        textstr = f'Neutral effect: {neutral_effect:.0f} ms\nHate effect: {hate_effect:.0f} ms\nReduction: {reduction:.0f} ms'
        ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=8,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.suptitle('H2: Emotion × Plausibility Interaction at Critical Noun\n(Reduced Plausibility Effect in Hate Context)',
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()

    output_file = Path(output_dir) / 'H2_interaction_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()

def plot_rt_by_region_comparison(df, output_dir):
    """
    Show RT across all sentence regions for all conditions
    Across different exclusion strategies
    """

    # Define region order
    region_order = ['context', 'modifier', 'critical_noun', 'spillover']
    df_filtered = df[df['region'].isin(region_order)].copy()

    # Create conditions
    df_filtered['condition'] = df_filtered['emotion'] + df_filtered['plausibility']

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    strategies = ['No Exclusion', 'Standard (100-3000ms)', 'Stricter (±2.5 SD)']

    colors = {'HP': '#1f77b4', 'HI': '#ff7f0e', 'NP': '#2ca02c', 'NI': '#d62728'}
    labels = {'HP': 'Hate-Plausible', 'HI': 'Hate-Implausible',
             'NP': 'Neutral-Plausible', 'NI': 'Neutral-Implausible'}

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_filtered[df_filtered['exclusion_strategy'] == strategy]

        # Calculate means and SEM
        summary = data.groupby(['condition', 'region'])['RT'].agg(['mean', 'sem']).reset_index()

        for condition in ['HP', 'HI', 'NP', 'NI']:
            cond_data = summary[summary['condition'] == condition]
            cond_data = cond_data.set_index('region').reindex(region_order).reset_index()

            x_pos = range(len(region_order))
            ax.plot(x_pos, cond_data['mean'], marker='o', linewidth=2.5,
                   markersize=8, color=colors[condition], label=labels[condition], alpha=0.8)
            ax.fill_between(x_pos,
                           cond_data['mean'] - 1.96 * cond_data['sem'],
                           cond_data['mean'] + 1.96 * cond_data['sem'],
                           alpha=0.2, color=colors[condition])

        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(['Context', 'Modifier', 'Critical\nNoun', 'Spillover'], fontsize=9)
        ax.set_xlabel('Sentence Region', fontsize=10)
        ax.set_ylabel('Mean RT (ms)' if idx == 0 else '', fontsize=10)
        ax.set_title(f'{strategy}', fontsize=11, fontweight='bold')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)

        # Highlight critical regions
        ax.axvspan(0.5, 2.5, alpha=0.1, color='gray')

    plt.suptitle('RT Across Sentence Regions by Condition\n(Shaded area = critical regions)',
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()

    output_file = Path(output_dir) / 'RT_by_region_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()

def plot_exclusion_summary_table(df, output_dir):
    """Create a summary table showing data retention across strategies"""

    # Calculate summary statistics
    summary_stats = []

    for strategy in ['No Exclusion', 'Standard (100-3000ms)', 'Stricter (±2.5 SD)']:
        data = df[df['exclusion_strategy'] == strategy]

        n_obs = len(data)
        n_participants = data['participant'].nunique()
        mean_rt = data['RT'].mean()
        sd_rt = data['RT'].std()
        min_rt = data['RT'].min()
        max_rt = data['RT'].max()

        summary_stats.append({
            'Exclusion Strategy': strategy,
            'N Observations': n_obs,
            'N Participants': n_participants,
            'Mean RT (ms)': f'{mean_rt:.1f}',
            'SD RT (ms)': f'{sd_rt:.1f}',
            'Min RT (ms)': f'{min_rt:.1f}',
            'Max RT (ms)': f'{max_rt:.1f}',
            '% Retained': f'{100 * n_obs / len(df[df["exclusion_strategy"] == "No Exclusion"]):.1f}%'
        })

    summary_df = pd.DataFrame(summary_stats)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=summary_df.values,
                    colLabels=summary_df.columns,
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.18, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.10])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Style header
    for i in range(len(summary_df.columns)):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Style rows
    for i in range(1, len(summary_df) + 1):
        for j in range(len(summary_df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')

    plt.title('Data Retention Across Outlier Exclusion Strategies',
             fontsize=13, fontweight='bold', pad=20)

    output_file = Path(output_dir) / 'exclusion_summary_table.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()

    return summary_df

def main():
    """Main execution function"""

    # Configuration
    data_dir = Path('result_1201')  # Adjust to your actual data directory
    output_dir = Path('result_1201/outlier_comparison_plots')
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("Outlier Exclusion Comparison Visualization")
    print("="*60)

    # Load data
    print("\n[1/6] Loading SPR data...")
    data_file = data_dir / 'spr_cleaned.csv'  # Adjust to your actual file name

    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        print("Please ensure your SPR data is in CSV format with columns:")
        print("  - participant, item_id, emotion, plausibility, region, RT")
        return

    df = load_and_prepare_data(data_file)
    print(f"Loaded {len(df)} observations from {df['participant'].nunique()} participants")

    # Apply exclusion criteria
    print("\n[2/6] Applying exclusion criteria...")
    df_combined = apply_exclusion_criteria(df)

    # Generate visualizations
    print("\n[3/6] Plotting H1: Modifier RT comparison...")
    plot_h1_modifier_rt_comparison(df_combined, output_dir)

    print("\n[4/6] Plotting H2: Interaction comparison...")
    plot_h2_interaction_comparison(df_combined, output_dir)

    print("\n[5/6] Plotting RT by region comparison...")
    plot_rt_by_region_comparison(df_combined, output_dir)

    print("\n[6/6] Creating summary table...")
    summary_df = plot_exclusion_summary_table(df_combined, output_dir)
    print("\n" + summary_df.to_string(index=False))

    print("\n" + "="*60)
    print(f"All visualizations saved to: {output_dir}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
