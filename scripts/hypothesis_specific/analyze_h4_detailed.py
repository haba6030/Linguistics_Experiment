"""
H4 회상 데이터 상세 분석
- 부정적 표현 (확장된 사전)
- 잘못된 정보 (implausible 정보)
- 참가자별 정성적 분석
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

OUTPUT_DIR = 'result_1201'

def analyze_recall_detailed():
    """회상 데이터 상세 분석"""

    print("="*80)
    print("H4: 회상 데이터 상세 분석")
    print("="*80)

    recall = pd.read_excel(f'{OUTPUT_DIR}/ExpLing_Project.xlsx', sheet_name='Recall_Data')

    # 배경 사실
    background_facts = ['중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
                        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
                        '허브', '노래', '짧은', '반복', '유목', '정착']

    # 부정적 표현 (확장)
    negative_words = {
        '직접적 혐오': ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡'],
        '간접적 부정': ['천박', '무지', '수준 낮', '낙후', '원시', '조악'],
        '비하적': ['하찮', '졸렬', '단순', '부족']
    }

    # 잘못된 정보 (Implausible 문장에서 나온 내용들)
    false_info = [
        '금속', '고층', '사막', '날개', '날아', '비행', '점프', '뛰어넘',
        '금', '바꾼', '흙을 먹', '씹어먹', '물에 잠기', '떨어져', '재탄생',
        '매일 이동', '조립', '몸을 갖다대'
    ]

    # 중립적 서술
    neutral_descriptors = ['생활', '문화', '전통', '기술', '예술', '자연', '적응']

    results = []

    print("\n" + "="*80)
    print("참가자별 상세 분석")
    print("="*80)

    for idx, row in recall.iterrows():
        pid = row['Participant_ID']
        text = row['Recall_Text']

        print(f"\n{'='*80}")
        print(f"참가자 {pid}")
        print(f"{'='*80}")
        print(f"원문:\n{text}\n")

        # 1. 사실 포함
        facts_found = [fact for fact in background_facts if fact in text]
        fact_count = len(facts_found)

        # 2. 부정 표현 분석
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

        # 3. 잘못된 정보 분석
        false_info_found = [info for info in false_info if info in text]
        false_count = len(false_info_found)

        # 4. 중립 표현
        neutral_found = [word for word in neutral_descriptors if word in text]
        neutral_count = len(neutral_found)

        # 5. 텍스트 특성
        text_length = len(text)
        sentence_count = text.count('.') + text.count('。') + text.count('\n')

        # 6. 감정 점수 (중립 - 부정)
        sentiment = neutral_count - neg_total

        print(f"사실 포함: {fact_count}개")
        print(f"  → {', '.join(facts_found[:10])}{'...' if len(facts_found) > 10 else ''}")

        print(f"\n부정 표현: {neg_total}개")
        if neg_words_found:
            print(f"  → {', '.join(neg_words_found)}")
        else:
            print(f"  → 없음")

        print(f"\n잘못된 정보: {false_count}개")
        if false_info_found:
            print(f"  → {', '.join(false_info_found)}")
        else:
            print(f"  → 없음")

        print(f"\n중립 표현: {neutral_count}개")
        if neutral_found:
            print(f"  → {', '.join(neutral_found)}")

        print(f"\n텍스트 길이: {text_length}자, 문장: {sentence_count}개")
        print(f"감정 점수: {sentiment} (양수=중립적, 음수=부정적)")

        # 정성적 평가
        if neg_total > 0 or false_count > 2:
            print("\n⚠️ 주의: 부정 표현 또는 잘못된 정보 포함")

        results.append({
            'Participant_ID': pid,
            'Text_Length': text_length,
            'Sentence_Count': sentence_count,
            'Fact_Count': fact_count,
            'Fact_Ratio': fact_count / len(background_facts),
            'Negative_Direct': neg_direct,
            'Negative_Indirect': neg_indirect,
            'Negative_Derogatory': neg_derogatory,
            'Negative_Total': neg_total,
            'False_Info_Count': false_count,
            'Neutral_Count': neutral_count,
            'Sentiment_Score': sentiment,
            'Negative_Words': ', '.join(neg_words_found) if neg_words_found else 'None',
            'False_Info': ', '.join(false_info_found) if false_info_found else 'None'
        })

    results_df = pd.DataFrame(results)

    # 요약 통계
    print("\n\n" + "="*80)
    print("전체 요약 통계")
    print("="*80)

    summary = results_df[['Fact_Count', 'Negative_Total', 'False_Info_Count',
                          'Neutral_Count', 'Sentiment_Score']].describe().round(2)
    print(summary)

    print(f"\n부정 표현 사용자: {(results_df['Negative_Total'] > 0).sum()}명 / {len(results_df)}명")
    print(f"잘못된 정보 포함: {(results_df['False_Info_Count'] > 0).sum()}명 / {len(results_df)}명")

    # 시각화
    visualize_h4_detailed(results_df)

    # 저장
    results_df.to_csv(f'{OUTPUT_DIR}/h4_detailed_analysis.csv', index=False)
    print(f"\n저장: {OUTPUT_DIR}/h4_detailed_analysis.csv")

    return results_df

def visualize_h4_detailed(results_df):
    """H4 상세 분석 시각화"""

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # Panel 1: 참가자별 부정 표현
    x_pos = np.arange(len(results_df))

    axes[0,0].bar(x_pos, results_df['Negative_Total'],
                  color='darkred', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('Participant', fontsize=12)
    axes[0,0].set_ylabel('Negative Expression Count', fontsize=12)
    axes[0,0].set_title('H4: Negative Expressions Used', fontsize=13, fontweight='bold')
    axes[0,0].set_xticks(x_pos)
    axes[0,0].set_xticklabels([str(pid)[:6] for pid in results_df['Participant_ID']],
                              rotation=45, ha='right')
    axes[0,0].grid(axis='y', alpha=0.3)

    # 값 표시
    for i, v in enumerate(results_df['Negative_Total']):
        if v > 0:
            axes[0,0].text(i, v + 0.1, str(int(v)), ha='center', va='bottom',
                          fontweight='bold', fontsize=10)

    # Panel 2: 잘못된 정보
    axes[0,1].bar(x_pos, results_df['False_Info_Count'],
                  color='orange', alpha=0.7, edgecolor='black')
    axes[0,1].set_xlabel('Participant', fontsize=12)
    axes[0,1].set_ylabel('False Information Count', fontsize=12)
    axes[0,1].set_title('H4: False/Implausible Information', fontsize=13, fontweight='bold')
    axes[0,1].set_xticks(x_pos)
    axes[0,1].set_xticklabels([str(pid)[:6] for pid in results_df['Participant_ID']],
                              rotation=45, ha='right')
    axes[0,1].grid(axis='y', alpha=0.3)

    for i, v in enumerate(results_df['False_Info_Count']):
        if v > 0:
            axes[0,1].text(i, v + 0.1, str(int(v)), ha='center', va='bottom',
                          fontweight='bold', fontsize=10)

    # Panel 3: 감정 점수
    colors = ['green' if s >= 0 else 'red' for s in results_df['Sentiment_Score']]
    axes[0,2].bar(x_pos, results_df['Sentiment_Score'],
                  color=colors, alpha=0.7, edgecolor='black')
    axes[0,2].axhline(0, color='black', linestyle='--', linewidth=1)
    axes[0,2].set_xlabel('Participant', fontsize=12)
    axes[0,2].set_ylabel('Sentiment Score', fontsize=12)
    axes[0,2].set_title('Sentiment: Neutral - Negative', fontsize=13, fontweight='bold')
    axes[0,2].set_xticks(x_pos)
    axes[0,2].set_xticklabels([str(pid)[:6] for pid in results_df['Participant_ID']],
                              rotation=45, ha='right')
    axes[0,2].grid(axis='y', alpha=0.3)

    # Panel 4: 사실 vs 부정 표현
    axes[1,0].scatter(results_df['Fact_Count'], results_df['Negative_Total'],
                     s=100, alpha=0.6, color='purple', edgecolor='black')
    for idx, row in results_df.iterrows():
        axes[1,0].annotate(str(row['Participant_ID'])[:6],
                          (row['Fact_Count'], row['Negative_Total']),
                          fontsize=9, ha='right', va='bottom')
    axes[1,0].set_xlabel('Fact Count', fontsize=12)
    axes[1,0].set_ylabel('Negative Expressions', fontsize=12)
    axes[1,0].set_title('Facts vs Negative Expressions', fontsize=13, fontweight='bold')
    axes[1,0].grid(alpha=0.3)

    # Panel 5: 사실 vs 잘못된 정보
    axes[1,1].scatter(results_df['Fact_Count'], results_df['False_Info_Count'],
                     s=100, alpha=0.6, color='darkorange', edgecolor='black')
    for idx, row in results_df.iterrows():
        axes[1,1].annotate(str(row['Participant_ID'])[:6],
                          (row['Fact_Count'], row['False_Info_Count']),
                          fontsize=9, ha='right', va='bottom')
    axes[1,1].set_xlabel('Fact Count', fontsize=12)
    axes[1,1].set_ylabel('False Information Count', fontsize=12)
    axes[1,1].set_title('Facts vs False Information', fontsize=13, fontweight='bold')
    axes[1,1].grid(alpha=0.3)

    # Panel 6: 종합 비교
    width = 0.25
    x = np.arange(len(results_df))

    axes[1,2].bar(x - width, results_df['Fact_Count'], width,
                  label='Facts', color='green', alpha=0.7, edgecolor='black')
    axes[1,2].bar(x, results_df['Negative_Total'], width,
                  label='Negative', color='red', alpha=0.7, edgecolor='black')
    axes[1,2].bar(x + width, results_df['False_Info_Count'], width,
                  label='False Info', color='orange', alpha=0.7, edgecolor='black')

    axes[1,2].set_xlabel('Participant', fontsize=12)
    axes[1,2].set_ylabel('Count', fontsize=12)
    axes[1,2].set_title('Comprehensive Comparison', fontsize=13, fontweight='bold')
    axes[1,2].set_xticks(x)
    axes[1,2].set_xticklabels([str(pid)[:6] for pid in results_df['Participant_ID']],
                              rotation=45, ha='right')
    axes[1,2].legend()
    axes[1,2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_H4_Detailed.png', dpi=300, bbox_inches='tight')
    print(f"\n저장: {OUTPUT_DIR}/Figure_H4_Detailed.png")
    plt.close()

def main():
    results_df = analyze_recall_detailed()

    print("\n\n" + "="*80)
    print("H4 상세 분석 완료")
    print("="*80)
    print("\n핵심 발견:")

    neg_users = results_df[results_df['Negative_Total'] > 0]
    if len(neg_users) > 0:
        print(f"\n✅ 부정 표현 사용: {len(neg_users)}명")
        for _, row in neg_users.iterrows():
            print(f"  - {row['Participant_ID']}: {int(row['Negative_Total'])}개 - {row['Negative_Words']}")

    false_users = results_df[results_df['False_Info_Count'] > 0]
    if len(false_users) > 0:
        print(f"\n✅ 잘못된 정보 포함: {len(false_users)}명")
        for _, row in false_users.iterrows():
            print(f"  - {row['Participant_ID']}: {int(row['False_Info_Count'])}개 - {row['False_Info'][:50]}...")

    print("\n➡️ 기존 분석 문제점:")
    print("   - 부정 표현 사전이 너무 제한적 (직접적 혐오 8개만)")
    print("   - 간접적 부정, 비하적 표현 누락")
    print("   - 잘못된 정보(false memory) 분석 누락")

if __name__ == "__main__":
    main()
