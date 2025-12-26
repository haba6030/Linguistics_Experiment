import pandas as pd

# 파일 이름은 필요에 맞게 수정 가능
MASTER_CSV = "MasterSPR.csv"

# 1. 마스터 파일 읽기
df = pd.read_csv(MASTER_CSV)

# 2. 필러 vs 실험 자극 구분
#   - base 가 NA 이거나
#   - plausibility 가 "P_filler" 인 경우를 필러로 정의
is_filler = (
    df["base"].astype(str).str.upper().eq("NA")
    | df["plausibility"].astype(str).eq("P_filler")
)

filler_df = df[is_filler].copy()
exp_df = df[~is_filler].copy()

# version이 숫자형이 아닌 경우 대비
exp_df["version"] = exp_df["version"].astype(int)

# 3. condition 순서 정의: HP, HI, NP, NI
#   (emotion, plausibility) 튜플 순서
cond_order = [
    ("H", "P"),  # index 0
    ("H", "I"),  # index 1
    ("N", "P"),  # index 2
    ("N", "I"),  # index 3
]

# 4. 리스트별 version 패턴 정의
#    각 base에 대해 cond_order 순서에 맞춰 version 선택
version_patterns = {
    1: [1, 1, 1, 1],  # List1: 전부 v1
    2: [2, 2, 2, 2],  # List2: 전부 v2
    3: [1, 2, 1, 2],  # List3: HP1, HI2, NP1, NI2
    4: [2, 1, 2, 1],  # List4: HP2, HI1, NP2, NI1
}

# 5. (base, emotion, plausibility) → {version: row} 매핑 만들기
mapping = {}

for (base, emo, plaus), group in exp_df.groupby(["base", "emotion", "plausibility"]):
    # group 안에는 version 1,2 가 한 개씩 있을 것으로 기대
    inner = {}
    for _, row in group.iterrows():
        v = int(row["version"])
        inner[v] = row
    mapping[(base, emo, plaus)] = inner

# 6. 리스트별로 데이터프레임 생성
bases = sorted(exp_df["base"].unique())

for list_id, vpattern in version_patterns.items():
    rows = []

    # 각 base마다 cond_order 순서대로 하나씩 뽑기
    for base in bases:
        for cond_idx, (emo, plaus) in enumerate(cond_order):
            key = (base, emo, plaus)
            if key not in mapping:
                raise ValueError(f"Missing condition for base={base}, emotion={emo}, plaus={plaus}")
            # cond_idx에 해당하는 버전 선택
            v = vpattern[cond_idx]
            if v not in mapping[key]:
                raise ValueError(f"Missing version {v} for base={base}, emotion={emo}, plaus={plaus}")
            row = mapping[key][v]
            rows.append(row.to_dict())

    # 실험 자극 데이터프레임
    list_exp_df = pd.DataFrame(rows)

    # 필러 추가 (모든 리스트에 동일한 필러 사용)
    list_filler_df = filler_df.copy()

    # 리스트 ID와 필러 플래그 추가
    list_exp_df["list_id"] = list_id
    list_exp_df["is_filler"] = 0

    list_filler_df["list_id"] = list_id
    list_filler_df["is_filler"] = 1

    # 컬럼 순서 정리 (원하는 대로 수정 가능)
    cols_order = [
        "list_id",
        "item_id",
        "base",
        "emotion",
        "plausibility",
        "version",
        "stimulus_text",
        "is_filler",
    ]

    list_df = pd.concat([list_exp_df, list_filler_df], ignore_index=True)
    # 혹시 마스터에 없는 컬럼이 있으면 예외 처리 없이 그냥 패스되도록
    list_df = list_df[[c for c in cols_order if c in list_df.columns]]

    # 7. CSV로 저장
    out_name = f"List{list_id}.csv"
    list_df.to_csv(out_name, index=False, encoding="utf-8-sig")
    print(f"Saved {out_name} with {len(list_df)} rows.")