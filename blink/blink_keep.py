# --- gaze_data.py の変数を読み込む ---
from gaze_data import *

# --- 参加者とエピソードを定義 ---
participants = range(1, 25)
episodes = [1, 2, 3]

# --- 例：全データをまとめて処理する ---
results = {}

for i in participants:
    for ep in episodes:
        key = f"p{i:02d}{ep:02d}"  # 例: p0101, p0203 の形
        try:
            data = globals()[key]  # 変数名を文字列から取得
            results[key] = data
        except KeyError:
            print(f"⚠️ {key} が見つかりません。")

# --- 結果を確認 ---
print(f"読み込んだデータ数: {len(results)}")
print(results["p0101"][:10])  # 一部を確認

# --- 必要ならJSONに保存 ---
import json, os
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/gaze_all.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n✅ すべての gaze_data をまとめて保存しました！")
