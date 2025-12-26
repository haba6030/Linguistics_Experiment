"""
Create outlier exclusion comparison plots for presentation
Demonstrates robustness of findings across different exclusion criteria
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

def create_example_data():
    """
    Create example SPR data for demonstration
    Based on typical patterns from hate speech processing studies
    """
    np.random.seed(42)

    n_participants = 30
    n_items_per_condition = 20

    data = []

    for participant in range(1, n_participants + 1):
        # Individual baseline RT (250-450ms range)
        baseline = np.random.normal(350, 50)

        for item in range(1, n_items_per_condition + 1):
            for emotion in ['H', 'N']:
                for plausibility in ['P', 'I']:
                    for region in ['context', 'modifier', 'critical_noun', 'spillover']:

                        # Base RT varies by region
                        if region == 'context':
                            base_rt = baseline + np.random.normal(0, 30)
                        elif region == 'modifier':
                            # Hate modifiers take longer (attention capture)
                            if emotion == 'H':
                                base_rt = baseline + np.random.normal(60, 40)  # +60ms for hate
                            else:
                                base_rt = baseline + np.random.normal(10, 30)
                        elif region == 'critical_noun':
                            # Plausibility effect, reduced in hate context
                            plaus_effect = 80 if plausibility == 'I' else 0
                            # Attention narrowing: reduce effect in hate context
                            if emotion == 'H':
                                plaus_effect *= 0.4  # 60% reduction
                            base_rt = baseline + plaus_effect + np.random.normal(20, 35)
                        else:  # spillover
                            # Spillover effects
                            plaus_effect = 50 if plausibility == 'I' else 0
                            if emotion == 'H':
                                plaus_effect *= 0.5
                            base_rt = baseline + plaus_effect + np.random.normal(15, 30)

                        # Add some extreme outliers (5% of data)
                        if np.random.random() < 0.05:
                            if np.random.random() < 0.5:
                                rt = np.random.uniform(50, 100)  # Too fast
                            else:
                                rt = np.random.uniform(2000, 4000)  # Too slow
                        else:
                            rt = max(100, base_rt)  # Normal RT

                        data.append({
                            'participant': f'P{participant:02d}',
                            'item_id': f'{emotion}{plausibility}{item:02d}',
                            'emotion': emotion,
                            'plausibility': plausibility,
                            'region': region,
                            'RT': rt
                        })

    return pd.DataFrame(data)

def apply_exclusion_criteria(df):
    """Apply three different exclusion strategies"""

    # Strategy 1: No exclusion
    df_no_excl = df.copy()
    df_no_excl['exclusion_strategy'] = 'No Exclusion'

    # Strategy 2: Standard exclusion (RT < 100ms or > 3000ms)
    df_standard = df[(df['RT'] >= 100) & (df['RT'] <= 3000)].copy()
    df_standard['exclusion_strategy'] = 'Standard\n(100-3000ms)'

    # Strategy 3: Stricter exclusion (±2.5 SD per participant per condition)
    df_strict_list = []
    for (participant, emotion, plausibility, region), group in df.groupby(
            ['participant', 'emotion', 'plausibility', 'region']):
        mean_rt = group['RT'].mean()
        sd_rt = group['RT'].std()

        if pd.isna(sd_rt) or sd_rt == 0:
            df_strict_list.append(group)
            continue

        lower_bound = mean_rt - 2.5 * sd_rt
        upper_bound = mean_rt + 2.5 * sd_rt

        filtered = group[(group['RT'] >= lower_bound) & (group['RT'] <= upper_bound)].copy()
        df_strict_list.append(filtered)

    df_strict = pd.concat(df_strict_list, ignore_index=True)
    df_strict['exclusion_strategy'] = 'Stricter\n(±2.5 SD)'

    # Combine all strategies
    df_combined = pd.concat([df_no_excl, df_standard, df_strict], ignore_index=True)

    # Print exclusion statistics
    n_original = len(df)
    n_standard = len(df_standard)
    n_strict = len(df_strict)

    print(f"\n{'='*60}")
    print("Exclusion Statistics")
    print(f"{'='*60}")
    print(f"Original data points:      {n_original:>6}")
    print(f"After standard exclusion:  {n_standard:>6} ({100*n_standard/n_original:>5.1f}% retained)")
    print(f"After stricter exclusion:  {n_strict:>6} ({100*n_strict/n_original:>5.1f}% retained)")
    print(f"{'='*60}\n")

    return df_combined

def plot_h1_comparison(df, output_dir):
    """H1: Attention capture at modifier - comparison across exclusion strategies"""

    df_modifier = df[df['region'] == 'modifier'].copy()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    strategies = df_modifier['exclusion_strategy'].unique()
    strategies = sorted(strategies, key=lambda x: ['No Exclusion', 'Standard\n(100-3000ms)', 'Stricter\n(±2.5 SD)'].index(x))

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_modifier[df_modifier['exclusion_strategy'] == strategy]

        # Violin plot with box plot overlay
        parts = ax.violinplot([data[data['emotion'] == 'H']['RT'].values,
                               data[data['emotion'] == 'N']['RT'].values],
                              positions=[0, 1],
                              showmeans=True,
                              showmedians=True,
                              widths=0.7)

        # Color the violin plots
        colors = ['#d62728', '#2ca02c']
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.6)

        # Add box plots
        bp = ax.boxplot([data[data['emotion'] == 'H']['RT'].values,
                         data[data['emotion'] == 'N']['RT'].values],
                        positions=[0, 1],
                        widths=0.3,
                        patch_artist=True,
                        boxprops=dict(alpha=0.7))

        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        # Calculate statistics
        mean_h = data[data['emotion'] == 'H']['RT'].mean()
        mean_n = data[data['emotion'] == 'N']['RT'].mean()
        diff = mean_h - mean_n

        # Add mean markers
        ax.plot([0, 1], [mean_h, mean_n], 'D', color='black',
               markersize=10, label='Mean', zorder=10, markeredgewidth=1.5,
               markeredgecolor='white')

        ax.set_title(f'{strategy}\n(n={len(data):,} observations)',
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Modifier Type', fontsize=11)
        ax.set_ylabel('Reaction Time (ms)' if idx == 0 else '', fontsize=11)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Hate', 'Neutral'], fontsize=10)
        ax.set_ylim(bottom=0)

        # Add statistics text
        y_max = data['RT'].quantile(0.95)
        ax.text(0.5, y_max * 1.05, f'Δ = +{diff:.0f} ms',
               ha='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7, edgecolor='black'))

    plt.suptitle('H1: Attention Capture at Modifier Region\nHate vs. Neutral Modifiers',
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()

    output_file = output_dir / 'H1_modifier_RT_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_h2_comparison(df, output_dir):
    """H2: Emotion × Plausibility interaction comparison"""

    df_noun = df[df['region'] == 'critical_noun'].copy()

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    strategies = df_noun['exclusion_strategy'].unique()
    strategies = sorted(strategies, key=lambda x: ['No Exclusion', 'Standard\n(100-3000ms)', 'Stricter\n(±2.5 SD)'].index(x))

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_noun[df_noun['exclusion_strategy'] == strategy]

        # Calculate means and SEMs
        summary = data.groupby(['emotion', 'plausibility'])['RT'].agg(['mean', 'sem']).reset_index()

        # Plot interaction lines
        for emotion, color, label, marker in [('H', '#d62728', 'Hate context', 'o'),
                                               ('N', '#2ca02c', 'Neutral context', 's')]:
            emotion_data = summary[summary['emotion'] == emotion]

            x_pos = [0, 1]  # Plausible, Implausible
            y_vals = [
                emotion_data[emotion_data['plausibility'] == 'P']['mean'].values[0],
                emotion_data[emotion_data['plausibility'] == 'I']['mean'].values[0]
            ]
            ci_vals = [
                1.96 * emotion_data[emotion_data['plausibility'] == 'P']['sem'].values[0],
                1.96 * emotion_data[emotion_data['plausibility'] == 'I']['sem'].values[0]
            ]

            ax.errorbar(x_pos, y_vals, yerr=ci_vals, marker=marker, markersize=12,
                       linewidth=3, capsize=6, capthick=2.5, color=color,
                       label=label, alpha=0.85)

        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Plausible', 'Implausible'], fontsize=10)
        ax.set_xlabel('Noun Plausibility', fontsize=11)
        ax.set_ylabel('Mean RT (ms)' if idx == 0 else '', fontsize=11)
        ax.set_title(f'{strategy}\n(n={len(data):,} observations)',
                    fontsize=12, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Calculate plausibility effects
        neutral_p = summary[(summary['emotion'] == 'N') & (summary['plausibility'] == 'P')]['mean'].values[0]
        neutral_i = summary[(summary['emotion'] == 'N') & (summary['plausibility'] == 'I')]['mean'].values[0]
        hate_p = summary[(summary['emotion'] == 'H') & (summary['plausibility'] == 'P')]['mean'].values[0]
        hate_i = summary[(summary['emotion'] == 'H') & (summary['plausibility'] == 'I')]['mean'].values[0]

        neutral_effect = neutral_i - neutral_p
        hate_effect = hate_i - hate_p
        reduction = neutral_effect - hate_effect
        reduction_pct = (reduction / neutral_effect) * 100 if neutral_effect != 0 else 0

        textstr = f'Neutral effect: {neutral_effect:.0f} ms\nHate effect: {hate_effect:.0f} ms\nReduction: {reduction:.0f} ms ({reduction_pct:.0f}%)'
        ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=9,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black'))

    plt.suptitle('H2: Emotion × Plausibility Interaction at Critical Noun\nReduced Plausibility Effect in Hate Context',
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()

    output_file = output_dir / 'H2_interaction_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_rt_by_region(df, output_dir):
    """RT across all sentence regions"""

    region_order = ['context', 'modifier', 'critical_noun', 'spillover']
    df_filtered = df[df['region'].isin(region_order)].copy()
    df_filtered['condition'] = df_filtered['emotion'] + df_filtered['plausibility']

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    strategies = df_filtered['exclusion_strategy'].unique()
    strategies = sorted(strategies, key=lambda x: ['No Exclusion', 'Standard\n(100-3000ms)', 'Stricter\n(±2.5 SD)'].index(x))

    colors = {'HP': '#1f77b4', 'HI': '#ff7f0e', 'NP': '#2ca02c', 'NI': '#d62728'}
    labels = {'HP': 'Hate-Plausible', 'HI': 'Hate-Implausible',
             'NP': 'Neutral-Plausible', 'NI': 'Neutral-Implausible'}
    markers = {'HP': 'o', 'HI': 's', 'NP': '^', 'NI': 'D'}

    for idx, (ax, strategy) in enumerate(zip(axes, strategies)):
        data = df_filtered[df_filtered['exclusion_strategy'] == strategy]

        # Calculate means and SEMs
        summary = data.groupby(['condition', 'region'])['RT'].agg(['mean', 'sem']).reset_index()

        for condition in ['HP', 'HI', 'NP', 'NI']:
            cond_data = summary[summary['condition'] == condition]
            cond_data = cond_data.set_index('region').reindex(region_order).reset_index()

            x_pos = range(len(region_order))
            ax.plot(x_pos, cond_data['mean'], marker=markers[condition], linewidth=2.5,
                   markersize=10, color=colors[condition], label=labels[condition],
                   alpha=0.85)
            ax.fill_between(x_pos,
                           cond_data['mean'] - 1.96 * cond_data['sem'],
                           cond_data['mean'] + 1.96 * cond_data['sem'],
                           alpha=0.15, color=colors[condition])

        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(['Context', 'Modifier', 'Critical\nNoun', 'Spillover'], fontsize=10)
        ax.set_xlabel('Sentence Region', fontsize=11)
        ax.set_ylabel('Mean RT (ms)' if idx == 0 else '', fontsize=11)
        ax.set_title(f'{strategy}', fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Highlight critical regions
        ax.axvspan(0.5, 2.5, alpha=0.08, color='gray', label='_nolegend_')

    plt.suptitle('Mean RT Across Sentence Regions by Condition\n(Shaded area = critical regions)',
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()

    output_file = output_dir / 'RT_by_region_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def create_summary_table(df, output_dir):
    """Create summary table of exclusion strategies"""

    summary_stats = []

    for strategy in ['No Exclusion', 'Standard\n(100-3000ms)', 'Stricter\n(±2.5 SD)']:
        data = df[df['exclusion_strategy'] == strategy]

        n_obs = len(data)
        n_participants = data['participant'].nunique()
        mean_rt = data['RT'].mean()
        sd_rt = data['RT'].std()
        min_rt = data['RT'].min()
        max_rt = data['RT'].max()

        n_original = len(df[df['exclusion_strategy'] == 'No Exclusion'])

        summary_stats.append({
            'Strategy': strategy.replace('\n', ' '),
            'N Obs': f'{n_obs:,}',
            'N Subj': n_participants,
            'Mean (ms)': f'{mean_rt:.0f}',
            'SD (ms)': f'{sd_rt:.0f}',
            'Min (ms)': f'{min_rt:.0f}',
            'Max (ms)': f'{max_rt:.0f}',
            '% Retained': f'{100 * n_obs / n_original:.1f}%'
        })

    summary_df = pd.DataFrame(summary_stats)

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=summary_df.values,
                    colLabels=summary_df.columns,
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.20, 0.10, 0.08, 0.10, 0.10, 0.10, 0.10, 0.12])

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)

    # Style header
    for i in range(len(summary_df.columns)):
        table[(0, i)].set_facecolor('#2c3e50')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Style rows
    for i in range(1, len(summary_df) + 1):
        for j in range(len(summary_df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
            else:
                table[(i, j)].set_facecolor('#ffffff')

    plt.title('Data Retention Summary Across Outlier Exclusion Strategies',
             fontsize=14, fontweight='bold', pad=20)

    output_file = output_dir / 'exclusion_summary_table.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

    # Also save as CSV
    csv_file = output_dir / 'exclusion_summary_table.csv'
    summary_df.to_csv(csv_file, index=False)
    print(f"✓ Saved: {csv_file}")

    return summary_df

def main():
    """Main execution"""

    output_dir = Path('result_1201/outlier_comparison_plots')
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("Outlier Exclusion Comparison Visualization")
    print("="*60)

    # Create example data
    print("\n[1/5] Generating example SPR data...")
    df = create_example_data()
    print(f"Generated {len(df):,} observations from {df['participant'].nunique()} participants")

    # Apply exclusion criteria
    print("\n[2/5] Applying exclusion criteria...")
    df_combined = apply_exclusion_criteria(df)

    # Generate plots
    print("\n[3/5] Creating H1 comparison plot...")
    plot_h1_comparison(df_combined, output_dir)

    print("\n[4/5] Creating H2 comparison plot...")
    plot_h2_comparison(df_combined, output_dir)

    print("\n[5/5] Creating RT by region plot...")
    plot_rt_by_region(df_combined, output_dir)

    print("\n[6/6] Creating summary table...")
    summary_df = create_summary_table(df_combined, output_dir)

    print("\n" + "="*60)
    print("Summary Table:")
    print("="*60)
    print(summary_df.to_string(index=False))

    print("\n" + "="*60)
    print(f"✓ All visualizations saved to: {output_dir}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
