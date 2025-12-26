"""
Comprehensive Analysis Script for Experimental Linguistics Term Project
Based on hypotheses specified in CLAUDE.md
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.family'] = 'DejaVu Sans'

def load_data():
    """Load all experimental data sheets"""
    xl = pd.ExcelFile('result_1128/ExpLing_Project.xlsx')

    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name=sheet)

    return data

def parse_spr_regions(df):
    """
    Parse SPR data to extract reading times by region.
    Assumes sentence structure: [modifier1] [modifier2] [noun] [spillover1] [spillover2] ...
    """
    # Convert string representation of lists to actual lists
    df['Regions_List'] = df['Regions'].apply(eval)
    df['RT_List'] = df['Region_RTs'].apply(eval)

    parsed_rows = []

    for idx, row in df.iterrows():
        regions = row['Regions_List']
        rts = row['RT_List']

        # Create a record for each region
        for i, (region_text, rt) in enumerate(zip(regions, rts)):
            parsed_row = {
                'Participant_ID': row['Participant_ID'],
                'List_ID': row['List_ID'],
                'Trial_Index': row['Trial_Index'],
                'Item_ID': row['Item_ID'],
                'Base': row['Base'],
                'Emotion': row['Emotion'],
                'Plausibility': row['Plausibility'],
                'Version': row['Version'],
                'Is_Filler': row['Is_Filler'],
                'Region_Index': i,
                'Region_Text': region_text,
                'RT': rt,
                'Total_RT': row['Total_Reading_Time_ms']
            }

            # Classify region type based on position
            # First 1-2 regions: modifiers, then noun, then spillover
            if i <= 1:
                parsed_row['Region_Type'] = 'Modifier'
                parsed_row['Region_Position'] = f'Modifier_{i+1}'
            elif i == 2:
                parsed_row['Region_Type'] = 'Noun'
                parsed_row['Region_Position'] = 'Critical_Noun'
            else:
                parsed_row['Region_Type'] = 'Spillover'
                parsed_row['Region_Position'] = f'Spillover_{i-2}'

            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)

def remove_outliers(df, rt_col='RT', lower_bound=200, upper_bound=3000):
    """Remove outliers based on RT thresholds"""
    before = len(df)
    df_clean = df[(df[rt_col] >= lower_bound) & (df[rt_col] <= upper_bound)].copy()
    after = len(df_clean)
    print(f"Removed {before - after} outliers ({(before-after)/before*100:.1f}%) from {before} observations")
    return df_clean

def test_h1_attention_capture(spr_parsed):
    """
    H1: Hate-modifier sentences will show longer reading times at the hate modifier
    than at neutral modifiers (affect-driven attentional capture)
    """
    print("\n" + "="*80)
    print("H1: ATTENTION CAPTURE AT HATE MODIFIER")
    print("="*80)

    # Filter to modifier regions only, excluding fillers
    modifier_data = spr_parsed[
        (spr_parsed['Region_Type'] == 'Modifier') &
        (spr_parsed['Is_Filler'] == 0)
    ].copy()

    # Clean outliers
    modifier_data = remove_outliers(modifier_data)

    # Descriptive statistics
    print("\nDescriptive Statistics (Modifier RT by Emotion):")
    desc = modifier_data.groupby('Emotion')['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(desc)

    # Mixed effects model: RT ~ Emotion + (1|Participant) + (1|Base)
    try:
        model = mixedlm("RT ~ C(Emotion)",
                       modifier_data,
                       groups=modifier_data["Participant_ID"],
                       re_formula="1")
        result = model.fit(method='powell')
        print("\nMixed Effects Model: RT ~ Emotion + (1|Participant)")
        print(result.summary())
    except Exception as e:
        print(f"\nMixed model failed: {e}")
        print("Falling back to t-test...")

        # Paired t-test at participant level
        hate_rt = modifier_data[modifier_data['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
        neutral_rt = modifier_data[modifier_data['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

        t_stat, p_val = stats.ttest_rel(hate_rt, neutral_rt)
        print(f"\nPaired t-test: t={t_stat:.3f}, p={p_val:.4f}")
        print(f"Mean difference (H-N): {hate_rt.mean() - neutral_rt.mean():.1f} ms")

    return modifier_data

def test_h2_attention_narrowing(spr_parsed):
    """
    H2: Attention narrowing & shallow integration
    - Neutral condition should show clear plausibility effect (I > P)
    - Hate condition should show reduced plausibility effect
    At critical noun and spillover regions
    """
    print("\n" + "="*80)
    print("H2: ATTENTION NARROWING (Reduced Plausibility Effect in Hate Condition)")
    print("="*80)

    # Filter to critical noun and spillover regions
    critical_data = spr_parsed[
        (spr_parsed['Region_Type'].isin(['Noun', 'Spillover'])) &
        (spr_parsed['Is_Filler'] == 0)
    ].copy()

    critical_data = remove_outliers(critical_data)

    # Descriptive statistics
    print("\nDescriptive Statistics (RT by Emotion × Plausibility):")
    desc = critical_data.groupby(['Emotion', 'Plausibility'])['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(desc)

    # Calculate plausibility effect separately for each emotion
    print("\nPlausibility Effect (Implausible - Plausible):")
    for emotion in ['H', 'N']:
        emotion_data = critical_data[critical_data['Emotion'] == emotion]
        plaus_rt = emotion_data[emotion_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        implaus_rt = emotion_data[emotion_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        effect = implaus_rt.mean() - plaus_rt.mean()
        t_stat, p_val = stats.ttest_rel(implaus_rt, plaus_rt)

        print(f"  {emotion}: {effect:.1f} ms (t={t_stat:.3f}, p={p_val:.4f})")

    # Test interaction: Emotion × Plausibility
    try:
        model = mixedlm("RT ~ C(Emotion) * C(Plausibility)",
                       critical_data,
                       groups=critical_data["Participant_ID"],
                       re_formula="1")
        result = model.fit(method='powell')
        print("\nMixed Effects Model: RT ~ Emotion × Plausibility + (1|Participant)")
        print(result.summary())
    except Exception as e:
        print(f"\nMixed model failed: {e}")
        print("Performing 2-way repeated measures ANOVA-style analysis...")

        # Create aggregated data for 2-way ANOVA
        agg_data = critical_data.groupby(['Participant_ID', 'Emotion', 'Plausibility'])['RT'].mean().reset_index()

        # Calculate interaction effect manually
        hp = agg_data[(agg_data['Emotion']=='H') & (agg_data['Plausibility']=='P')]['RT']
        hi = agg_data[(agg_data['Emotion']=='H') & (agg_data['Plausibility']=='I')]['RT']
        np_data = agg_data[(agg_data['Emotion']=='N') & (agg_data['Plausibility']=='P')]['RT']
        ni = agg_data[(agg_data['Emotion']=='N') & (agg_data['Plausibility']=='I')]['RT']

        hate_effect = hi.mean() - hp.mean()
        neutral_effect = ni.mean() - np_data.mean()
        interaction = hate_effect - neutral_effect

        print(f"\nInteraction (reduction in plausibility effect): {interaction:.1f} ms")

    return critical_data

def test_h3_memory_bias(rating_data):
    """
    H3: Biased memory / trade-off + distortion
    - Lower accuracy for neutral/factual statements in hate context
    - Higher false alarm rates for hate-consistent lures
    """
    print("\n" + "="*80)
    print("H3: MEMORY BIAS (Accuracy and False Alarms)")
    print("="*80)

    # Check what rating data contains
    print("\nRating Data Overview:")
    print(rating_data.head(10))
    print(f"\nUnique values in Rating column: {rating_data['Rating'].dropna().unique()}")

    # Analyze rating patterns by condition
    if 'Rating' in rating_data.columns:
        print("\nRating Distribution by Emotion:")
        rating_by_emotion = rating_data.groupby(['Emotion', 'Rating']).size().unstack(fill_value=0)
        print(rating_by_emotion)

        print("\nMean Rating by Emotion and Plausibility:")
        mean_ratings = rating_data.groupby(['Emotion', 'Plausibility'])['Rating'].agg(['mean', 'std', 'count'])
        print(mean_ratings)

    return rating_data

def test_manipulation_check(manip_data):
    """
    Validate manipulation: Hate modifiers should be rated as more negative than neutral
    """
    print("\n" + "="*80)
    print("MANIPULATION CHECK: Negativity Ratings")
    print("="*80)

    print("\nDescriptive Statistics:")
    desc = manip_data.groupby('Modifier_Category')['Negativity_Rating'].agg(['mean', 'std', 'count', 'sem'])
    print(desc)

    # Statistical test
    hate_ratings = manip_data[manip_data['Modifier_Category'] == 'hate']['Negativity_Rating']
    neutral_ratings = manip_data[manip_data['Modifier_Category'] == 'neutral']['Negativity_Rating']

    # Independent samples t-test (if different items)
    t_stat, p_val = stats.ttest_ind(hate_ratings, neutral_ratings)
    print(f"\nIndependent t-test: t={t_stat:.3f}, p={p_val:.4f}")
    print(f"Mean difference (H-N): {hate_ratings.mean() - neutral_ratings.mean():.2f}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((hate_ratings.std()**2 + neutral_ratings.std()**2) / 2)
    cohens_d = (hate_ratings.mean() - neutral_ratings.mean()) / pooled_std
    print(f"Effect size (Cohen's d): {cohens_d:.3f}")

    return manip_data

def visualize_results(spr_parsed, modifier_data, critical_data, manip_data):
    """Create comprehensive visualizations"""
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)

    # Figure 1: Reading time by region position
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1a. Mean RT by region position (all conditions)
    ax = axes[0, 0]
    region_order = ['Modifier_1', 'Modifier_2', 'Critical_Noun', 'Spillover_1', 'Spillover_2']

    # Filter to first 5 positions for clarity
    plot_data = spr_parsed[
        (spr_parsed['Region_Position'].isin(region_order)) &
        (spr_parsed['Is_Filler'] == 0)
    ].copy()

    # Clean outliers
    plot_data = remove_outliers(plot_data)

    sns.pointplot(data=plot_data, x='Region_Position', y='RT',
                 order=region_order, errorbar='se', ax=ax, color='black')
    ax.set_xlabel('Region Position', fontsize=12)
    ax.set_ylabel('Reading Time (ms)', fontsize=12)
    ax.set_title('Mean Reading Time by Region Position', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)

    # 1b. H1: Modifier RT by Emotion
    ax = axes[0, 1]
    sns.barplot(data=modifier_data, x='Emotion', y='RT', errorbar='se', ax=ax, palette='Set2')
    ax.set_xlabel('Emotion Condition', fontsize=12)
    ax.set_ylabel('Reading Time (ms)', fontsize=12)
    ax.set_title('H1: Modifier Reading Time by Emotion', fontsize=14, fontweight='bold')
    ax.set_xticklabels(['Hate (H)', 'Neutral (N)'])

    # 1c. H2: Interaction plot
    ax = axes[1, 0]
    interaction_data = critical_data.groupby(['Participant_ID', 'Emotion', 'Plausibility'])['RT'].mean().reset_index()

    sns.pointplot(data=interaction_data, x='Plausibility', y='RT', hue='Emotion',
                 errorbar='se', ax=ax, palette='Set1', markers=['o', 's'], linestyles=['-', '--'])
    ax.set_xlabel('Plausibility', fontsize=12)
    ax.set_ylabel('Reading Time (ms)', fontsize=12)
    ax.set_title('H2: Emotion × Plausibility Interaction (Noun + Spillover)', fontsize=14, fontweight='bold')
    ax.set_xticklabels(['Plausible (P)', 'Implausible (I)'])
    ax.legend(title='Emotion', labels=['Hate (H)', 'Neutral (N)'])

    # 1d. Manipulation check
    ax = axes[1, 1]
    sns.violinplot(data=manip_data, x='Modifier_Category', y='Negativity_Rating', ax=ax, palette='Set3')
    sns.swarmplot(data=manip_data, x='Modifier_Category', y='Negativity_Rating',
                 ax=ax, color='black', alpha=0.3, size=3)
    ax.set_xlabel('Modifier Category', fontsize=12)
    ax.set_ylabel('Negativity Rating', fontsize=12)
    ax.set_title('Manipulation Check: Negativity Ratings', fontsize=14, fontweight='bold')
    ax.set_xticklabels(['Hate (H)', 'Neutral (N)'])

    plt.tight_layout()
    plt.savefig('result_1128/analysis_plots.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/analysis_plots.png")

    # Figure 2: Distribution plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 2a. RT distribution by emotion (modifier)
    ax = axes[0]
    modifier_data[modifier_data['Emotion']=='H']['RT'].hist(bins=30, alpha=0.5, label='Hate', ax=ax, color='red')
    modifier_data[modifier_data['Emotion']=='N']['RT'].hist(bins=30, alpha=0.5, label='Neutral', ax=ax, color='blue')
    ax.set_xlabel('Reading Time (ms)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('RT Distribution: Modifier Region', fontsize=14, fontweight='bold')
    ax.legend()

    # 2b. RT distribution by plausibility (critical region)
    ax = axes[1]
    critical_data[critical_data['Plausibility']=='P']['RT'].hist(bins=30, alpha=0.5, label='Plausible', ax=ax, color='green')
    critical_data[critical_data['Plausibility']=='I']['RT'].hist(bins=30, alpha=0.5, label='Implausible', ax=ax, color='orange')
    ax.set_xlabel('Reading Time (ms)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('RT Distribution: Critical Noun + Spillover', fontsize=14, fontweight='bold')
    ax.legend()

    # 2c. Negativity rating distribution
    ax = axes[2]
    manip_data[manip_data['Modifier_Category']=='hate']['Negativity_Rating'].hist(bins=7, alpha=0.5, label='Hate', ax=ax, color='red')
    manip_data[manip_data['Modifier_Category']=='neutral']['Negativity_Rating'].hist(bins=7, alpha=0.5, label='Neutral', ax=ax, color='blue')
    ax.set_xlabel('Negativity Rating', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Negativity Rating Distribution', fontsize=14, fontweight='bold')
    ax.legend()

    plt.tight_layout()
    plt.savefig('result_1128/distribution_plots.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/distribution_plots.png")

    plt.close('all')

def analyze_secondary_metrics(spr_data, manip_data, metadata):
    """Analyze secondary metrics like manipulation check RT"""
    print("\n" + "="*80)
    print("SECONDARY METRICS")
    print("="*80)

    # Manipulation check RT
    print("\nManipulation Check RT by Category:")
    manip_rt = manip_data.groupby('Modifier_Category')['RT_ms'].agg(['mean', 'std', 'count', 'sem'])
    print(manip_rt)

    hate_rt = manip_data[manip_data['Modifier_Category'] == 'hate']['RT_ms']
    neutral_rt = manip_data[manip_data['Modifier_Category'] == 'neutral']['RT_ms']
    t_stat, p_val = stats.ttest_ind(hate_rt, neutral_rt)
    print(f"\nt-test: t={t_stat:.3f}, p={p_val:.4f}")

    # Overall experiment metrics
    print("\n\nOverall Experiment Metrics:")
    print(f"Total participants: {metadata['Participant_ID'].nunique()}")
    print(f"Mean total duration: {metadata['Total_Experiment_Duration_ms'].mean()/1000/60:.1f} minutes")
    print(f"Mean background reading time: {metadata['Background_Reading_Time_ms'].mean()/1000:.1f} seconds")

def main():
    """Main analysis pipeline"""
    print("="*80)
    print("EXPERIMENTAL LINGUISTICS TERM PROJECT - DATA ANALYSIS")
    print("="*80)

    # Load data
    print("\nLoading data...")
    data = load_data()

    spr_data = data['SPR_Data']
    rating_data = data['Rating_Data']
    manip_data = data['Manipulation_Check']
    recall_data = data['Recall_Data']
    metadata = data['Metadata']

    print(f"\nData loaded successfully:")
    print(f"  - SPR trials: {len(spr_data)}")
    print(f"  - Rating trials: {len(rating_data)}")
    print(f"  - Manipulation checks: {len(manip_data)}")
    print(f"  - Recall responses: {len(recall_data)}")
    print(f"  - Participants: {metadata['Participant_ID'].nunique()}")

    # Parse SPR data
    print("\nParsing SPR regions...")
    spr_parsed = parse_spr_regions(spr_data)
    print(f"Total region observations: {len(spr_parsed)}")

    # Run hypothesis tests
    modifier_data = test_h1_attention_capture(spr_parsed)
    critical_data = test_h2_attention_narrowing(spr_parsed)
    test_h3_memory_bias(rating_data)
    test_manipulation_check(manip_data)

    # Secondary metrics
    analyze_secondary_metrics(spr_data, manip_data, metadata)

    # Visualizations
    visualize_results(spr_parsed, modifier_data, critical_data, manip_data)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - result_1128/analysis_plots.png")
    print("  - result_1128/distribution_plots.png")

if __name__ == "__main__":
    main()
