#参加者ごとにまとめたデータを使って、3種類の散布図を作成・保存するスクリプト

import json
import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# --- グループ化後のファイル読み込み ---
with open("data/processed/grouped/stepTD_grouped_after.json", "r", encoding="utf-8") as f:
    stepTD_data = json.load(f)

with open("data/processed/grouped/blink_grouped_after.json", "r", encoding="utf-8") as f:
    blink_data = json.load(f)

with open("data/processed/grouped/choice_grouped_after.json", "r", encoding="utf-8") as f:
    choice_data = json.load(f)

# --- 保存フォルダ ---
save_dir = "figures/scatter_grouped_after"
os.makedirs(save_dir, exist_ok=True)

# --- 共通関数: 散布図を作成・保存 ---
def make_scatter(x, y, xlabel, ylabel, title, save_path):
    # データ長を揃える
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]

    # 相関係数
    try:
        r, p = pearsonr(x, y)
    except Exception as e:
        print(f"⚠️ {title}: 相関計算失敗 ({e})")
        return

    # 散布図
    plt.figure()
    plt.scatter(x, y, alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"{title}\n r={r:.2f}, p={p:.3f}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


# --- 参加者ごとに散布図作成 ---
for key in stepTD_data.keys():
    if key not in blink_data or key not in choice_data:
        print(f"⚠️ {key}: 一部データ欠損のためスキップ")
        continue

    x_stepTD = stepTD_data[key]
    y_blink = blink_data[key]
    y_choice = choice_data[key]

    # データがリストでない場合はスキップ
    if not (isinstance(x_stepTD, list) and isinstance(y_blink, list) and isinstance(y_choice, list)):
        print(f"⚠️ {key}: リスト形式でないためスキップ")
        continue

    # --- ① stepTD vs blink ---
    make_scatter(
        x_stepTD, y_blink,
        "stepTD", "blink",
        f"{key}: stepTD vs blink",
        os.path.join(save_dir, f"{key}_stepTD_vs_blink.png")
    )

    # --- ② stepTD vs choice ---
    make_scatter(
        x_stepTD, y_choice,
        "stepTD", "choice",
        f"{key}: stepTD vs choice",
        os.path.join(save_dir, f"{key}_stepTD_vs_choice.png")
    )

    # --- ③ blink vs choice ---
    make_scatter(
        y_blink, y_choice,
        "blink", "choice",
        f"{key}: blink vs choice",
        os.path.join(save_dir, f"{key}_blink_vs_choice.png")
    )

print("✅ 完了：3種類の散布図を全参加者分保存しました！")
