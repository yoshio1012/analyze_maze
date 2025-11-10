import json
import os
from collections import defaultdict

# --- ファイル読み込み ---
base_dir = "data/processed/grouped"
with open(os.path.join(base_dir, "stepTD_grouped_after.json"), "r", encoding="utf-8") as f:
    stepTD_data = json.load(f)

with open(os.path.join(base_dir, "blink_grouped_after.json"), "r", encoding="utf-8") as f:
    blink_data = json.load(f)

with open(os.path.join(base_dir, "choice_grouped_after.json"), "r", encoding="utf-8") as f:
    choice_data = json.load(f)

# --- すべての参加者をまとめる ---
def merge_all(data_dict):
    merged = []
    for key, values in data_dict.items():
        if isinstance(values, list):
            merged.extend(values)
    return merged

stepTD_all = merge_all(stepTD_data)
blink_all = merge_all(blink_data)
choice_all = merge_all(choice_data)

# --- 統合したデータを1つの辞書にまとめる ---
merged_dict = {
    "stepTD": stepTD_all,
    "blink": blink_all,
    "choice": choice_all
}

# --- 保存 ---
save_path = "data/processed/grouped/all_participants_merged_after.json"
with open(save_path, "w", encoding="utf-8") as f:
    json.dump(merged_dict, f, ensure_ascii=False, indent=2)

print("✅ 完了：全参加者（p01〜p24）を1つのデータに統合しました！")
