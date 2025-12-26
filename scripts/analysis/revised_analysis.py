"""
수정된 분석 스크립트
- 연습 문장 제거
- 문장 구조: 주어 - 수식어 - spillover - 사실부분(평균)
- Trial-level outlier 제거
- 단어별 조작 검증
- 회상 데이터 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import mixedlm
import warnings
import re
warnings.filterwarnings('ignore')

# Font settings - use English to avoid font issues
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def load_data():
    """데이터 로드"""
    xl = pd.ExcelFile('result_1128/ExpLing_Project.xlsx')
    data = {}
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel('result_1128/ExpLing_Project.xlsx', sheet_name=sheet)
    return data

def remove_practice_trials(df):
    """연습 문장 제거"""
    # "연습" 포함된 문장 제거
    before = len(df)
    df_clean = df[~df['Sentence_Text'].str.contains('연습', na=False)].copy()
    after = len(df_clean)
    print(f"\n연습 문장 제거: {before}개 → {after}개 ({before-after}개 제거)")
    return df_clean

def identify_outlier_trials(df, method='iqr', k=2.5):
    """
    Trial-level outlier 식별
    기준: Total_Reading_Time이 IQR * k를 벗어나는 trial
    또는 평균 ± 2.5 SD를 벗어나는 trial
    """
    total_rts = df['Total_Reading_Time_ms'].values

    if method == 'iqr':
        Q1 = np.percentile(total_rts, 25)
        Q3 = np.percentile(total_rts, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        criterion = f"IQR method (k={k})"
    else:  # sd method
        mean_rt = np.mean(total_rts)
        sd_rt = np.std(total_rts)
        lower_bound = mean_rt - k * sd_rt
        upper_bound = mean_rt + k * sd_rt
        criterion = f"SD method (±{k} SD)"

    outliers = (total_rts < lower_bound) | (total_rts > upper_bound)

    print(f"\n=== Trial-level Outlier 제거 ===")
    print(f"기준: {criterion}")
    print(f"하한: {lower_bound:.0f} ms")
    print(f"상한: {upper_bound:.0f} ms")
    print(f"제거된 trial: {outliers.sum()}개 / {len(df)}개 ({outliers.sum()/len(df)*100:.1f}%)")

    return df[~outliers].copy(), criterion, lower_bound, upper_bound

def parse_sentence_structure(df):
    """
    문장 구조 파싱: 주어 - 수식어 - spillover - 사실부분(평균)
    탈렌족은(주어) - 저급한(수식어) - 민족으로(spillover) - 나머지(사실부분)
    """
    parsed_rows = []

    for idx, row in df.iterrows():
        if row['Is_Filler'] == 1:  # 필러는 제외
            continue

        regions = eval(row['Regions'])
        rts = eval(row['Region_RTs'])

        # 기본 정보
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

        # 문장 구조 파싱
        # 첫 번째: 주어 (탈렌족은/탈렌족의 등)
        # 두 번째: 수식어 (저급한, 정착한 등)
        # 세 번째: spillover (민족으로,)
        # 나머지: 사실부분

        if len(regions) >= 4:
            # 주어
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Subject',
                'Region_Text': regions[0],
                'RT': rts[0]
            })

            # 수식어
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Modifier',
                'Region_Text': regions[1],
                'RT': rts[1]
            })

            # Spillover
            parsed_rows.append({
                **base_info,
                'Region_Type': 'Spillover',
                'Region_Text': regions[2],
                'RT': rts[2]
            })

            # 사실부분 (평균)
            fact_regions = regions[3:]
            fact_rts = rts[3:]

            # Word-level outlier 제거 (200-3000ms)
            valid_rts = [rt for rt in fact_rts if 200 <= rt <= 3000]
            if len(valid_rts) > 0:
                avg_fact_rt = np.mean(valid_rts)
                parsed_rows.append({
                    **base_info,
                    'Region_Type': 'Fact',
                    'Region_Text': ' '.join(fact_regions),
                    'RT': avg_fact_rt
                })

    return pd.DataFrame(parsed_rows)

def remove_word_outliers(df, lower=200, upper=3000):
    """Word-level outlier 제거"""
    before = len(df)
    df_clean = df[(df['RT'] >= lower) & (df['RT'] <= upper)].copy()
    after = len(df_clean)
    removed = before - after
    print(f"\nWord-level outlier 제거 (200-3000ms): {removed}개 / {before}개 ({removed/before*100:.1f}%)")
    return df_clean

def analyze_manipulation_check_by_word(manip_data):
    """조작 검증: 단어별 평가"""
    print("\n" + "="*80)
    print("조작 검증: 단어별 부정성 평가")
    print("="*80)

    # 단어별 평균
    word_summary = manip_data.groupby(['Modifier_Text', 'Modifier_Category']).agg({
        'Negativity_Rating': ['mean', 'std', 'count']
    }).round(2)

    print("\n단어별 부정성 평가 요약:")
    print(word_summary)

    # 전체 통계
    print("\n\n=== 전체 카테고리별 통계 ===")
    cat_summary = manip_data.groupby('Modifier_Category')['Negativity_Rating'].agg(['mean', 'std', 'count', 'sem'])
    print(cat_summary)

    hate_ratings = manip_data[manip_data['Modifier_Category'] == 'hate']['Negativity_Rating']
    neutral_ratings = manip_data[manip_data['Modifier_Category'] == 'neutral']['Negativity_Rating']

    t_stat, p_val = stats.ttest_ind(hate_ratings, neutral_ratings)
    pooled_std = np.sqrt((hate_ratings.std()**2 + neutral_ratings.std()**2) / 2)
    cohens_d = (hate_ratings.mean() - neutral_ratings.mean()) / pooled_std

    print(f"\nt-test: t({len(hate_ratings)+len(neutral_ratings)-2}) = {t_stat:.3f}, p = {p_val:.4f}")
    print(f"평균 차이: {hate_ratings.mean() - neutral_ratings.mean():.2f} points")
    print(f"Cohen's d: {cohens_d:.3f}")

    return word_summary

def power_analysis(observed_d, alpha=0.05, power=0.80):
    """
    필요한 참가자 수 계산
    효과크기 기반 power analysis
    """
    from scipy.stats import norm, t as t_dist

    print("\n" + "="*80)
    print("필요 참가자 수 산출 (Power Analysis)")
    print("="*80)

    # 현재 데이터
    current_n = 6

    # 여러 효과크기에 대해 계산
    effect_sizes = {
        '관찰된 효과크기 (H1: d≈0.05)': 0.05,
        '작은 효과 (d=0.2)': 0.2,
        '중간 효과 (d=0.5)': 0.5,
        '큰 효과 (d=0.8)': 0.8
    }

    print(f"\n목표: Power = {power}, α = {alpha} (양측검정)")
    print(f"현재 참가자 수: {current_n}명\n")

    results = []

    for desc, d in effect_sizes.items():
        # Cohen (1988) 공식 기반 근사치
        # n ≈ 2 * ((Z_α/2 + Z_β) / d)^2
        z_alpha = norm.ppf(1 - alpha/2)  # 1.96 for α=0.05
        z_beta = norm.ppf(power)  # 0.84 for power=0.80

        n_per_group = 2 * ((z_alpha + z_beta) / d) ** 2

        # Within-subjects는 correlation 고려하여 더 적게 필요
        # 보수적으로 r=0.5 가정
        r = 0.5
        n_within = n_per_group * (1 - r)

        results.append({
            '효과크기': desc,
            'd': d,
            '필요 N (between)': int(np.ceil(n_per_group)),
            '필요 N (within, r=.5)': int(np.ceil(n_within))
        })

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    print("\n\n=== 결론 ===")
    print(f"- 작은 효과(d=0.2) 탐지: 약 {int(np.ceil(2*((z_alpha+z_beta)/0.2)**2*(1-r)))}명 필요")
    print(f"- 중간 효과(d=0.5) 탐지: 약 {int(np.ceil(2*((z_alpha+z_beta)/0.5)**2*(1-r)))}명 필요")
    print(f"- 큰 효과(d=0.8) 탐지: 약 {int(np.ceil(2*((z_alpha+z_beta)/0.8)**2*(1-r)))}명 필요")
    print(f"\n권장: 중간 효과크기 기준 최소 30-35명 모집")

    return results_df

def analyze_recall_data(recall_data):
    """
    회상 데이터 분석
    1. 사실 포함 정도
    2. 배경지문 대비 오류율
    3. 탈렌족에 대한 정서적 경향
    """
    print("\n" + "="*80)
    print("회상 데이터 분석 (자유 회상)")
    print("="*80)

    # 배경 지문의 핵심 사실들 (정답 기준)
    background_facts = [
        '중앙아시아', '협곡', '산악', '반지하', '흙', '돌',
        '산양', '오리', '정령', '의식', '장인', '도기', '뼈',
        '허브', '노래', '짧은', '반복', '유목', '정착'
    ]

    results = []

    for idx, row in recall_data.iterrows():
        text = row['Recall_Text']
        participant_id = row['Participant_ID']

        # 1. 사실 포함 정도
        fact_count = sum(1 for fact in background_facts if fact in text)
        fact_ratio = fact_count / len(background_facts)

        # 2. 부정적 표현 탐지
        negative_words = ['저급', '야만', '후진', '열등', '미개', '더러', '무식', '조잡']
        negative_count = sum(text.count(word) for word in negative_words)

        # 3. 긍정적/중립적 표현
        neutral_words = ['생활', '문화', '전통', '기술', '예술', '음식', '의식']
        neutral_count = sum(text.count(word) for word in neutral_words)

        # 4. 텍스트 길이
        text_length = len(text)

        # 5. 문장 수
        sentence_count = text.count('.') + text.count('。')

        results.append({
            'Participant_ID': participant_id,
            'Text_Length': text_length,
            'Sentence_Count': sentence_count,
            'Fact_Count': fact_count,
            'Fact_Ratio': fact_ratio,
            'Negative_Count': negative_count,
            'Neutral_Count': neutral_count,
            'Sentiment_Score': neutral_count - negative_count,  # 양수면 중립적, 음수면 부정적
            'Text': text[:100] + '...'  # 첫 100자만
        })

    results_df = pd.DataFrame(results)

    print("\n참가자별 회상 패턴:")
    print(results_df[['Participant_ID', 'Text_Length', 'Fact_Count', 'Fact_Ratio',
                      'Negative_Count', 'Neutral_Count', 'Sentiment_Score']].to_string(index=False))

    print(f"\n\n=== 전체 평균 ===")
    print(f"평균 사실 포함: {results_df['Fact_Count'].mean():.1f}개 ({results_df['Fact_Ratio'].mean()*100:.1f}%)")
    print(f"평균 부정 표현: {results_df['Negative_Count'].mean():.1f}개")
    print(f"평균 중립 표현: {results_df['Neutral_Count'].mean():.1f}개")
    print(f"평균 감정 점수: {results_df['Sentiment_Score'].mean():.1f} (양수=중립적, 음수=부정적)")

    # 개별 텍스트 출력
    print("\n\n=== 개별 회상 텍스트 ===")
    for idx, row in results_df.iterrows():
        print(f"\n참가자 {row['Participant_ID']}:")
        print(f"  사실: {row['Fact_Count']}개 | 부정: {row['Negative_Count']}개 | 감정점수: {row['Sentiment_Score']}")
        print(f"  내용: {row['Text']}")

    return results_df

def test_hypotheses(parsed_data):
    """가설 검증"""

    print("\n" + "="*80)
    print("H1: 혐오 수식어에서의 주의 포착 (Attention Capture)")
    print("="*80)

    # H1: Modifier RT
    modifier_data = parsed_data[parsed_data['Region_Type'] == 'Modifier'].copy()

    print("\n수식어 영역 RT (Emotion별):")
    h1_desc = modifier_data.groupby('Emotion')['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(h1_desc)

    # Paired t-test
    hate_rt = modifier_data[modifier_data['Emotion'] == 'H'].groupby('Participant_ID')['RT'].mean()
    neutral_rt = modifier_data[modifier_data['Emotion'] == 'N'].groupby('Participant_ID')['RT'].mean()

    t_stat, p_val = stats.ttest_rel(hate_rt, neutral_rt)
    cohens_d = (hate_rt.mean() - neutral_rt.mean()) / hate_rt.std()

    print(f"\nPaired t-test: t({len(hate_rt)-1}) = {t_stat:.3f}, p = {p_val:.4f}")
    print(f"평균 차이: {hate_rt.mean() - neutral_rt.mean():.1f} ms")
    print(f"Cohen's d: {cohens_d:.3f}")

    # Mixed model
    try:
        model = mixedlm("RT ~ C(Emotion)", modifier_data, groups=modifier_data["Participant_ID"])
        result = model.fit(method='powell')
        print("\n\nMixed Effects Model:")
        print(result.summary())
    except Exception as e:
        print(f"\nMixed model 실패: {e}")

    print("\n" + "="*80)
    print("H2: 주의 협소화 및 얕은 통합 (Attention Narrowing)")
    print("="*80)

    # H2: Spillover + Fact regions
    critical_data = parsed_data[parsed_data['Region_Type'].isin(['Spillover', 'Fact'])].copy()

    print("\nCritical Region RT (Emotion × Plausibility):")
    h2_desc = critical_data.groupby(['Emotion', 'Plausibility'])['RT'].agg(['mean', 'std', 'count', 'sem'])
    print(h2_desc)

    # Plausibility effect by Emotion
    print("\n\nPlausibility Effect (Implausible - Plausible):")
    for emotion in ['H', 'N']:
        emotion_data = critical_data[critical_data['Emotion'] == emotion]
        plaus_rt = emotion_data[emotion_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        implaus_rt = emotion_data[emotion_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        common_p = plaus_rt.index.intersection(implaus_rt.index)
        if len(common_p) > 0:
            p_aligned = plaus_rt.loc[common_p]
            i_aligned = implaus_rt.loc[common_p]

            effect = i_aligned.mean() - p_aligned.mean()
            t_stat, p_val = stats.ttest_rel(i_aligned, p_aligned)

            print(f"  {emotion}: {effect:.1f} ms (t={t_stat:.3f}, p={p_val:.4f})")

    # Interaction test
    try:
        model = mixedlm("RT ~ C(Emotion) * C(Plausibility)", critical_data,
                       groups=critical_data["Participant_ID"])
        result = model.fit(method='powell')
        print("\n\nMixed Effects Model (Emotion × Plausibility):")
        print(result.summary())
    except Exception as e:
        print(f"\nMixed model 실패: {e}")

    return modifier_data, critical_data, h1_desc, h2_desc

def create_visualizations(parsed_data, modifier_data, critical_data, manip_data):
    """각 가설별 개별 시각화"""

    # 조작 검증 시각화
    print("\n조작 검증 시각화 생성 중...")
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
    plt.savefig('result_1128/Figure_ManipulationCheck.png', dpi=300, bbox_inches='tight')
    print("저장: result_1128/Figure_ManipulationCheck.png")
    plt.close()

    # H1 시각화
    print("H1 시각화 생성 중...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    sns.barplot(data=modifier_data, x='Emotion', y='RT', errorbar='se', ax=ax, palette='Set1')
    ax.set_xlabel('Emotion Condition', fontsize=13, fontweight='bold')
    ax.set_ylabel('Reading Time (ms)', fontsize=13, fontweight='bold')
    ax.set_title('H1: Reading Time at Modifier Region', fontsize=15, fontweight='bold')
    ax.set_xticklabels(['Hate (H)', 'Neutral (N)'])

    # Add significance annotation
    hate_mean = modifier_data[modifier_data['Emotion']=='H']['RT'].mean()
    neutral_mean = modifier_data[modifier_data['Emotion']=='N']['RT'].mean()
    max_y = max(hate_mean, neutral_mean) * 1.1
    ax.plot([0, 1], [max_y, max_y], 'k-', linewidth=1)
    ax.text(0.5, max_y*1.02, 'n.s.', ha='center', fontsize=11)

    ax = axes[1]
    modifier_data[modifier_data['Emotion']=='H']['RT'].hist(bins=25, alpha=0.6, label='Hate (H)',
                                                              color='red', ax=ax)
    modifier_data[modifier_data['Emotion']=='N']['RT'].hist(bins=25, alpha=0.6, label='Neutral (N)',
                                                              color='blue', ax=ax)
    ax.set_xlabel('Reading Time (ms)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title('RT Distribution: Modifier Region', fontsize=15, fontweight='bold')
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H1_AttentionCapture.png', dpi=300, bbox_inches='tight')
    print("저장: result_1128/Figure_H1_AttentionCapture.png")
    plt.close()

    # H2 시각화 (2x2 design + 효과/상호작용)
    print("H2 시각화 생성 중...")
    fig = plt.figure(figsize=(18, 6))

    # Panel 1: 2x2 bar plot
    ax1 = plt.subplot(1, 3, 1)
    h2_summary = critical_data.groupby(['Emotion', 'Plausibility'])['RT'].mean().reset_index()
    h2_summary['Condition'] = h2_summary['Emotion'] + h2_summary['Plausibility']
    condition_map = {'HP': 'Hate-Plausible', 'HI': 'Hate-Implausible',
                     'NP': 'Neutral-Plausible', 'NI': 'Neutral-Implausible'}
    h2_summary['Condition_Label'] = h2_summary['Condition'].map(condition_map)

    colors_map = {'HP': '#ff9999', 'HI': '#ff0000', 'NP': '#9999ff', 'NI': '#0000ff'}
    colors = [colors_map[c] for c in h2_summary['Condition']]

    bars = ax1.bar(range(4), h2_summary['RT'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(4))
    ax1.set_xticklabels(h2_summary['Condition_Label'], rotation=15, ha='right', fontsize=10)
    ax1.set_ylabel('Mean Reading Time (ms)', fontsize=13, fontweight='bold')
    ax1.set_title('H2: 2x2 Design (Emotion x Plausibility)', fontsize=15, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Panel 2: Interaction plot
    ax2 = plt.subplot(1, 3, 2)
    interaction_data = critical_data.groupby(['Participant_ID', 'Emotion', 'Plausibility'])['RT'].mean().reset_index()

    for emotion, color, marker in [('H', 'red', 'o'), ('N', 'blue', 's')]:
        emotion_data = interaction_data[interaction_data['Emotion'] == emotion]
        plaus_means = emotion_data.groupby('Plausibility')['RT'].agg(['mean', 'sem']).reset_index()
        plaus_means = plaus_means.sort_values('Plausibility')  # I, P order

        ax2.errorbar([0, 1], plaus_means['mean'], yerr=plaus_means['sem'],
                    marker=marker, markersize=10, linewidth=2.5, capsize=5,
                    label='Hate' if emotion=='H' else 'Neutral', color=color)

    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Implausible (I)', 'Plausible (P)'])
    ax2.set_xlabel('Plausibility', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Mean Reading Time (ms)', fontsize=13, fontweight='bold')
    ax2.set_title('H2: Emotion x Plausibility Interaction', fontsize=15, fontweight='bold')
    ax2.legend(fontsize=12, title='Emotion')
    ax2.grid(alpha=0.3)

    # Panel 3: Effect sizes
    ax3 = plt.subplot(1, 3, 3)

    # Calculate effects
    effects = []
    for emotion in ['H', 'N']:
        emotion_data = critical_data[critical_data['Emotion'] == emotion]
        plaus_rt = emotion_data[emotion_data['Plausibility'] == 'P'].groupby('Participant_ID')['RT'].mean()
        implaus_rt = emotion_data[emotion_data['Plausibility'] == 'I'].groupby('Participant_ID')['RT'].mean()

        common_p = plaus_rt.index.intersection(implaus_rt.index)
        if len(common_p) > 0:
            effect = implaus_rt.loc[common_p].mean() - plaus_rt.loc[common_p].mean()
            effects.append(effect)

    effect_labels = ['Hate', 'Neutral']
    colors_effect = ['red', 'blue']
    bars = ax3.barh(effect_labels, effects, color=colors_effect, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax3.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax3.set_xlabel('Plausibility Effect (Implaus - Plaus, ms)', fontsize=13, fontweight='bold')
    ax3.set_title('H2: Plausibility Effect by Emotion', fontsize=15, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)

    # Annotate values
    for i, (bar, effect) in enumerate(zip(bars, effects)):
        ax3.text(effect + 3, i, f'{effect:.1f}ms', va='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('result_1128/Figure_H2_AttentionNarrowing.png', dpi=300, bbox_inches='tight')
    print("저장: result_1128/Figure_H2_AttentionNarrowing.png")
    plt.close()

    # Overall word position visualization
    print("전체 영역별 RT 시각화 생성 중...")
    fig, ax = plt.subplots(figsize=(12, 6))

    region_order = ['Subject', 'Modifier', 'Spillover', 'Fact']
    region_labels = ['Subject', 'Modifier', 'Spillover', 'Fact Region']

    region_summary = parsed_data.groupby('Region_Type')['RT'].agg(['mean', 'sem']).reindex(region_order)

    bars = ax.bar(region_labels, region_summary['mean'], yerr=region_summary['sem'],
                  color=['gray', 'orange', 'green', 'skyblue'], alpha=0.8,
                  capsize=7, edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Sentence Region', fontsize=14, fontweight='bold')
    ax.set_ylabel('Mean Reading Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('Mean Reading Time by Sentence Region', fontsize=16, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Annotate values
    for bar, mean in zip(bars, region_summary['mean']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 10,
                f'{mean:.0f}ms', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('result_1128/Figure_RegionRT.png', dpi=300, bbox_inches='tight')
    print("저장: result_1128/Figure_RegionRT.png")
    plt.close()

def main():
    """메인 분석 파이프라인"""
    print("="*80)
    print("수정된 분석 시작")
    print("="*80)

    # 데이터 로드
    data = load_data()
    spr_data = data['SPR_Data']
    manip_data = data['Manipulation_Check']
    recall_data = data['Recall_Data']

    # 1. 연습 문장 제거
    spr_clean = remove_practice_trials(spr_data)

    # 2. Trial-level outlier 제거
    spr_clean, outlier_criterion, lower_bound, upper_bound = identify_outlier_trials(
        spr_clean, method='iqr', k=2.5
    )

    # 3. 문장 구조 파싱
    print("\n문장 구조 파싱 중...")
    parsed_data = parse_sentence_structure(spr_clean)
    print(f"파싱된 관찰치: {len(parsed_data)}개")

    # 4. Word-level outlier 제거
    parsed_data = remove_word_outliers(parsed_data)

    # 5. 조작 검증 (단어별)
    word_summary = analyze_manipulation_check_by_word(manip_data)

    # 6. Power analysis
    power_results = power_analysis(observed_d=0.05)

    # 7. 회상 데이터 분석
    recall_results = analyze_recall_data(recall_data)

    # 8. 가설 검증
    modifier_data, critical_data, h1_desc, h2_desc = test_hypotheses(parsed_data)

    # 9. 시각화
    create_visualizations(parsed_data, modifier_data, critical_data, manip_data)

    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)

    # Return results for documentation
    return {
        'outlier_criterion': outlier_criterion,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'n_trials_after_outlier': len(spr_clean),
        'n_observations': len(parsed_data),
        'word_summary': word_summary,
        'power_results': power_results,
        'recall_results': recall_results,
        'h1_desc': h1_desc,
        'h2_desc': h2_desc
    }

if __name__ == "__main__":
    results = main()
