"""
H3: Memory Bias Analysis
- Emotion × Plausibility effects on recognition memory ratings
- Higher rating = more plausible/confident it was presented
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def analyze_h3():
    """
    H3 가설:
    혐오 맥락에서:
    (a) 중립적/사실적 진술에 대한 정확도 감소 (낮은 rating)
    (b) 혐오 일치 lure에 대한 오경보율 증가 (높은 rating?)

    하지만 현재 데이터는 old/new 구분이 없으므로,
    대신 Emotion × Plausibility 효과를 검증:
    - 혐오 맥락에서 plausibility rating이 왜곡되는지 확인
    """

    print("="*80)
    print("H3: MEMORY BIAS ANALYSIS")
    print("="*80)

    # Load data
    rating = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='Rating_Data')

    print(f"\nTotal observations: {len(rating)}")
    print(f"Missing ratings: {rating['Rating'].isna().sum()} ({rating['Rating'].isna().sum()/len(rating)*100:.1f}%)")

    # Remove NaN
    rating_clean = rating[rating['Rating'].notna()].copy()
    print(f"Clean observations: {len(rating_clean)}")

    # Descriptive statistics
    print("\n" + "="*80)
    print("Descriptive Statistics: Rating by Emotion × Plausibility")
    print("="*80)

    desc = rating_clean.groupby(['Emotion', 'Plausibility'])['Rating'].agg([
        'count', 'mean', 'std', 'sem', 'min', 'max'
    ])
    print("\n", desc)

    # Main effects and interaction
    print("\n" + "="*80)
    print("Statistical Tests")
    print("="*80)

    # 1. Main effect of Emotion
    print("\n1. Main Effect of Emotion:")
    hate_ratings = rating_clean[rating_clean['Emotion'] == 'H']['Rating']
    neutral_ratings = rating_clean[rating_clean['Emotion'] == 'N']['Rating']

    t_stat, p_val = stats.ttest_ind(hate_ratings, neutral_ratings)
    print(f"   Hate mean: {hate_ratings.mean():.3f}")
    print(f"   Neutral mean: {neutral_ratings.mean():.3f}")
    print(f"   Difference: {hate_ratings.mean() - neutral_ratings.mean():.3f}")
    print(f"   t({len(hate_ratings)+len(neutral_ratings)-2}) = {t_stat:.3f}, p = {p_val:.4f}")

    # 2. Main effect of Plausibility
    print("\n2. Main Effect of Plausibility:")
    plaus_ratings = rating_clean[rating_clean['Plausibility'] == 'P']['Rating']
    implaus_ratings = rating_clean[rating_clean['Plausibility'] == 'I']['Rating']

    t_stat, p_val = stats.ttest_ind(plaus_ratings, implaus_ratings)
    print(f"   Plausible mean: {plaus_ratings.mean():.3f}")
    print(f"   Implausible mean: {implaus_ratings.mean():.3f}")
    print(f"   Difference: {plaus_ratings.mean() - implaus_ratings.mean():.3f}")
    print(f"   t({len(plaus_ratings)+len(implaus_ratings)-2}) = {t_stat:.3f}, p = {p_val:.4f}")

    # 3. Interaction: Emotion × Plausibility
    print("\n3. Interaction Test:")
    print("\n   Plausibility effect by Emotion:")

    for emotion in ['H', 'N']:
        emotion_data = rating_clean[rating_clean['Emotion'] == emotion]
        p_ratings = emotion_data[emotion_data['Plausibility'] == 'P']['Rating']
        i_ratings = emotion_data[emotion_data['Plausibility'] == 'I']['Rating']

        effect = p_ratings.mean() - i_ratings.mean()
        t_stat, p_val = stats.ttest_ind(p_ratings, i_ratings)

        print(f"   {emotion}: {effect:.3f} (P - I) [t = {t_stat:.3f}, p = {p_val:.4f}]")

    # Calculate interaction
    hp = rating_clean[(rating_clean['Emotion']=='H') & (rating_clean['Plausibility']=='P')]['Rating'].mean()
    hi = rating_clean[(rating_clean['Emotion']=='H') & (rating_clean['Plausibility']=='I')]['Rating'].mean()
    np_val = rating_clean[(rating_clean['Emotion']=='N') & (rating_clean['Plausibility']=='P')]['Rating'].mean()
    ni = rating_clean[(rating_clean['Emotion']=='N') & (rating_clean['Plausibility']=='I')]['Rating'].mean()

    hate_effect = hp - hi
    neutral_effect = np_val - ni
    interaction = hate_effect - neutral_effect

    print(f"\n   Interaction (difference in plausibility effects): {interaction:.3f}")
    print(f"   (Negative = plausibility effect reduced in hate condition)")

    # 4. Mixed Effects Model
    print("\n4. Mixed Effects Model:")
    print("   Formula: Rating ~ Emotion * Plausibility + (1|Participant) + (1|Item)")

    try:
        # Add item random effect
        model = mixedlm("Rating ~ C(Emotion) * C(Plausibility)",
                       rating_clean,
                       groups=rating_clean["Participant_ID"],
                       re_formula="1")
        result = model.fit(method='powell')
        print("\n", result.summary())

    except Exception as e:
        print(f"\n   Mixed model failed: {e}")
        print("   Falling back to 2-way ANOVA...")

        # Manual 2-way ANOVA calculation
        from scipy import stats as sp_stats

        # Reshape for ANOVA
        emotion_codes = rating_clean['Emotion'].map({'H': 0, 'N': 1})
        plaus_codes = rating_clean['Plausibility'].map({'I': 0, 'P': 1})

        # F-tests for each factor
        print("\n   Approximate 2-way ANOVA results:")

        # Main effect of Emotion
        f_emotion, p_emotion = sp_stats.f_oneway(
            rating_clean[rating_clean['Emotion']=='H']['Rating'],
            rating_clean[rating_clean['Emotion']=='N']['Rating']
        )
        print(f"   Emotion: F(1, {len(rating_clean)-2}) = {f_emotion:.3f}, p = {p_emotion:.4f}")

        # Main effect of Plausibility
        f_plaus, p_plaus = sp_stats.f_oneway(
            rating_clean[rating_clean['Plausibility']=='I']['Rating'],
            rating_clean[rating_clean['Plausibility']=='P']['Rating']
        )
        print(f"   Plausibility: F(1, {len(rating_clean)-2}) = {f_plaus:.3f}, p = {p_plaus:.4f}")

    # 5. By-participant analysis
    print("\n\n5. By-Participant Analysis:")
    participant_summary = rating_clean.groupby(['Participant_ID', 'Emotion', 'Plausibility'])['Rating'].mean().reset_index()

    print("\n   Mean ratings by participant and condition:")
    pivot_table = participant_summary.pivot_table(
        index='Participant_ID',
        columns=['Emotion', 'Plausibility'],
        values='Rating'
    )
    print(pivot_table)

    return rating_clean

def create_h3_visualizations(rating_clean):
    """Create visualizations for H3"""

    print("\n\nCreating H3 visualizations...")

    # Figure 1: Main visualization (2x2 + distributions)
    fig = plt.figure(figsize=(18, 6))

    # Panel 1: 2x2 bar plot
    ax1 = plt.subplot(1, 3, 1)

    summary = rating_clean.groupby(['Emotion', 'Plausibility'])['Rating'].agg(['mean', 'sem']).reset_index()
    summary['Condition'] = summary['Emotion'] + summary['Plausibility']
    condition_map = {
        'HP': 'Hate-Plausible',
        'HI': 'Hate-Implausible',
        'NP': 'Neutral-Plausible',
        'NI': 'Neutral-Implausible'
    }
    summary['Condition_Label'] = summary['Condition'].map(condition_map)

    colors_map = {'HP': '#ff9999', 'HI': '#ff0000', 'NP': '#9999ff', 'NI': '#0000ff'}
    colors = [colors_map[c] for c in summary['Condition']]

    bars = ax1.bar(range(4), summary['mean'], yerr=summary['sem'],
                   color=colors, alpha=0.8, capsize=7, edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(4))
    ax1.set_xticklabels(summary['Condition_Label'], rotation=15, ha='right', fontsize=10)
    ax1.set_ylabel('Mean Plausibility Rating (1-4)', fontsize=13, fontweight='bold')
    ax1.set_title('H3: 2x2 Design (Emotion x Plausibility)', fontsize=15, fontweight='bold')
    ax1.set_ylim([0, 4.5])
    ax1.grid(axis='y', alpha=0.3)

    # Add values on bars
    for i, (bar, mean) in enumerate(zip(bars, summary['mean'])):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                f'{mean:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Panel 2: Interaction plot
    ax2 = plt.subplot(1, 3, 2)

    for emotion, color, marker in [('H', 'red', 'o'), ('N', 'blue', 's')]:
        emotion_data = rating_clean[rating_clean['Emotion'] == emotion]
        plaus_means = emotion_data.groupby('Plausibility')['Rating'].agg(['mean', 'sem']).reset_index()
        plaus_means = plaus_means.sort_values('Plausibility')  # I, P

        ax2.errorbar([0, 1], plaus_means['mean'], yerr=plaus_means['sem'],
                    marker=marker, markersize=12, linewidth=3, capsize=6,
                    label='Hate' if emotion=='H' else 'Neutral', color=color)

    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Implausible', 'Plausible'])
    ax2.set_xlabel('Item Plausibility', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Mean Rating (1-4)', fontsize=13, fontweight='bold')
    ax2.set_title('H3: Emotion x Plausibility Interaction', fontsize=15, fontweight='bold')
    ax2.set_ylim([2.0, 3.5])
    ax2.legend(fontsize=12, title='Emotion Context')
    ax2.grid(alpha=0.3)

    # Panel 3: Distribution by Emotion
    ax3 = plt.subplot(1, 3, 3)

    hate_ratings = rating_clean[rating_clean['Emotion']=='H']['Rating']
    neutral_ratings = rating_clean[rating_clean['Emotion']=='N']['Rating']

    ax3.hist(hate_ratings, bins=4, alpha=0.6, color='red', label='Hate', edgecolor='black')
    ax3.hist(neutral_ratings, bins=4, alpha=0.6, color='blue', label='Neutral', edgecolor='black')

    ax3.set_xlabel('Plausibility Rating (1-4)', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax3.set_title('H3: Rating Distribution by Emotion', fontsize=15, fontweight='bold')
    ax3.legend(fontsize=12)
    ax3.set_xticks([1, 2, 3, 4])

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H3_MemoryBias.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/Figure_H3_MemoryBias.png")
    plt.close()

    # Figure 2: Box plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # By Emotion
    ax = axes[0]
    sns.boxplot(data=rating_clean, x='Emotion', y='Rating', ax=ax, palette='Set1')
    sns.swarmplot(data=rating_clean, x='Emotion', y='Rating', ax=ax,
                  color='black', alpha=0.3, size=3)
    ax.set_xlabel('Emotion Context', fontsize=13, fontweight='bold')
    ax.set_ylabel('Plausibility Rating (1-4)', fontsize=13, fontweight='bold')
    ax.set_title('H3: Rating by Emotion Context', fontsize=15, fontweight='bold')
    ax.set_xticklabels(['Hate', 'Neutral'])

    # By Plausibility
    ax = axes[1]
    sns.boxplot(data=rating_clean, x='Plausibility', y='Rating', ax=ax, palette='Set2')
    sns.swarmplot(data=rating_clean, x='Plausibility', y='Rating', ax=ax,
                  color='black', alpha=0.3, size=3)
    ax.set_xlabel('Item Plausibility', fontsize=13, fontweight='bold')
    ax.set_ylabel('Plausibility Rating (1-4)', fontsize=13, fontweight='bold')
    ax.set_title('H3: Rating by Item Plausibility', fontsize=15, fontweight='bold')
    ax.set_xticklabels(['Implausible', 'Plausible'])

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H3_Boxplots.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/Figure_H3_Boxplots.png")
    plt.close()

def main():
    rating_clean = analyze_h3()
    create_h3_visualizations(rating_clean)

    print("\n" + "="*80)
    print("H3 ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - result_1128/Figure_H3_MemoryBias.png")
    print("  - result_1128/Figure_H3_Boxplots.png")

if __name__ == "__main__":
    main()
