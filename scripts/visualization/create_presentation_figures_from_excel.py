"""
Create two presentation-ready figures from Excel data:
1. Combined histogram: Original distribution + Strict criterion overlay
2. RT distribution boxplot: Strict criterion only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

def parse_spr_data(excel_path):
    """Parse SPR data from Excel file and extract modifier RTs"""

    print(f"Loading data from: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name='SPR_Data')

    print(f"Loaded {len(df)} trials")
    print(f"Participants: {df['Participant_ID'].nunique()}")

    # Parse region data to extract modifier RT
    modifier_rts = []

    for idx, row in df.iterrows():
        # Skip fillers
        if row['Is_Filler'] == 1:
            continue

        # Parse regions and RTs
        try:
            regions = json.loads(row['Regions']) if isinstance(row['Regions'], str) else row['Regions']
            rts = json.loads(row['Region_RTs']) if isinstance(row['Region_RTs'], str) else row['Region_RTs']

            # For experimental items, modifier should be at index 1 (after subject)
            # Structure: ["탈렌족은", "미개한", "민족으로,", ...]
            if len(regions) >= 2 and len(rts) >= 2:
                modifier_rts.append({
                    'participant': row['Participant_ID'],
                    'item_id': row['Item_ID'],
                    'base': row['Base'],
                    'emotion': row['Emotion'],
                    'plausibility': row['Plausibility'],
                    'modifier_RT': rts[1]  # Index 1 is the modifier
                })
        except Exception as e:
            print(f"Error parsing row {idx}: {e}")
            continue

    df_modifier = pd.DataFrame(modifier_rts)
    print(f"\nExtracted {len(df_modifier)} modifier RTs")
    if len(df_modifier) > 0:
        print(f"RT range: {df_modifier['modifier_RT'].min():.0f} - {df_modifier['modifier_RT'].max():.0f} ms")
    else:
        print("ERROR: No modifier RTs extracted!")

    return df_modifier

def create_combined_histogram(df, output_path):
    """
    Figure 1: Combined histogram showing:
    - Complete distribution (ALL data including >3000ms)
    - Strict criterion overlay (200-1600ms highlighted)
    """

    # Use ALL data (no upper bound filtering)
    df_all = df.copy()

    # Apply strict criterion (200-1600ms)
    df_strict = df[(df['modifier_RT'] >= 200) & (df['modifier_RT'] <= 1600)].copy()

    print(f"\nComplete distribution (all data): {len(df_all)} observations")
    print(f"Strict criterion (200-1600ms): {len(df_strict)} observations")
    print(f"Excluded: {len(df_all) - len(df_strict)} observations ({100*(len(df_all)-len(df_strict))/len(df_all):.1f}%)")

    # Determine max RT for plot range
    max_rt = df_all['modifier_RT'].max()
    plot_max = min(max_rt + 200, 5000)  # Cap at 5000ms for readability

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot complete distribution (lighter color)
    ax.hist(df_all['modifier_RT'], bins=60, range=(0, plot_max),
            alpha=0.4, color='gray', edgecolor='black', linewidth=0.5)

    # Plot strict criterion (highlighted color)
    ax.hist(df_strict['modifier_RT'], bins=40, range=(200, 1600),
            alpha=0.7, color='#2ca02c', edgecolor='black', linewidth=0.5)

    # Add vertical lines for boundaries
    ax.axvline(x=200, color='blue', linestyle='--', linewidth=2.5, zorder=10)
    ax.axvline(x=1600, color='red', linestyle='--', linewidth=3, zorder=10)

    # Add shaded regions for excluded areas
    n_below_200 = len(df_all[df_all['modifier_RT'] < 200])
    if n_below_200 > 0:
        ax.axvspan(0, 200, alpha=0.15, color='orange')

    n_above_1600 = len(df_all[df_all['modifier_RT'] > 1600])
    if plot_max > 1800:
        ax.axvspan(1600, plot_max, alpha=0.15, color='red')

    ax.set_xlabel('Modifier RT (ms)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
    ax.set_title('Outlier Exclusion: Complete Distribution vs. Strict Criterion\nModifier Region RT Distribution',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_path}")
    plt.close()

def create_boxplot_by_condition(df, output_path):
    """
    Figure 2: RT distribution boxplot by emotion condition
    Using strict criterion (200-1600ms) only
    Simple boxplot without statistics
    """

    # Apply strict criterion (200-1600ms)
    df_strict = df[(df['modifier_RT'] >= 200) & (df['modifier_RT'] <= 1600)].copy()

    # Map emotion labels
    df_strict['Emotion_Label'] = df_strict['emotion'].map({'H': 'Hate', 'N': 'Neutral'})

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create boxplot
    sns.boxplot(data=df_strict, x='Emotion_Label', y='modifier_RT', ax=ax,
                palette={'Hate': '#d62728', 'Neutral': '#2ca02c'},
                width=0.6, linewidth=2.5)

    ax.set_xlabel('Emotion Condition', fontsize=14, fontweight='bold')
    ax.set_ylabel('Reaction Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('RT Distribution by Emotion Condition (Modifier Region)\nStrict Criterion: 200-1600ms',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()

def main():
    """Main execution"""

    print("\n" + "="*70)
    print("Creating Presentation Figures from Excel Data")
    print("="*70)

    # Load data
    print("\n[1/3] Parsing SPR data from Excel...")
    excel_path = Path('result_1201/ExpLing_Project.xlsx')

    if not excel_path.exists():
        print(f"\nError: Excel file not found at {excel_path}")
        return

    df = parse_spr_data(excel_path)

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

    print("\n" + "="*70)
    print("All figures created successfully!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
