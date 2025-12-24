#参加者ごとのデータをまとめるスクリプト

import json
import os
from collections import defaultdict

# --- ファイル読み込み ---
with open("data/processed/TD.json", "r", encoding="utf-8") as f:
    stepTD_data = json.load(f)

with open("data/processed/blink.json", "r", encoding="utf-8") as f:
    blink_data = json.load(f)

with open("data/processed/choice.json", "r", encoding="utf-8") as f:
    choice_data = json.load(f)

# --- 参加者ごとにまとめる関数 ---
def group_by_participant(data_dict):
    grouped = defaultdict(list)
    for key, values in data_dict.items():
        if not isinstance(values, list):
            continue
        # 例: "p0103" → "p01"
        base_key = key[:3]  # "p01"
        grouped[base_key].extend(values)
    return dict(grouped)

# --- グルーピング ---
stepTD_grouped = group_by_participant(stepTD_data)
blink_grouped = group_by_participant(blink_data)
choice_grouped = group_by_participant(choice_data)

# --- 保存フォルダ ---
save_dir = "data/processed/grouped"
os.makedirs(save_dir, exist_ok=True)

# --- JSON出力 ---
with open(os.path.join(save_dir, "TD_grouped.json"), "w", encoding="utf-8") as f:
    json.dump(stepTD_grouped, f, ensure_ascii=False, indent=2)

with open(os.path.join(save_dir, "blink_grouped.json"), "w", encoding="utf-8") as f:
    json.dump(blink_grouped, f, ensure_ascii=False, indent=2)

with open(os.path.join(save_dir, "choice_grouped.json"), "w", encoding="utf-8") as f:
    json.dump(choice_grouped, f, ensure_ascii=False, indent=2)

print("✅ 完了：p0101~p0103 を p01 のようにまとめたJSONを保存しました！")
