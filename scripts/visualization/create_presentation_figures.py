"""
Create two presentation-ready figures:
1. Combined histogram: Original distribution + Strict criterion overlay
2. RT distribution boxplot: Strict criterion only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

def load_spr_data():
    """Load SPR data from result_1201 directory"""
    # Try different possible file names
    data_dir = Path('result_1201')

    possible_files = [
        'spr_cleaned.csv',
        'spr_data.csv',
        'cleaned_spr_data.csv',
        'modifier_rt_data.csv'
    ]

    for fname in possible_files:
        fpath = data_dir / fname
        if fpath.exists():
            print(f"Loading data from: {fpath}")
            return pd.read_csv(fpath)

    # If no file found, print available files
    print(f"No SPR data file found. Available files in {data_dir}:")
    for f in data_dir.glob('*.csv'):
        print(f"  - {f.name}")
    return None

def create_combined_histogram(df, output_path):
    """
    Figure 1: Combined histogram showing:
    - Original distribution (all data 200-3000ms)
    - Strict criterion overlay (200-1600ms highlighted)
    """

    # Filter for modifier region only
    if 'region' in df.columns:
        df_modifier = df[df['region'] == 'modifier'].copy()
    else:
        print("Warning: 'region' column not found. Using all data.")
        df_modifier = df.copy()

    # Apply original criterion (200-3000ms)
    df_original = df_modifier[(df_modifier['RT'] >= 200) & (df_modifier['RT'] <= 3000)].copy()

    # Apply strict criterion (200-1600ms)
    df_strict = df_modifier[(df_modifier['RT'] >= 200) & (df_modifier['RT'] <= 1600)].copy()

    print(f"\nOriginal criterion (200-3000ms): {len(df_original)} observations")
    print(f"Strict criterion (200-1600ms): {len(df_strict)} observations")
    print(f"Excluded: {len(df_original) - len(df_strict)} observations ({100*(len(df_original)-len(df_strict))/len(df_original):.1f}%)")

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot original distribution (lighter color)
    ax.hist(df_original['RT'], bins=50, range=(200, 3000),
            alpha=0.4, color='gray', label='Original (200-3000ms)', edgecolor='black')

    # Plot strict criterion (highlighted color)
    ax.hist(df_strict['RT'], bins=40, range=(200, 1600),
            alpha=0.7, color='#2ca02c', label='Strict criterion (200-1600ms)', edgecolor='black')

    # Add vertical line at 1600ms cutoff
    ax.axvline(x=1600, color='red', linestyle='--', linewidth=2.5,
               label='Strict upper bound (1600ms)', zorder=10)

    # Add annotations
    y_max = ax.get_ylim()[1]

    # Annotation for excluded region
    ax.axvspan(1600, 3000, alpha=0.2, color='red', label='Excluded region')
    ax.text(2300, y_max * 0.85, f'Excluded\n{len(df_original) - len(df_strict)} obs\n({100*(len(df_original)-len(df_strict))/len(df_original):.1f}%)',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='red', linewidth=2))

    # Annotation for retained region
    ax.text(900, y_max * 0.85, f'Retained\n{len(df_strict)} obs\n({100*len(df_strict)/len(df_original):.1f}%)',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, edgecolor='green', linewidth=2))

    ax.set_xlabel('Modifier RT (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Outlier Exclusion: Original vs. Strict Criterion\nModifier Region RT Distribution',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_path}")
    plt.close()

def create_boxplot_by_condition(df, output_path):
    """
    Figure 2: RT distribution boxplot by emotion condition
    Using strict criterion (200-1600ms) only
    """

    # Filter for modifier region only
    if 'region' in df.columns:
        df_modifier = df[df['region'] == 'modifier'].copy()
    else:
        df_modifier = df.copy()

    # Apply strict criterion (200-1600ms)
    df_strict = df_modifier[(df_modifier['RT'] >= 200) & (df_modifier['RT'] <= 1600)].copy()

    # Map emotion labels
    if 'emotion' in df_strict.columns:
        df_strict['Emotion_Label'] = df_strict['emotion'].map({'H': 'Hate', 'N': 'Neutral'})
    else:
        print("Warning: 'emotion' column not found")
        return

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create boxplot with individual points
    sns.boxplot(data=df_strict, x='Emotion_Label', y='RT', ax=ax,
                palette={'Hate': '#d62728', 'Neutral': '#2ca02c'},
                width=0.5, linewidth=2)

    # Add individual points with jitter
    sns.stripplot(data=df_strict, x='Emotion_Label', y='RT', ax=ax,
                  color='black', alpha=0.3, size=4, jitter=0.2)

    # Calculate and display statistics
    stats_text = []
    for emotion_label in ['Hate', 'Neutral']:
        data = df_strict[df_strict['Emotion_Label'] == emotion_label]['RT']
        mean_rt = data.mean()
        median_rt = data.median()
        std_rt = data.std()
        n = len(data)

        stats_text.append(f"{emotion_label}:\n  n = {n}\n  Mean = {mean_rt:.1f} ms\n  Median = {median_rt:.1f} ms\n  SD = {std_rt:.1f} ms")

    # Add statistics box
    textstr = '\n\n'.join(stats_text)
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, linewidth=1.5))

    # Calculate mean difference
    mean_hate = df_strict[df_strict['Emotion_Label'] == 'Hate']['RT'].mean()
    mean_neutral = df_strict[df_strict['Emotion_Label'] == 'Neutral']['RT'].mean()
    diff = mean_hate - mean_neutral

    # Add mean difference annotation
    ax.text(0.5, 0.05, f'Mean difference (Hate - Neutral) = {diff:.1f} ms',
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, linewidth=2))

    ax.set_xlabel('Emotion Condition', fontsize=12, fontweight='bold')
    ax.set_ylabel('Reaction Time (ms)', fontsize=12, fontweight='bold')
    ax.set_title('RT Distribution by Emotion Condition (Modifier Region)\nStrict Criterion: 200-1600ms',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()

def main():
    """Main execution"""

    print("\n" + "="*60)
    print("Creating Presentation Figures")
    print("="*60)

    # Load data
    print("\n[1/3] Loading SPR data...")
    df = load_spr_data()

    if df is None:
        print("\nError: Could not load SPR data.")
        print("Please ensure your data file is in the result_1201/ directory")
        print("Required columns: RT, region (optional), emotion (optional)")
        return

    print(f"Loaded {len(df)} observations")
    print(f"Columns: {df.columns.tolist()}")

    # Create output directory
    output_dir = Path('result_1201')
    output_dir.mkdir(exist_ok=True)

    # Figure 1: Combined histogram
    print("\n[2/3] Creating combined histogram...")
    output_path1 = output_dir / 'combined_histogram_strict_criterion.png'
    create_combined_histogram(df, output_path1)

    # Figure 2: Boxplot by condition
    print("\n[3/3] Creating RT distribution boxplot...")
    output_path2 = output_dir / 'boxplot_rt_by_emotion_strict.png'
    create_boxplot_by_condition(df, output_path2)

    print("\n" + "="*60)
    print("All figures created successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
