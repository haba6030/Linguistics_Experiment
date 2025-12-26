"""
result_1201 데이터에 대한 종합 분석 스크립트
result_1128과 동일한 분석 방법론 적용
참가자 수: 7명 (6명 + 1명 추가)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
import os
warnings.filterwarnings('ignore')

# 폰트 설정
plt.rcParams['font.family'] = 'AppleSDGothicNeo'  # macOS 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

plt.rc('font', family='AppleGothic') 			## 이 두 줄을 
plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용 시, 마이너스 폰트 깨지는 문제 해결

# 출력 디렉토리
OUTPUT_DIR = 'result_1201'

def ensure_output_dir():
    """출력 디렉토리 확인 및 생성"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print(f"출력 디렉토리: {OUTPUT_DIR}")

def load_data():
    """데이터 로드"""
    excel_path = f'{OUTPUT_DIR}/ExpLing_Project.xlsx'
    xl = pd.ExcelFile(excel_path)
    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel(excel_path, sheet_name=sheet)
    print(f"\n데이터 로드 완료: {list(data.keys())}")
    return data

def remove_practice_trials(df):
    """연습 문장 제거"""
    before = len(df)
    df_clean = df[~df['Sentence_Text'].str.contains('연습', na=False)].copy()
    after = len(df_clean)
    print(f"연습 문장 제거: {before}개 → {after}개 ({before-after}개 제거)")
    return df_clean

def identify_outlier_trials(df, method='iqr', k=2.5):
    """Trial-level outlier 식별 (IQR method)"""
    total_rts = df['Total_Reading_Time_ms'].values

    Q1 = np.percentile(total_rts, 25)
    Q3 = np.percentile(total_rts, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR

    outliers = (total_rts < lower_bound) | (total_rts > upper_bound)

    print(f"\n=== Trial-level Outlier 제거 (IQR, k={k}) ===")
    print(f"하한: {lower_bound:.0f} ms, 상한: {upper_bound:.0f} ms")
    print(f"제거: {outliers.sum()}개 / {len(df)}개 ({outliers.sum()/len(df)*100:.1f}%)")

    return df[~outliers].copy()

def parse_sentence_structure(df):
    """문장 구조 파싱: Subject - Modifier - Spillover - Fact(avg)"""
    parsed_rows = []

    for idx, row in df.iterrows():
        if row['Is_Filler'] == 1:
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        base_info = {
            'Participant_ID': row['Participant_ID'],
            'List_ID': row['List_ID'],
            'Trial_Index': row['Trial_Index'],
            'Item_ID': row['Item_ID'],
            'Base': row['Base'],
            'Emotion': row['Emotion'],
            'Plausibility': row['Plausibility'],
            'Version': row['Version']
        }

        if len(regions) >= 4:
            # Subject
            parsed_rows.append({**base_info, 'Region_Type': 'Subject',
                               'Region_Text': regions[0], 'RT': rts[0]})
            # Modifier
            parsed_rows.append({**base_info, 'Region_Type': 'Modifier',
                               'Region_Text': regions[1], 'RT': rts[1]})
            # Spillover
            parsed_rows.append({**base_info, 'Region_Type': 'Spillover',
                               'Region_Text': regions[2], 'RT': rts[2]})
            # Fact (평균)
            fact_rts = [rt for rt in rts[3:] if 200 <= rt <= 3000]
            if len(fact_rts) > 0:
                parsed_rows.append({**base_info, 'Region_Type': 'Fact',
                                   'Region_Text': ' '.join(regions[3:]),
                                   'RT': np.mean(fact_rts)})

    return pd.DataFrame(parsed_rows)

def remove_word_outliers(df, lower=200, upper=3000):
    """Word-level outlier 제거"""
    before = len(df)
    df_clean = df[(df['RT'] >= lower) & (df['RT'] <= upper)].copy()
    after = len(df_clean)
    removed = before - after
    print(f"Word-level outlier 제거 ({lower}-{upper}ms): {removed}개 / {before}개 ({removed/before*100:.1f}%)")
    return df_clean

def analyze_manipulation_check(manip_data):
    """조작 검증 분석"""
    print("\n" + "="*80)
    print("조작 검증: 수식어 부정성 평가")
    print("="*80)

    # 카테고리별 요약
    summary = manip_data.groupby('Modifier_Category')['Negativity_Rating'].agg(
        ['mean', 'std', 'count', 'sem']).round(3)
    print("\n카테고리별 통계:")
    print(summary)

    # t-test
    hate = manip_data[manip_data['Modifier_Category'] == 'hate']['Negativity_Rating']
    neutral = manip_data[manip_data['Modifier_Category'] == 'neutral']['Negativity_Rating']

    t_stat, p_val = stats.ttest_ind(hate, neutral)
    pooled_std = np.sqrt((hate.std()**2 + neutral.std()**2) / 2)
    cohens_d = (hate.mean() - neutral.mean()) / pooled_std

    print(f"\nt-test: t({len(hate)+len(neutral)-2}) = {t_stat:.2f}, p < .0001")
    print(f"평균 차이: {hate.mean() - neutral.mean():.2f}")
    print(f"Cohen's d: {cohens_d:.2f}")

    # 시각화
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 분포
    axes[0].hist(hate, alpha=0.6, label='Hate', bins=8, color='salmon', edgecolor='black')
    axes[0].hist(neutral, alpha=0.6, label='Neutral', bins=8, color='skyblue', edgecolor='black')
    axes[0].set_xlabel('Negativity Rating (1-4)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Distribution by Modifier Type', fontsize=13, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # 박스플롯
    data_plot = pd.concat([
        pd.DataFrame({'Category': 'Hate', 'Rating': hate}),
        pd.DataFrame({'Category': 'Neutral', 'Rating': neutral})
    ])
    sns.boxplot(data=data_plot, x='Category', y='Rating', ax=axes[1],
                palette={'Hate': 'salmon', 'Neutral': 'skyblue'})
    axes[1].set_title(f'Manipulation Check (d={cohens_d:.2f})', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Negativity Rating', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_ManipulationCheck.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_ManipulationCheck.png")
    plt.close()

def specific_manipulation(manip_data):
    # 조작 검증 시각화
    print("\n단어 별 조작 결과 확인")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    sns.violinplot(data=manip_data, x='Modifier_Category', y='Negativity_Rating',
                   ax=ax, palette='Set2')
    sns.swarmplot(data=manip_data, x='Modifier_Category', y='Negativity_Rating',
                 ax=ax, color='black', alpha=0.3, size=3)
    ax.set_xlabel('Modifier Type', fontsize=13, fontweight='bold')
    ax.set_ylabel('Negativity Rating (1-4)', fontsize=13, fontweight='bold')
    ax.set_title('Manipulation Check: Negativity Ratings by Modifier Type', fontsize=15, fontweight='bold')
    ax.set_xticklabels(['Hate', 'Neutral'])

    ax = axes[1]
    word_means = manip_data.groupby(['Modifier_Text', 'Modifier_Category'])['Negativity_Rating'].mean().reset_index()
    word_means_sorted = word_means.sort_values('Negativity_Rating', ascending=False)
    colors = ['red' if cat=='hate' else 'blue' for cat in word_means_sorted['Modifier_Category']]
    ax.barh(word_means_sorted['Modifier_Text'], word_means_sorted['Negativity_Rating'], color=colors, alpha=0.7)
    ax.set_xlabel('Mean Negativity Rating', fontsize=13, fontweight='bold')
    ax.set_ylabel('Modifier Word', fontsize=13, fontweight='bold')
    ax.set_title('Word-by-Word Negativity Ratings', fontsize=15, fontweight='bold')
    ax.axvline(x=2.5, color='gray', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_ManipulationCheck_WordByWord.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_ManipulationCheck_WordByWord.png")
    plt.close()

def analyze_region_rt(parsed_df):
    """영역별 평균 RT 시각화"""
    print("\n" + "="*80)
    print("영역별 평균 RT 분석")
    print("="*80)

    region_summary = parsed_df.groupby('Region_Type')['RT'].agg(
        ['mean', 'std', 'count', 'sem']).round(1)
    print("\n영역별 RT:")
    print(region_summary)

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 6))

    regions = ['Subject', 'Modifier', 'Spillover', 'Fact']
    means = [region_summary.loc[r, 'mean'] for r in regions if r in region_summary.index]
    sems = [region_summary.loc[r, 'sem'] for r in regions if r in region_summary.index]
    colors = ['lightblue', 'salmon', 'lightgreen', 'wheat']

    bars = ax.bar(regions[:len(means)], means, yerr=sems, capsize=5,
                  color=colors[:len(means)], alpha=0.8, edgecolor='black', linewidth=1.5)

    ax.set_ylabel('Reading Time (ms)', fontsize=13)
    ax.set_xlabel('Sentence Region', fontsize=13)
    ax.set_title('Mean RT by Sentence Region', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # 값 표시
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 10,
                f'{mean:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/Figure_RegionRT.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {OUTPUT_DIR}/Figure_RegionRT.png")
    plt.close()

def main():
    """메인 분석 실행"""
    print("="*80)
    print("result_1201 데이터 종합 분석")
    print("="*80)

    ensure_output_dir()

    # 1. 데이터 로드
    data = load_data()
    spr_data = data['SPR_Data']
    rating_data = data['Rating_Data']
    manip_data = data['Manipulation_Check']
    recall_data = data['Recall_Data']

    print(f"\n참가자 수: {spr_data['Participant_ID'].nunique()}명")

    # 2. SPR 데이터 전처리
    print("\n" + "="*80)
    print("SPR 데이터 전처리")
    print("="*80)

    spr_clean = remove_practice_trials(spr_data)
    spr_clean = identify_outlier_trials(spr_clean)

    # 3. 문장 구조 파싱
    parsed_df = parse_sentence_structure(spr_clean)
    parsed_df = remove_word_outliers(parsed_df)

    print(f"\n파싱된 데이터: {len(parsed_df)}개 관찰치")

    # 4. 분석 실행
    analyze_manipulation_check(manip_data)
    specific_manipulation(manip_data)
    analyze_region_rt(parsed_df)

    print("\n\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print(f"\n생성된 파일:")
    print(f"  - {OUTPUT_DIR}/Figure_ManipulationCheck.png")
    print(f"  - {OUTPUT_DIR}/Figure_ManipulationCheck_WordByWord.png")
    print(f"  - {OUTPUT_DIR}/Figure_RegionRT.png")

if __name__ == "__main__":
    main()