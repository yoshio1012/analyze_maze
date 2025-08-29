import pandas as pd
import json

# --- 1. データ読み込み ---
# TSV (瞳孔径データ)
df = pd.read_csv("yobi101.tsv", sep="\t", usecols=[
    "Eyetracker timestamp", 
    "Pupil diameter left", "Pupil diameter right","event"
])

# JSON (試行ごとの開始・終了)
with open("time_result.json", "r") as f:
    trials = json.load(f)

# --- 2. 瞬き判定列（両目とも NaN のとき True） ---
#isna() は pandas のメソッドで、「そのセルが 欠損値 (NaN: Not a Number) かどうか」を判定して True/False を返します
df["blink"] = df["Pupil diameter left"].isna() & df["Pupil diameter right"].isna()

# --- 3. ScreenRecordingStart のインデックス番号取得 ---
starts_idx = df.index[df["event"] == "ScreenRecordingStart"].tolist()

# --- 4. 試行ごとの瞬き回数 ---
results = []
for i, idx in enumerate(starts_idx):
    trial_start_ts = df.loc[idx, "Eyetracker timestamp"]
    duration_ms = trials[i][2] * 1000  # JSON の duration を ms に変換
    trial_end_ts = trial_start_ts + duration_ms

    # 試行区間抽出
    mask = (df["Eyetracker timestamp"] >= trial_start_ts) & (df["Eyetracker timestamp"] < trial_end_ts)
    sub = df.loc[mask, ["Eyetracker timestamp", "blink"]].reset_index(drop=True)

    # --- 瞬きカウント（500ms以上） ---
    blink_count = 0
    in_blink = False
    blink_start = None

    for idx2, row in sub.iterrows():
        if row["blink"] and not in_blink:
            in_blink = True
            blink_start = row["Eyetracker timestamp"]
        elif not row["blink"] and in_blink:
            blink_end = sub.loc[idx2-1, "Eyetracker timestamp"]
            if (blink_end - blink_start) >= 500:
                blink_count += 1
            in_blink = False

    # 最後まで瞬き中で終わる場合
    if in_blink:
        blink_end = sub.iloc[-1]["Eyetracker timestamp"]
        if (blink_end - blink_start) >= 500:
            blink_count += 1

    # 次の試行開始までのインターバル
    if i+1 < len(starts_idx):
        next_start_ts = df.loc[starts_idx[i+1], "Eyetracker timestamp"]
        interval_ms = next_start_ts - trial_end_ts
    else:
        interval_ms = None

    results.append([i+1, trial_start_ts, trial_end_ts, duration_ms, blink_count, interval_ms])

# --- 4. DataFrame化 & 保存 ---
df_blinks = pd.DataFrame(
    results, 
    columns=["trial", "trial_start_ts", "trial_end_ts", "duration_ms", "blink_count", "interval_ms"]
)
df_blinks.to_csv("trial_blink_counts.csv", index=False)

print(df_blinks.head())