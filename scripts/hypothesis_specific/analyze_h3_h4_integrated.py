"""
H3-H4 통합 분석:
H3에서 발견된 기억 왜곡(plausibility 판단 손상)이
H4 회상 내용(사실 포함, 부정 표현)과 어떻게 연결되는지 분석
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

def analyze_h3_h4_integration():
    """H3 기억 왜곡과 H4 회상 패턴의 관계"""

    print("="*80)
    print("H3-H4 통합 분석: 기억 왜곡과 회상 내용의 관계")
    print("="*80)

    # Load data
    rating = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='Rating_Data')
    recall = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name='Recall_Data')

    # Clean rating data
    rating_clean = rating[rating['Rating'].notna()].copy()

    # 1. H3: 참가자별 기억 왜곡 정도 계산
    print("\n" + "="*80)
    print("1. H3 분석: 참가자별 기억 왜곡 정도")
    print("="*80)

    participant_h3 = []

    for pid in rating_clean['Participant_ID'].unique():
        p_data = rating_clean[rating_clean['Participant_ID'] == pid]

        # Hate condition: Plausibility effect
        h_data = p_data[p_data['Emotion'] == 'H']
        h_p = h_data[h_data['Plausibility'] == 'P']['Rating'].mean()
        h_i = h_data[h_data['Plausibility'] == 'I']['Rating'].mean()
        hate_plaus_effect = h_p - h_i

        # Neutral condition: Plausibility effect
        n_data = p_data[p_data['Emotion'] == 'N']
        n_p = n_data[n_data['Plausibility'] == 'P']['Rating'].mean()
        n_i = n_data[n_data['Plausibility'] == 'I']['Rating'].mean()
        neutral_plaus_effect = n_p - n_i

        # H3 핵심: Hate에서 plausibility 구별 능력 손상 정도
        # 음수일수록 더 큰 왜곡 (중립에서는 정상, 혐오에서는 손상)
        distortion = hate_plaus_effect - neutral_plaus_effect

        # Overall bias: Hate context에서 전반적으로 낮게 평가하는 정도
        h_mean = h_data['Rating'].mean()
        n_mean = n_data['Rating'].mean()
        hate_bias = h_mean - n_mean

        participant_h3.append({
            'Participant_ID': pid,
            'Hate_Plaus_Effect': hate_plaus_effect,
            'Neutral_Plaus_Effect': neutral_plaus_effect,
            'Distortion': distortion,
            'Hate_Mean_Rating': h_mean,
            'Neutral_Mean_Rating': n_mean,
            'Hate_Bias': hate_bias
        })

    h3_df = pd.DataFrame(participant_h3)

    print("\n참가자별 H3 지표:")
    print(h3_df.to_string(index=False))
    print("\n해석:")
    print("  - Distortion: 음수 = 혐오에서 plausibility 구별 손상")
    print("  - Hate_Bias: 음수 = 혐오 맥락에서 전반적으로 낮게 평가")

    # 2. H4: 참가자별 회상 패턴
    print("\n\n" + "="*80)
    print("2. H4 분석: 참가자별 회상 패턴")
    print("="*80)

    background_facts = ['중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
                        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
                        '허브', '노래', '짧은', '반복', '유목', '정착']

    negative_words = ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡']

    # 추가 부정 표현 확장 (형용사, 동사 포함)
    extended_negative = negative_words + [
        '부족', '낙후', '원시', '천박', '졸렬', '하찮', '조악',
        '빈약', '단순', '거칠', '투박', '촌스러', '멀다', '떨어지',
        '못하', '약하', '적은', '부실', '허술'
    ]

    participant_h4 = []

    for idx, row in recall.iterrows():
        text = row['Recall_Text']

        # 사실 포함 개수
        fact_count = sum(1 for fact in background_facts if fact in text)

        # 부정 표현 (기본)
        negative_count = sum(text.count(word) for word in negative_words)

        # 부정 표현 (확장)
        extended_negative_count = sum(text.count(word) for word in extended_negative)

        # 텍스트 길이 및 사실 비율
        text_length = len(text)
        fact_ratio = fact_count / (text_length / 10) if text_length > 0 else 0

        participant_h4.append({
            'Participant_ID': row['Participant_ID'],
            'Fact_Count': fact_count,
            'Negative_Count': negative_count,
            'Extended_Negative_Count': extended_negative_count,
            'Text_Length': text_length,
            'Fact_Ratio': fact_ratio
        })

    h4_df = pd.DataFrame(participant_h4)

    print("\n참가자별 H4 지표:")
    print(h4_df.to_string(index=False))

    # 3. H3-H4 통합: 상관분석
    print("\n\n" + "="*80)
    print("3. H3-H4 통합 분석: 기억 왜곡과 회상 내용의 상관")
    print("="*80)

    # Merge
    merged = h3_df.merge(h4_df, on='Participant_ID')

    print("\n통합 데이터:")
    print(merged.to_string(index=False))

    # 상관분석
    print("\n\n=== 핵심 상관분석 ===\n")

    # (1) Distortion(기억 왜곡) × Fact_Count(사실 포함)
    if merged['Distortion'].std() > 0 and merged['Fact_Count'].std() > 0:
        r1, p1 = stats.pearsonr(merged['Distortion'], merged['Fact_Count'])
        print(f"1. 기억 왜곡(Distortion) × 사실 포함 개수:")
        print(f"   r = {r1:.3f}, p = {p1:.3f}")
        print(f"   해석: 왜곡이 {'클수록' if r1 < 0 else '작을수록'} 사실을 {'많이' if r1 < 0 else '적게'} 회상")
        print(f"   {'⚠️ 음의 상관: 왜곡이 심할수록 사실 회상 감소!' if r1 < -0.3 and p1 < 0.1 else ''}")

    # (2) Distortion × Extended_Negative_Count
    if merged['Distortion'].std() > 0 and merged['Extended_Negative_Count'].std() > 0:
        r2, p2 = stats.pearsonr(merged['Distortion'], merged['Extended_Negative_Count'])
        print(f"\n2. 기억 왜곡(Distortion) × 부정 표현 사용:")
        print(f"   r = {r2:.3f}, p = {p2:.3f}")
        print(f"   해석: 왜곡이 {'클수록' if r2 < 0 else '작을수록'} 부정 표현을 {'많이' if r2 < 0 else '적게'} 사용")
    else:
        print("\n2. 기억 왜곡(Distortion) × 부정 표현 사용:")
        print("   분산 없음 (모든 참가자가 0)")

    # (3) Hate_Bias(혐오 맥락 전반적 하락) × Fact_Count
    if merged['Hate_Bias'].std() > 0:
        r3, p3 = stats.pearsonr(merged['Hate_Bias'], merged['Fact_Count'])
        print(f"\n3. 혐오 편향(Hate_Bias) × 사실 포함 개수:")
        print(f"   r = {r3:.3f}, p = {p3:.3f}")
        print(f"   해석: 혐오 맥락에서 낮게 평가할수록 사실을 {'많이' if r3 < 0 else '적게'} 회상")

    # (4) Neutral_Plaus_Effect(정상적 판단 능력) × Fact_Count
    if merged['Neutral_Plaus_Effect'].std() > 0:
        r4, p4 = stats.pearsonr(merged['Neutral_Plaus_Effect'], merged['Fact_Count'])
        print(f"\n4. 중립 조건 판단 능력(Neutral_Plaus_Effect) × 사실 포함 개수:")
        print(f"   r = {r4:.3f}, p = {p4:.3f}")
        print(f"   해석: 중립 조건에서 잘 판단할수록 사실을 {'많이' if r4 > 0 else '적게'} 회상")

    # (5) Fact_Ratio(길이 대비 사실 밀도) 분석
    if merged['Fact_Ratio'].std() > 0:
        r5, p5 = stats.pearsonr(merged['Distortion'], merged['Fact_Ratio'])
        print(f"\n5. 기억 왜곡(Distortion) × 사실 밀도(Fact_Ratio):")
        print(f"   r = {r5:.3f}, p = {p5:.3f}")
        print(f"   해석: 길이를 통제해도 왜곡과 사실 회상의 {'음의' if r5 < 0 else '양의'} 관계")

    print(f"\n\n⚠️ 주의: N=6으로 모든 상관은 탐색적. p < .05는 통계적으로 의미 있으나,")
    print(f"        N < 10에서는 우연일 가능성도 높음. 패턴 파악 목적.")

    # 4. 시각화
    create_h3_h4_visualizations(merged)

    return merged

def create_h3_h4_visualizations(merged):
    """H3-H4 통합 시각화"""

    print("\n\n" + "="*80)
    print("시각화 생성 중...")
    print("="*80)

    fig = plt.figure(figsize=(18, 12))

    # Panel 1: Distortion vs Fact_Count
    ax1 = plt.subplot(2, 3, 1)
    if merged['Distortion'].std() > 0 and merged['Fact_Count'].std() > 0:
        ax1.scatter(merged['Distortion'], merged['Fact_Count'],
                   s=100, alpha=0.6, color='steelblue', edgecolor='black')

        # Add participant labels
        for idx, row in merged.iterrows():
            ax1.annotate(str(row['Participant_ID'])[:3],
                        (row['Distortion'], row['Fact_Count']),
                        fontsize=9, ha='right', va='bottom')

        # Regression line
        z = np.polyfit(merged['Distortion'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Distortion'].min(), merged['Distortion'].max(), 100)
        ax1.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

        r, p_val = stats.pearsonr(merged['Distortion'], merged['Fact_Count'])
        ax1.set_title(f'Memory Distortion vs Fact Recall\n(r={r:.3f}, p={p_val:.3f})',
                     fontsize=13, fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'No variance', ha='center', va='center', fontsize=12)
        ax1.set_title('Memory Distortion vs Fact Recall', fontsize=13, fontweight='bold')

    ax1.set_xlabel('Distortion (Hate - Neutral plaus effect)', fontsize=11)
    ax1.set_ylabel('Fact Count in Recall', fontsize=11)
    ax1.axvline(0, color='gray', linestyle='--', alpha=0.5)
    ax1.grid(alpha=0.3)

    # Panel 2: Hate_Bias vs Fact_Count
    ax2 = plt.subplot(2, 3, 2)
    if merged['Hate_Bias'].std() > 0:
        ax2.scatter(merged['Hate_Bias'], merged['Fact_Count'],
                   s=100, alpha=0.6, color='coral', edgecolor='black')

        for idx, row in merged.iterrows():
            ax2.annotate(str(row['Participant_ID'])[:3],
                        (row['Hate_Bias'], row['Fact_Count']),
                        fontsize=9, ha='right', va='bottom')

        z = np.polyfit(merged['Hate_Bias'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Hate_Bias'].min(), merged['Hate_Bias'].max(), 100)
        ax2.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

        r, p_val = stats.pearsonr(merged['Hate_Bias'], merged['Fact_Count'])
        ax2.set_title(f'Hate Context Bias vs Fact Recall\n(r={r:.3f}, p={p_val:.3f})',
                     fontsize=13, fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'No variance', ha='center', va='center', fontsize=12)
        ax2.set_title('Hate Context Bias vs Fact Recall', fontsize=13, fontweight='bold')

    ax2.set_xlabel('Hate Bias (Hate - Neutral mean rating)', fontsize=11)
    ax2.set_ylabel('Fact Count in Recall', fontsize=11)
    ax2.axvline(0, color='gray', linestyle='--', alpha=0.5)
    ax2.grid(alpha=0.3)

    # Panel 3: Neutral_Plaus_Effect vs Fact_Count
    ax3 = plt.subplot(2, 3, 3)
    if merged['Neutral_Plaus_Effect'].std() > 0:
        ax3.scatter(merged['Neutral_Plaus_Effect'], merged['Fact_Count'],
                   s=100, alpha=0.6, color='mediumseagreen', edgecolor='black')

        for idx, row in merged.iterrows():
            ax3.annotate(str(row['Participant_ID'])[:3],
                        (row['Neutral_Plaus_Effect'], row['Fact_Count']),
                        fontsize=9, ha='right', va='bottom')

        z = np.polyfit(merged['Neutral_Plaus_Effect'], merged['Fact_Count'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Neutral_Plaus_Effect'].min(),
                            merged['Neutral_Plaus_Effect'].max(), 100)
        ax3.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

        r, p_val = stats.pearsonr(merged['Neutral_Plaus_Effect'], merged['Fact_Count'])
        ax3.set_title(f'Neutral Discrimination vs Fact Recall\n(r={r:.3f}, p={p_val:.3f})',
                     fontsize=13, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'No variance', ha='center', va='center', fontsize=12)
        ax3.set_title('Neutral Discrimination vs Fact Recall', fontsize=13, fontweight='bold')

    ax3.set_xlabel('Neutral Plaus Effect (P - I rating)', fontsize=11)
    ax3.set_ylabel('Fact Count in Recall', fontsize=11)
    ax3.grid(alpha=0.3)

    # Panel 4: Distortion vs Fact_Ratio
    ax4 = plt.subplot(2, 3, 4)
    if merged['Distortion'].std() > 0 and merged['Fact_Ratio'].std() > 0:
        ax4.scatter(merged['Distortion'], merged['Fact_Ratio'],
                   s=100, alpha=0.6, color='mediumpurple', edgecolor='black')

        for idx, row in merged.iterrows():
            ax4.annotate(str(row['Participant_ID'])[:3],
                        (row['Distortion'], row['Fact_Ratio']),
                        fontsize=9, ha='right', va='bottom')

        z = np.polyfit(merged['Distortion'], merged['Fact_Ratio'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(merged['Distortion'].min(), merged['Distortion'].max(), 100)
        ax4.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

        r, p_val = stats.pearsonr(merged['Distortion'], merged['Fact_Ratio'])
        ax4.set_title(f'Memory Distortion vs Fact Density\n(r={r:.3f}, p={p_val:.3f})',
                     fontsize=13, fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No variance', ha='center', va='center', fontsize=12)
        ax4.set_title('Memory Distortion vs Fact Density', fontsize=13, fontweight='bold')

    ax4.set_xlabel('Distortion (Hate - Neutral plaus effect)', fontsize=11)
    ax4.set_ylabel('Fact Density (per 10 chars)', fontsize=11)
    ax4.axvline(0, color='gray', linestyle='--', alpha=0.5)
    ax4.grid(alpha=0.3)

    # Panel 5: Participant comparison (H3 metrics)
    ax5 = plt.subplot(2, 3, 5)
    x_pos = np.arange(len(merged))
    width = 0.35

    bars1 = ax5.bar(x_pos - width/2, merged['Hate_Plaus_Effect'], width,
                    label='Hate Plaus Effect', color='salmon', alpha=0.8, edgecolor='black')
    bars2 = ax5.bar(x_pos + width/2, merged['Neutral_Plaus_Effect'], width,
                    label='Neutral Plaus Effect', color='skyblue', alpha=0.8, edgecolor='black')

    ax5.set_xlabel('Participant', fontsize=11)
    ax5.set_ylabel('Plausibility Effect (P - I)', fontsize=11)
    ax5.set_title('H3: Plausibility Discrimination by Emotion', fontsize=13, fontweight='bold')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels([str(pid)[:3] for pid in merged['Participant_ID']], rotation=0)
    ax5.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax5.legend(fontsize=9)
    ax5.grid(axis='y', alpha=0.3)

    # Panel 6: Participant comparison (H4 metrics)
    ax6 = plt.subplot(2, 3, 6)
    ax6_twin = ax6.twinx()

    bars = ax6.bar(x_pos, merged['Fact_Count'], color='lightgreen',
                   alpha=0.8, edgecolor='black', label='Fact Count')
    line = ax6_twin.plot(x_pos, merged['Text_Length'], 'ro-', linewidth=2,
                         markersize=8, label='Text Length')

    ax6.set_xlabel('Participant', fontsize=11)
    ax6.set_ylabel('Fact Count', fontsize=11, color='green')
    ax6_twin.set_ylabel('Text Length (chars)', fontsize=11, color='red')
    ax6.set_title('H4: Recall Content Analysis', fontsize=13, fontweight='bold')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels([str(pid)[:3] for pid in merged['Participant_ID']], rotation=0)
    ax6.tick_params(axis='y', labelcolor='green')
    ax6_twin.tick_params(axis='y', labelcolor='red')
    ax6.grid(axis='y', alpha=0.3)

    # Add values on bars
    for i, (bar, val) in enumerate(zip(bars, merged['Fact_Count'])):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2, height + 0.2,
                f'{int(val)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H3_H4_Integration.png', dpi=300, bbox_inches='tight')
    print("\nSaved: result_1128/Figure_H3_H4_Integration.png")
    plt.close()

    # Additional: Heatmap of correlations
    fig2, ax = plt.subplots(figsize=(10, 8))

    # Select key variables for correlation
    corr_vars = ['Distortion', 'Hate_Bias', 'Neutral_Plaus_Effect',
                 'Fact_Count', 'Text_Length', 'Fact_Ratio']

    corr_matrix = merged[corr_vars].corr()

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', center=0, vmin=-1, vmax=1,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax)

    ax.set_title('H3-H4 Integration: Correlation Matrix\n(N=6, exploratory)',
                fontsize=15, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H3_H4_Correlations.png', dpi=300, bbox_inches='tight')
    print("Saved: result_1128/Figure_H3_H4_Correlations.png")
    plt.close()

def main():
    merged = analyze_h3_h4_integration()

    # Save results
    merged.to_csv('result_1128/h3_h4_integrated.csv', index=False)

    print("\n\n" + "="*80)
    print("H3-H4 통합 분석 완료")
    print("="*80)
    print("\n생성된 파일:")
    print("  - result_1128/Figure_H3_H4_Integration.png (6패널 산점도 + 비교)")
    print("  - result_1128/Figure_H3_H4_Correlations.png (상관 히트맵)")
    print("  - result_1128/h3_h4_integrated.csv (통합 데이터)")

    print("\n\n=== 핵심 메시지 ===")
    print("H3에서 발견된 '기억 왜곡'이 H4 '회상 내용'에 어떻게 반영되는지 탐색")
    print("- 왜곡(Distortion) = Hate조건에서 plausibility 구별 능력 손상 정도")
    print("- 음의 상관 기대: 왜곡 클수록 → 사실 회상 감소")
    print("- N=6으로 통계적 검정력은 부족하나, 패턴 파악 목적의 탐색적 분석")

if __name__ == "__main__":
    main()
