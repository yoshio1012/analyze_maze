import json
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# --- ① データ読み込み ---
td_path = "data/raw/gaze_all.json"
with open(td_path, "r", encoding="utf-8") as f:
    blink_data = json.load(f)

# --- ② 保存先フォルダ作成 ---
save_dir = "figures/blink_vs_evaluation_scatter"
os.makedirs(save_dir, exist_ok=True)

# --- ③ 各No×epごとに処理 ---
for key, Blink in blink_data.items():
    
    first = int(key[1:3])
    second = int(key[4])

    # 主観評価のパス
    subj_path = f"data/raw/No{first}/ep{second}_result/choice_history.json"
    if not os.path.exists(subj_path):
        print(f"⚠️ {first}{second} が見つかりません。スキップします。")
        continue

    # --- 主観評価の読み込み ---
    with open(subj_path, "r", encoding="utf-8") as f:
        subjective = json.load(f)

    # --- データ長の調整 ---
    min_len = min(len(subjective), len(Blink))
    subjective = subjective[:min_len]
    Blink = Blink[:min_len]

    # --- 散布図作成 ---
    plt.figure(figsize=(8,6))
    plt.scatter(subjective, Blink, color='tab:red', alpha=0.6, label='data')

    # --- 回帰線の計算 ---
    coef = np.polyfit(subjective, Blink, 1)  # 1次式でフィッティング
    poly1d_fn = np.poly1d(coef)
    x_line = np.array([min(subjective), max(subjective)])
    y_line = poly1d_fn(x_line)
    plt.plot(x_line, y_line, color='tab:blue', linestyle='--', label='regression line')

    # --- 相関係数 ---
    corr, p_value = pearsonr(subjective, Blink)
    plt.text(0.05, 0.95, f'r = {corr:.2f}', transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    # --- 軸・タイトル ---
    plt.xlabel("Evaluation (1–7)")
    plt.ylabel("Blink")
    plt.title(f"No{first}-ep{second}: Blink vs Evaluation")
    plt.grid(True, linestyle=':')
    plt.legend()

    # --- 保存 ---
    save_path = os.path.join(save_dir, f"No{first}_ep{second}_blink_scatter.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ {save_path} を保存しました。")

print("\n🎉 全24×3件の散布図＋回帰線作成が完了しました！")
