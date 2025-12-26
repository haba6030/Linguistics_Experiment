#!/usr/bin/env python3
"""
Apply outlier exclusion criteria to result_1201 SPR data
Generates comparison statistics and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Create output directory if needed
os.makedirs('result_1201', exist_ok=True)

# Read the data
print("Reading data...")
df = pd.read_csv('result_1201/spr_data_parsed_1201.csv')

print(f"Original data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Filter to experimental items only (exclude fillers)
df_exp = df[df['is_filler'] == 0].copy()
print(f"\nExperimental items only: {df_exp.shape}")

# Check modifier RT column
print(f"\nModifier RT column info:")
print(df_exp['modifier_RT'].describe())
print(f"Min: {df_exp['modifier_RT'].min()}")
print(f"Max: {df_exp['modifier_RT'].max()}")
print(f"Values >1600ms: {(df_exp['modifier_RT'] > 1600).sum()}")
print(f"Values >3000ms: {(df_exp['modifier_RT'] > 3000).sum()}")

# Define exclusion criteria
criteria = {
    'Original (200-3000ms)': (200, 3000),
    'Stricter (200-1600ms)': (200, 1600)
}

# Store results
results = []

print("\n" + "="*60)
print("APPLYING EXCLUSION CRITERIA")
print("="*60)

for criterion_name, (lower, upper) in criteria.items():
    print(f"\n{criterion_name}:")
    print(f"  Lower bound: {lower}ms")
    print(f"  Upper bound: {upper}ms")

    # Apply exclusion
    mask = (df_exp['modifier_RT'] >= lower) & (df_exp['modifier_RT'] <= upper)
    df_filtered = df_exp[mask].copy()

    n_excluded = len(df_exp) - len(df_filtered)
    pct_excluded = 100 * n_excluded / len(df_exp)

    print(f"  Excluded: {n_excluded} trials ({pct_excluded:.1f}%)")
    print(f"  Retained: {len(df_filtered)} trials")

    # Calculate statistics by emotion condition
    hate_rts = df_filtered[df_filtered['emotion'] == 'H']['modifier_RT']
    neutral_rts = df_filtered[df_filtered['emotion'] == 'N']['modifier_RT']

    mean_hate = hate_rts.mean()
    mean_neutral = neutral_rts.mean()
    diff = mean_hate - mean_neutral

    # Statistical test
    t_stat, p_value = stats.ttest_ind(hate_rts, neutral_rts)

    # Cohen's d
    pooled_std = np.sqrt(((len(hate_rts)-1)*hate_rts.std()**2 +
                          (len(neutral_rts)-1)*neutral_rts.std()**2) /
                         (len(hate_rts) + len(neutral_rts) - 2))
    cohens_d = diff / pooled_std

    print(f"  Mean Hate RT: {mean_hate:.2f}ms")
    print(f"  Mean Neutral RT: {mean_neutral:.2f}ms")
    print(f"  Difference: {diff:.2f}ms")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
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
        'N_hate': len(hate_rts),
        'N_neutral': len(neutral_rts)
    })

    # Save filtered dataset
    output_name = criterion_name.split()[0].lower()
    output_file = f'result_1201/spr_data_parsed_1201_{output_name}.csv'
    df_filtered.to_csv(output_file, index=False)
    print(f"  Saved to: {output_file}")

# Save comparison table
results_df = pd.DataFrame(results)
results_df.to_csv('result_1201/outlier_criteria_comparison.csv', index=False)
print("\n" + "="*60)
print("Comparison table saved to: result_1201/outlier_criteria_comparison.csv")
print("="*60)

# Create visualization
print("\nGenerating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Distribution comparison - Original
ax1 = axes[0, 0]
mask_orig = (df_exp['modifier_RT'] >= 200) & (df_exp['modifier_RT'] <= 3000)
df_orig = df_exp[mask_orig]

for emotion, label, color in [('H', 'Hate', 'red'), ('N', 'Neutral', 'blue')]:
    data = df_orig[df_orig['emotion'] == emotion]['modifier_RT']
    ax1.hist(data, bins=30, alpha=0.5, label=label, color=color, edgecolor='black')

ax1.axvline(1600, color='green', linestyle='--', linewidth=2, label='Stricter cutoff (1600ms)')
ax1.set_xlabel('Modifier RT (ms)', fontsize=11)
ax1.set_ylabel('Frequency', fontsize=11)
ax1.set_title('Original Criterion (200-3000ms)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Plot 2: Distribution comparison - Stricter
ax2 = axes[0, 1]
mask_strict = (df_exp['modifier_RT'] >= 200) & (df_exp['modifier_RT'] <= 1600)
df_strict = df_exp[mask_strict]

for emotion, label, color in [('H', 'Hate', 'red'), ('N', 'Neutral', 'blue')]:
    data = df_strict[df_strict['emotion'] == emotion]['modifier_RT']
    ax2.hist(data, bins=30, alpha=0.5, label=label, color=color, edgecolor='black')

ax2.set_xlabel('Modifier RT (ms)', fontsize=11)
ax2.set_ylabel('Frequency', fontsize=11)
ax2.set_title('Stricter Criterion (200-1600ms)', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

# Plot 3: Box plots comparison
ax3 = axes[1, 0]
data_for_box = []
labels_for_box = []

for criterion_name, (lower, upper) in criteria.items():
    mask = (df_exp['modifier_RT'] >= lower) & (df_exp['modifier_RT'] <= upper)
    df_filtered = df_exp[mask]

    for emotion, label in [('H', 'Hate'), ('N', 'Neutral')]:
        data_for_box.append(df_filtered[df_filtered['emotion'] == emotion]['modifier_RT'])
        short_name = 'Orig' if 'Original' in criterion_name else 'Strict'
        labels_for_box.append(f'{short_name}\n{label}')

bp = ax3.boxplot(data_for_box, labels=labels_for_box, patch_artist=True)
colors = ['lightcoral', 'lightblue', 'lightcoral', 'lightblue']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

ax3.set_ylabel('Modifier RT (ms)', fontsize=11)
ax3.set_title('RT Distribution by Criterion', fontsize=12, fontweight='bold')
ax3.grid(alpha=0.3, axis='y')

# Plot 4: Mean comparison with error bars
ax4 = axes[1, 1]
x_pos = np.arange(len(results))
width = 0.35

hate_means = [r['Mean_Hate'] for r in results]
neutral_means = [r['Mean_Neutral'] for r in results]

# Calculate SEM
hate_sems = []
neutral_sems = []
for criterion_name, (lower, upper) in criteria.items():
    mask = (df_exp['modifier_RT'] >= lower) & (df_exp['modifier_RT'] <= upper)
    df_filtered = df_exp[mask]
    hate_sems.append(df_filtered[df_filtered['emotion'] == 'H']['modifier_RT'].sem())
    neutral_sems.append(df_filtered[df_filtered['emotion'] == 'N']['modifier_RT'].sem())

bars1 = ax4.bar(x_pos - width/2, hate_means, width, yerr=hate_sems,
                label='Hate', color='lightcoral', capsize=5, edgecolor='black')
bars2 = ax4.bar(x_pos + width/2, neutral_means, width, yerr=neutral_sems,
                label='Neutral', color='lightblue', capsize=5, edgecolor='black')

ax4.set_ylabel('Mean Modifier RT (ms)', fontsize=11)
ax4.set_xlabel('Exclusion Criterion', fontsize=11)
ax4.set_title('Mean RT Comparison (±SEM)', fontsize=12, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(['Original\n(200-3000ms)', 'Stricter\n(200-1600ms)'])
ax4.legend()
ax4.grid(alpha=0.3, axis='y')

# Add significance stars
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
plt.savefig('result_1201/outlier_exclusion_comparison.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: result_1201/outlier_exclusion_comparison.png")

# Generate text summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

with open('result_1201/outlier_exclusion_summary.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("OUTLIER EXCLUSION COMPARISON - result_1201\n")
    f.write("="*60 + "\n\n")

    for result in results:
        f.write(f"{result['Criterion']}\n")
        f.write(f"  Range: {result['Lower_bound']}-{result['Upper_bound']}ms\n")
        f.write(f"  Excluded: {result['N_excluded']} trials ({result['Pct_excluded']:.1f}%)\n")
        f.write(f"  Retained: {result['N_retained']} trials\n")
        f.write(f"  Mean Hate RT: {result['Mean_Hate']:.2f}ms (N={result['N_hate']})\n")
        f.write(f"  Mean Neutral RT: {result['Mean_Neutral']:.2f}ms (N={result['N_neutral']})\n")
        f.write(f"  Difference: {result['Difference']:.2f}ms\n")
        f.write(f"  t({result['N_hate']+result['N_neutral']-2}) = {result['t_stat']:.4f}, p = {result['p_value']:.4f}\n")
        f.write(f"  Cohen's d = {result['cohens_d']:.4f}\n")
        f.write("\n")

    f.write("="*60 + "\n")
    f.write("RECOMMENDATION\n")
    f.write("="*60 + "\n")

    # Compare effect sizes
    orig_d = results[0]['cohens_d']
    strict_d = results[1]['cohens_d']

    f.write(f"\nEffect size change: d = {orig_d:.4f} → {strict_d:.4f}\n")
    f.write(f"Difference in Cohen's d: {strict_d - orig_d:.4f}\n\n")

    if abs(strict_d - orig_d) < 0.05:
        f.write("✓ Results are ROBUST across criteria\n")
        f.write("  → Recommend using Original (200-3000ms) for maximum statistical power\n")
    else:
        f.write("⚠ Results DIFFER substantially between criteria\n")
        f.write("  → Recommend using Stricter (200-1600ms) to ensure data quality\n")
        f.write("  → Report both as sensitivity analysis\n")

print("Summary saved to: result_1201/outlier_exclusion_summary.txt")
print("\n✓ All analyses complete!")
