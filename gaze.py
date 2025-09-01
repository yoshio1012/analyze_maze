import pandas as pd
import json

# --- TSV読み込み ---
df = pd.read_csv("data/raw/yobi101.tsv", sep="\t")
df["ts"] = df["Eyetracker timestamp"].astype(float)  # µs 


# --- 数値型に変換 ---
df["Pupil diameter left"] = pd.to_numeric(df["Pupil diameter left"], errors="coerce")
df["Pupil diameter right"] = pd.to_numeric(df["Pupil diameter right"], errors="coerce")

# --- 瞬き候補 ---
blink_mask = (
    df["Pupil diameter left"].isna() &
    df["Pupil diameter right"].isna()
)

#true/False を 1/0 に変換して新しい列を追加
df["blink"] = blink_mask.astype(int)

# --- time_result.json読み込み（Trialを生成） ---
with open("yobi1/ep1_result/time_result.json", "r", encoding="utf-8") as f:
    trials = json.load(f)  # [[start, end, duration], ...]

Trial = []
for i in range(len(trials)):
    Duration_us = trials[i][2] * 1000000  # 秒 → µs に変換
    Trial.append(("duration", Duration_us))
    if i < len(trials) - 1:
        interval_us = (trials[i+1][0] - trials[i][1])*1000000  # 秒 → µs に変換
        Trial.append(("interval", interval_us))

# --- 瞬き数カウント ---
def count_blinks_from_event(Trial):
    results = []

    # --- ScreenRecordingStart の基準時刻 ---
    event_idx = df.index[df["Event"] == "ScreenRecordingStart"][0]  # イベント行のインデックス
    start_event_ts = df.loc[event_idx + 1, "ts"]  # 次の行のタイムスタンプを取る

    current_time = start_event_ts  # 今の基準時刻（ms）

    for kind, length in Trial:
        start = current_time
        end = start + length
        current_time = end

        if kind == "duration":
            trial_data = df[(df["ts"] >= start) & (df["ts"] <= end)]

            blinks = []
            in_blink = False
            blink_start = None

            for t, b in zip(trial_data["ts"].values, trial_data["blink"].values):
                if b == 1 and not in_blink:
                    in_blink = True
                    blink_start = t
                elif b == 0 and in_blink:
                    in_blink = False
                    blink_end = t
                    if 500_000 >= (blink_end - blink_start) >= 50_000:
                        blinks.append((blink_start, blink_end))

            results.append(len(blinks))

    return results

# --- 実行 ---
blinks_per_duration = count_blinks_from_event(Trial)
print(blinks_per_duration)
