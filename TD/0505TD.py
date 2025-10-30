# alpha=0.5, gamma=0.5 のデータだけを全ファイルから抽出してまとめるスクリプト

import json
import os

participants = range(1, 25)  # No1〜No24
episodes = [1, 2, 3]         # ep1〜ep3

target_key = "alpha=0.5, gamma=0.5"
results = {}

for i in participants:
    for ep in episodes:
        path = f"data/raw/No{i}/ep{ep}_result/aveTD_error.json"

        if not os.path.exists(path):
            print(f"⚠️ {path} が見つかりません。スキップします。")
            continue

        with open(path, "r") as f:
            data = json.load(f)

        if target_key in data:
            results[f"No{i}_ep{ep}"] = data[target_key]
        else:
            print(f"⚠️ {path} に {target_key} がありません。")

# 抽出結果を保存
output_path = "data/raw/TD_error_alpha0.5_gamma0.5.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ 抽出完了！結果を {output_path} に保存しました。")
