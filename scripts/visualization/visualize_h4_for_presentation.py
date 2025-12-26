"""
H4 회상 데이터 시각화 (발표용)
확장된 부정 표현 사전 사용:
- 직접적 혐오 (Direct hate speech)
- 간접적 부정 (Indirect negative)
- 비하적 표현 (Derogatory)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = ['AppleGothic', 'Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300

def analyze_recall_with_expanded_dictionary(recall_file):
    """
    확장된 부정 표현 사전을 사용한 회상 데이터 분석
    """

    print("\n" + "="*80)
    print("H4: 회상 데이터 분석 (확장된 부정 표현 사전)")
    print("="*80)

    # 데이터 로드
    recall = pd.read_excel(recall_file, sheet_name='Recall_Data')

    # 배경 사실
    background_facts = [
        '중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
        '허브', '노래', '짧은', '반복', '유목', '정착'
    ]

    # 확장된 부정 표현 사전
    negative_words = {
        '직접적 혐오': ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡'],
        '간접적 부정': ['천박', '무지', '수준 낮', '낙후', '원시', '조악'],
        '비하적': ['하찮', '졸렬', '단순', '부족']
    }

    # 잘못된 정보 (Implausible 조건에서 나온 내용)
    false_info = [
        '금속', '고층', '사막', '날개', '날아', '비행', '점프', '뛰어넘',
        '금', '바꾼', '흙을 먹', '씹어먹', '물에 잠기', '떨어져', '재탄생',
        '매일 이동', '조립', '몸을 갖다대'
    ]

    # 중립적 서술어
    neutral_descriptors = ['생활', '문화', '전통', '기술', '예술', '자연', '적응']

    results = []

    print("\n참가자별 분석:")
    print("-" * 80)

    for idx, row in recall.iterrows():
        pid = row['Participant_ID']
        text = str(row['Recall_Text'])

        # 1. 사실 정보 포함
        facts_found = [fact for fact in background_facts if fact in text]
        fact_count = len(facts_found)

        # 2. 부정 표현 분석 (카테고리별)
        neg_direct = sum(text.count(word) for word in negative_words['직접적 혐오'])
        neg_indirect = sum(text.count(word) for word in negative_words['간접적 부정'])
        neg_derogatory = sum(text.count(word) for word in negative_words['비하적'])
        neg_total = neg_direct + neg_indirect + neg_derogatory

        # 부정 단어 검출
        neg_words_found = []
        for category, words in negative_words.items():
            for word in words:
                if word in text:
                    neg_words_found.append(f"{word}({category})")

        # 3. 잘못된 정보
        false_info_found = [info for info in false_info if info in text]
        false_count = len(false_info_found)

        # 4. 중립 표현
        neutral_found = [word for word in neutral_descriptors if word in text]
        neutral_count = len(neutral_found)

        # 5. 감정 점수 (중립 - 부정)
        sentiment_score = neutral_count - neg_total

        # 6. 텍스트 특성
        text_length = len(text)

        print(f"{pid}: Facts={fact_count}, Neg={neg_total} (D={neg_direct}, I={neg_indirect}, Der={neg_derogatory}), "
              f"False={false_count}, Sentiment={sentiment_score:+d}")

        if neg_words_found:
            print(f"  └─ 부정 표현: {', '.join(neg_words_found)}")
        if false_info_found:
            print(f"  └─ 잘못된 정보: {', '.join(false_info_found)}")

        results.append({
            'Participant_ID': pid,
            'Text_Length': text_length,
            'Fact_Count': fact_count,
            'Fact_Ratio': fact_count / len(background_facts),
            'Negative_Direct': neg_direct,
            'Negative_Indirect': neg_indirect,
            'Negative_Derogatory': neg_derogatory,
            'Negative_Total': neg_total,
            'False_Info_Count': false_count,
            'Neutral_Count': neutral_count,
            'Sentiment_Score': sentiment_score,
            'Has_Negative': 1 if neg_total > 0 else 0,
            'Has_False_Info': 1 if false_count > 0 else 0,
            'Negative_Words': '; '.join(neg_words_found) if neg_words_found else 'None',
            'False_Info': '; '.join(false_info_found) if false_info_found else 'None'
        })

    results_df = pd.DataFrame(results)

    # 요약 통계
    print("\n" + "="*80)
    print("요약 통계")
    print("="*80)

    summary = results_df[['Fact_Count', 'Negative_Direct', 'Negative_Indirect',
                          'Negative_Derogatory', 'Negative_Total',
                          'False_Info_Count', 'Neutral_Count', 'Sentiment_Score']].describe()
    print(summary.round(2))

    print(f"\n부정 표현 사용 참가자: {results_df['Has_Negative'].sum()}명 / {len(results_df)}명")
    print(f"  - 직접적 혐오만: {(results_df['Negative_Direct'] > 0).sum()}명")
    print(f"  - 간접적 부정만: {(results_df['Negative_Indirect'] > 0).sum()}명")
    print(f"  - 비하적 표현만: {(results_df['Negative_Derogatory'] > 0).sum()}명")

    print(f"\n잘못된 정보 포함: {results_df['Has_False_Info'].sum()}명 / {len(results_df)}명")

    neg_sentiment = (results_df['Sentiment_Score'] < 0).sum()
    print(f"부정적 감정 점수 (<0): {neg_sentiment}명 / {len(results_df)}명")

    return results_df, negative_words

def create_h4_visualizations(results_df, negative_words, output_dir):
    """
    H4 발표용 시각화 생성
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Figure 1: 부정 표현 카테고리별 사용 (Stacked Bar)
    fig, ax = plt.subplots(figsize=(14, 6))

    x_pos = np.arange(len(results_df))
    width = 0.7

    # Stacked bar chart
    p1 = ax.bar(x_pos, results_df['Negative_Direct'], width,
                label='직접적 혐오 (Direct Hate)', color='#d62728', alpha=0.9)
    p2 = ax.bar(x_pos, results_df['Negative_Indirect'], width,
                bottom=results_df['Negative_Direct'],
                label='간접적 부정 (Indirect Negative)', color='#ff7f0e', alpha=0.9)
    p3 = ax.bar(x_pos, results_df['Negative_Derogatory'], width,
                bottom=results_df['Negative_Direct'] + results_df['Negative_Indirect'],
                label='비하적 (Derogatory)', color='#bcbd22', alpha=0.9)

    # Total 라벨 추가
    for i, total in enumerate(results_df['Negative_Total']):
        if total > 0:
            ax.text(i, total + 0.15, f'{int(total)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax.set_xlabel('Participant ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Negative Expression Count', fontsize=12, fontweight='bold')
    ax.set_title('H4: Negative Expressions by Category\n(Direct Hate + Indirect Negative + Derogatory)',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(pid)[:10] for pid in results_df['Participant_ID']],
                       rotation=45, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # 통계 정보 추가
    n_users = results_df['Has_Negative'].sum()
    total_neg = results_df['Negative_Total'].sum()
    textstr = f'Users with negative expressions: {n_users}/{len(results_df)}\nTotal negative expressions: {int(total_neg)}'
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    output_file = output_dir / 'H4_negative_expressions_by_category.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_file}")
    plt.close()

    # Figure 2: Facts vs. Negative vs. False Info (Grouped Bar)
    fig, ax = plt.subplots(figsize=(14, 6))

    x_pos = np.arange(len(results_df))
    width = 0.25

    bars1 = ax.bar(x_pos - width, results_df['Fact_Count'], width,
                   label='Factual Details', color='#2ca02c', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x_pos, results_df['Negative_Total'], width,
                   label='Negative Expressions', color='#d62728', alpha=0.8, edgecolor='black')
    bars3 = ax.bar(x_pos + width, results_df['False_Info_Count'], width,
                   label='False Information', color='#ff7f0e', alpha=0.8, edgecolor='black')

    ax.set_xlabel('Participant ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('H4: Facts vs. Negative Expressions vs. False Information',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(pid)[:10] for pid in results_df['Participant_ID']],
                       rotation=45, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    output_file = output_dir / 'H4_comprehensive_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

    # Figure 3: Scatter plots (2x2 grid)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel 1: Facts vs. Total Negative
    ax = axes[0, 0]
    ax.scatter(results_df['Fact_Count'], results_df['Negative_Total'],
              s=150, alpha=0.7, color='purple', edgecolor='black', linewidth=1.5)

    # Correlation
    if results_df['Negative_Total'].sum() > 0:
        r, p = stats.pearsonr(results_df['Fact_Count'], results_df['Negative_Total'])

        # Regression line
        z = np.polyfit(results_df['Fact_Count'], results_df['Negative_Total'], 1)
        p_fit = np.poly1d(z)
        x_line = np.linspace(results_df['Fact_Count'].min(), results_df['Fact_Count'].max(), 100)
        ax.plot(x_line, p_fit(x_line), "r--", alpha=0.8, linewidth=2, label=f'r={r:.3f}, p={p:.3f}')
        ax.legend(fontsize=10)

    ax.set_xlabel('Factual Details Count', fontsize=11, fontweight='bold')
    ax.set_ylabel('Total Negative Expressions', fontsize=11, fontweight='bold')
    ax.set_title('Facts vs. Negative Expressions', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3, linestyle='--')

    # Panel 2: Facts vs. False Info
    ax = axes[0, 1]
    ax.scatter(results_df['Fact_Count'], results_df['False_Info_Count'],
              s=150, alpha=0.7, color='darkorange', edgecolor='black', linewidth=1.5)

    if results_df['False_Info_Count'].sum() > 0:
        r, p = stats.pearsonr(results_df['Fact_Count'], results_df['False_Info_Count'])
        z = np.polyfit(results_df['Fact_Count'], results_df['False_Info_Count'], 1)
        p_fit = np.poly1d(z)
        x_line = np.linspace(results_df['Fact_Count'].min(), results_df['Fact_Count'].max(), 100)
        ax.plot(x_line, p_fit(x_line), "r--", alpha=0.8, linewidth=2, label=f'r={r:.3f}, p={p:.3f}')
        ax.legend(fontsize=10)

    ax.set_xlabel('Factual Details Count', fontsize=11, fontweight='bold')
    ax.set_ylabel('False Information Count', fontsize=11, fontweight='bold')
    ax.set_title('Facts vs. False Information', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3, linestyle='--')

    # Panel 3: Sentiment Score distribution
    ax = axes[1, 0]
    colors = ['green' if s >= 0 else 'red' for s in results_df['Sentiment_Score']]
    bars = ax.bar(range(len(results_df)), results_df['Sentiment_Score'],
                  color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.axhline(0, color='black', linestyle='--', linewidth=2)
    ax.set_xlabel('Participant ID', fontsize=11, fontweight='bold')
    ax.set_ylabel('Sentiment Score\n(Neutral - Negative)', fontsize=11, fontweight='bold')
    ax.set_title('Sentiment Score by Participant\n(Positive = Neutral, Negative = Biased)',
                fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(results_df)))
    ax.set_xticklabels([str(pid)[:10] for pid in results_df['Participant_ID']],
                       rotation=45, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Panel 4: Category breakdown (pie chart)
    ax = axes[1, 1]

    total_direct = results_df['Negative_Direct'].sum()
    total_indirect = results_df['Negative_Indirect'].sum()
    total_derogatory = results_df['Negative_Derogatory'].sum()

    if total_direct + total_indirect + total_derogatory > 0:
        sizes = [total_direct, total_indirect, total_derogatory]
        labels = [f'직접적 혐오\n({int(total_direct)})',
                 f'간접적 부정\n({int(total_indirect)})',
                 f'비하적\n({int(total_derogatory)})']
        colors_pie = ['#d62728', '#ff7f0e', '#bcbd22']
        explode = (0.05, 0.05, 0.05)

        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                           autopct='%1.1f%%', shadow=True, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)

        ax.set_title('Negative Expression Type Distribution\n(Total across all participants)',
                    fontsize=12, fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'No negative expressions found',
               ha='center', va='center', fontsize=14, transform=ax.transAxes)
        ax.set_title('Negative Expression Type Distribution', fontsize=12, fontweight='bold')

    plt.tight_layout()
    output_file = output_dir / 'H4_detailed_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

    print(f"\n✓ All H4 visualizations saved to: {output_dir}")

def create_summary_table(results_df, output_dir):
    """H4 요약 테이블 생성"""

    output_dir = Path(output_dir)

    # 요약 통계 계산
    summary_data = {
        'Metric': [
            'Factual Details (mean)',
            'Negative: Direct (mean)',
            'Negative: Indirect (mean)',
            'Negative: Derogatory (mean)',
            'Negative: Total (mean)',
            'False Information (mean)',
            'Sentiment Score (mean)',
            '',
            'Participants with Negative Exp.',
            'Participants with False Info',
            'Participants with Negative Sentiment'
        ],
        'Value': [
            f"{results_df['Fact_Count'].mean():.2f} (SD={results_df['Fact_Count'].std():.2f})",
            f"{results_df['Negative_Direct'].mean():.2f} (SD={results_df['Negative_Direct'].std():.2f})",
            f"{results_df['Negative_Indirect'].mean():.2f} (SD={results_df['Negative_Indirect'].std():.2f})",
            f"{results_df['Negative_Derogatory'].mean():.2f} (SD={results_df['Negative_Derogatory'].std():.2f})",
            f"{results_df['Negative_Total'].mean():.2f} (SD={results_df['Negative_Total'].std():.2f})",
            f"{results_df['False_Info_Count'].mean():.2f} (SD={results_df['False_Info_Count'].std():.2f})",
            f"{results_df['Sentiment_Score'].mean():.2f} (SD={results_df['Sentiment_Score'].std():.2f})",
            '',
            f"{results_df['Has_Negative'].sum()} / {len(results_df)} ({100*results_df['Has_Negative'].mean():.1f}%)",
            f"{results_df['Has_False_Info'].sum()} / {len(results_df)} ({100*results_df['Has_False_Info'].mean():.1f}%)",
            f"{(results_df['Sentiment_Score'] < 0).sum()} / {len(results_df)} ({100*(results_df['Sentiment_Score'] < 0).mean():.1f}%)"
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    # CSV로 저장
    csv_file = output_dir / 'H4_summary_statistics.csv'
    summary_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ Saved summary table: {csv_file}")

    # 참가자별 상세 데이터도 저장
    detail_file = output_dir / 'H4_participant_details.csv'
    results_df.to_csv(detail_file, index=False, encoding='utf-8-sig')
    print(f"✓ Saved participant details: {detail_file}")

    return summary_df

def main():
    """메인 실행 함수"""

    # 파일 경로 설정
    recall_file = 'result_1201/ExpLing_Project.xlsx'
    output_dir = 'result_1201/h4_presentation_plots'

    print("\n" + "="*80)
    print("H4 회상 데이터 분석 및 시각화 (발표용)")
    print("확장된 부정 표현 사전 사용")
    print("="*80)

    # 분석 실행
    results_df, negative_words = analyze_recall_with_expanded_dictionary(recall_file)

    # 시각화 생성
    print("\n" + "="*80)
    print("시각화 생성 중...")
    print("="*80)

    create_h4_visualizations(results_df, negative_words, output_dir)

    # 요약 테이블 생성
    summary_df = create_summary_table(results_df, output_dir)

    print("\n" + "="*80)
    print("H4 Summary Statistics")
    print("="*80)
    print(summary_df.to_string(index=False))

    print("\n" + "="*80)
    print("H4 분석 완료!")
    print("="*80)
    print(f"\n생성된 파일:")
    print(f"  1. H4_negative_expressions_by_category.png")
    print(f"  2. H4_comprehensive_comparison.png")
    print(f"  3. H4_detailed_analysis.png")
    print(f"  4. H4_summary_statistics.csv")
    print(f"  5. H4_participant_details.csv")
    print(f"\n저장 위치: {output_dir}/")

    # 주요 발견사항 출력
    print("\n" + "="*80)
    print("주요 발견사항 (Key Findings)")
    print("="*80)

    if results_df['Has_Negative'].sum() > 0:
        print(f"\n✓ 부정 표현 사용: {results_df['Has_Negative'].sum()}명/{len(results_df)}명")
        print(f"  - 직접적 혐오: 총 {int(results_df['Negative_Direct'].sum())}회")
        print(f"  - 간접적 부정: 총 {int(results_df['Negative_Indirect'].sum())}회")
        print(f"  - 비하적 표현: 총 {int(results_df['Negative_Derogatory'].sum())}회")

        # 간접적 표현의 중요성 강조
        if results_df['Negative_Indirect'].sum() > 0:
            indirect_pct = 100 * results_df['Negative_Indirect'].sum() / results_df['Negative_Total'].sum()
            print(f"\n  ⚠️ 주목: 간접적 부정 표현이 전체 부정 표현의 {indirect_pct:.1f}%를 차지")
            print(f"    → 직접적 혐오 표현만 분석했다면 {int(results_df['Negative_Indirect'].sum())}개 놓쳤을 것")

    if results_df['Has_False_Info'].sum() > 0:
        print(f"\n✓ 잘못된 정보 재생산: {results_df['Has_False_Info'].sum()}명/{len(results_df)}명")
        print(f"  - 총 {int(results_df['False_Info_Count'].sum())}개의 implausible 내용이 사실로 기억됨")

    if (results_df['Sentiment_Score'] < 0).sum() > 0:
        print(f"\n✓ 부정적 편향 기술: {(results_df['Sentiment_Score'] < 0).sum()}명/{len(results_df)}명")
        print(f"  - 중립적 표현보다 부정적 표현을 더 많이 사용")

    print("\n")

if __name__ == "__main__":
    main()
