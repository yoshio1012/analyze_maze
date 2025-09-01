import pandas as pd

# --- TSV 読み込み ---
df = pd.read_csv("data/raw/yobi101.tsv", sep="\t")
df.columns = df.columns.str.strip()

# --- 開始: ScreenRecordingStart の最初の行 ---
start_rows = df.loc[df["Event"] == "ScreenRecordingStart"].index
if len(start_rows) > 0:
    start_idx = start_rows[0] - 1  
    ts_start = df.loc[start_idx, "Eyetracker timestamp"]
else:
    ts_start = df["Eyetracker timestamp"].iloc[0]

# --- 終了: RecordingEnd の前の行を参照 ---
stop_rows = df.loc[df["Event"] == "RecordingEnd"].index
if len(stop_rows) > 0:
    stop_idx = stop_rows[0] - 1  # 1つ前の行
    ts_stop = df.loc[stop_idx, "Eyetracker timestamp"]
else:
    ts_stop = df["Eyetracker timestamp"].iloc[-1]

# --- µs → 秒に変換 ---
print(ts_start, ts_stop)
duration_sec = (ts_stop - ts_start) / 1e6

print("=== Eyetracker timestamp ===")
print(f"Start: {ts_start}")
print(f"Stop : {ts_stop}")
print(f"Duration: {duration_sec:.2f} 秒 ({duration_sec/60:.2f} 分)")
