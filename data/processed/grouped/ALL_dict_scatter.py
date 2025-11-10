import json
import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# --- ファイル読み込み ---
with open("data/processed/grouped/all_participants_merged_after.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stepTD = data["stepTD"]
blink = data["blink"]
choice = data["choice"]

# --- 保存フォルダ ---
save_dir = "figures/scatter_all_participants"
os.makedirs(save_dir, exist_ok=True)

# --- 散布図作成関数 ---
def make_scatter(x, y, xlabel, ylabel, filename):
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]

    # 相関係数
    try:
        r, p = pearsonr(x, y)
    except Exception as e:
        print(f"⚠️ 相関計算エラー: {xlabel} vs {ylabel} ({e})")
        return

    # 散布図
    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, alpha=0.6)
    plt.title(f"{xlabel} vs {ylabel}\n r={r:.2f}, p={p:.3f}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path)
    plt.close()
    print(f"✅ {filename} を保存しました")

# --- 3種類の散布図を作成 ---
make_scatter(stepTD, blink, "stepTD", "blink", "stepTD_vs_blink.png")
make_scatter(stepTD, choice, "stepTD", "choice", "stepTD_vs_choice.png")
make_scatter(blink, choice, "blink", "choice", "blink_vs_choice.png")

print("✅ 完了：全参加者まとめの散布図3種類を作成しました！")
