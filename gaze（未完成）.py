import pandas as pd
import json

# --- TSVデータ読み込み ---
df = pd.read_csv("data/raw/yobi101.tsv", sep="\t")
df["ts"] = df["Computer timestamp"].astype(float)  # ミリ秒

# --- 瞳孔径のみで瞬き候補 ---
# NaN または 0.5未満を瞬き候補
blink_mask = (
    df["Pupil diameter left"].isna() |
    df["Pupil diameter right"].isna() |
    (df["Pupil diameter left"] < 0.5) |
    (df["Pupil diameter right"] < 0.5)
)

#true/False を 1/0 に変換して新しい列を追加
df["blink"] = blink_mask.astype(int)

# --- time_result.json読み込み ---
with open("time_result.json", "r", encoding="utf-8") as f:
    trials = json.load(f)  # [[start_time, end_time, duration], ...]

# --- ScreenRecordingStart を基準にして count_blinks を呼ぶ ---
def count_blinks_from_event_duration(trials,min_duration_ms=500):
    blinks_per_trial = []

    # ScreenRecordingStart の ts を取得
    event_starts = df[df["Event"] == "ScreenRecordingStart"]["ts"].values

    #iは試行番号、start_origはjsonのstart_time、durationはjsonのduration
    for i, (start_orig, _, duration) in enumerate(trials):
        # TSV 内の ScreenRecordingStart に対応する start_ms
        if i < len(event_starts):
            start_ms = event_starts[i]
        else:
            start_ms = start_orig * 1000  # 保険で json の start_time を使う

        end_ms = start_ms + duration * 1000  # duration 秒分

        d = df[(df["ts"] >= start_ms) & (df["ts"] < end_ms)].copy()
        if d.empty:
            blinks_per_trial.append(0)
            continue

        # 連続欠損区間を検出
        changes = d["blink"].diff().fillna(0)
        starts = d.index[changes == 1]
        ends   = d.index[changes == -1]

        if len(ends) < len(starts):
            ends = ends.append(pd.Index([d.index[-1]]))

        blinks = 0
        for s, e in zip(starts, ends):
            duration_ms = d.loc[e, "ts"] - d.loc[s, "ts"]
            if duration_ms >= min_duration_ms:
                blinks += 1

        blinks_per_trial.append(blinks)

    return blinks_per_trial

# --- 実行 ---
blink_counts = count_blinks_from_event_duration(trials)
print("各試行の瞬き回数:", blink_counts)

