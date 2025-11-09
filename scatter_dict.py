import json
import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# --- ファイル読み込み ---
with open("data/processed/stepTD_dict_after.json", "r", encoding="utf-8") as f:
    data_before = json.load(f)

with open("data/processed/blink_dict_after.json", "r", encoding="utf-8") as f:
    data_after = json.load(f)

# --- 保存フォルダ ---
save_dir = "figures/scatter_stepTDVSblink_after"
os.makedirs(save_dir, exist_ok=True)

# --- 共通のキーで処理 ---
for key in data_before.keys():
    if key not in data_after:
        continue  # 片方にしかないデータはスキップ

    x = data_before[key]
    y = data_after[key]

    # Noneや空リストをスキップ
    if x is None or y is None:
        print(f"⚠️ {key}: Noneを含むためスキップ")
        continue
    if not isinstance(x, list) or not isinstance(y, list):
        print(f"⚠️ {key}: リストではないためスキップ")
        continue
    if len(x) < 2 or len(y) < 2:
        print(f"⚠️ {key}: データ数が少ないためスキップ")
        continue

    # データ長を合わせる
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]

    # 相関係数計算
    try:
        r, p = pearsonr(x, y)
    except Exception as e:
        print(f"⚠️ {key}: 相関係数の計算に失敗 ({e})")
        continue

    # 散布図作成
    plt.figure()
    plt.scatter(x, y)
    plt.title(f"{key}\n r={r:.2f}, p={p:.3f}")
    plt.xlabel("stepTD")
    plt.ylabel("blink")
    plt.grid(True)

    # 保存
    save_path = os.path.join(save_dir, f"{key}.png")
    plt.savefig(save_path)
    plt.close()

print("✅ 完了：全参加者の散布図を保存しました！")
