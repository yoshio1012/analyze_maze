import pandas as pd
import json

# --- TSV読み込み ---
df = pd.read_csv("data/raw/yobi101.tsv", sep="\t")
df["ts"] = df["Computer timestamp"].astype(float)  # ミリ秒

# --- 瞬き候補 ---
blink_mask = (
    df["Pupil diameter left"].isna() |
    df["Pupil diameter right"].isna() |
    (df["Pupil diameter left"] < 0.5) |
    (df["Pupil diameter right"] < 0.5)
)

#true/False を 1/0 に変換して新しい列を追加
df["blink"] = blink_mask.astype(int)

# --- time_result.json読み込み（Trialを生成） ---
with open("yobi1/ep1_result/time_result.json", "r", encoding="utf-8") as f:
    trials = json.load(f)  # [[start, end, duration], ...]

Trial = []
for i in range(len(trials)):
    Trial.append(("duration", trials[i][2]))
    if i < len(trials) - 1:
        interval = trials[i+1][0] - trials[i][1]
        Trial.append(("interval", interval))

# --- 瞬き数カウント ---
def count_blinks_from_event(Trial, min_duration_ms=500):
    results = []

    # ScreenRecordingStart の基準時刻
    start_event_ts = df[df["Event"] == "ScreenRecordingStart"]["ts"].values[0]

    current_time = start_event_ts  # 今の基準時刻（ms）

    for kind, length in Trial:
        start = current_time
        end = start + length*1000  # JSONは秒単位 → ms に変換
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
                    if (blink_end - blink_start) >= min_duration_ms:
                        blinks.append((blink_start, blink_end))

            results.append(len(blinks))

    return results

# --- 実行 ---
blinks_per_duration = count_blinks_from_event(Trial)
print(blinks_per_duration)
