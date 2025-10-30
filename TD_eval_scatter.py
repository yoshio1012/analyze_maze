import json
import os
import matplotlib.pyplot as plt
import numpy as np

# --- ① TD誤差の全データを読み込み ---
td_path = "data/raw/TD_error_alpha0.5_gamma0.5.json"
with open(td_path, "r", encoding="utf-8") as f:
    td_data = json.load(f)

# --- ② 保存先フォルダを作成 ---
save_dir = "figures/TD_vs_evaluation_scatter"
os.makedirs(save_dir, exist_ok=True)

# --- ③ 各No×epごとに処理 ---
for key, td_values in td_data.items():
    # key = "No6_ep1" のような形式
    parts = key.split("_")
    no = parts[0]   # No6
    ep = parts[1]   # ep1

    # 主観評価のパス
    subj_path = f"data/raw/{no}/{ep}_result/choice_history.json"
    if not os.path.exists(subj_path):
        print(f"⚠️ {subj_path} が見つかりません。スキップします。")
        continue

    # --- 主観評価の読み込み ---
    with open(subj_path, "r", encoding="utf-8") as f:
        subjective = json.load(f)

    # --- データ長の調整 ---
    min_len = min(len(subjective), len(td_values))
    subjective = subjective[:min_len]
    td_values = td_values[:min_len]

    # --- 散布図作成 ---
    plt.figure(figsize=(8,6))
    plt.scatter(subjective, td_values, color='tab:red', alpha=0.6, label='data')

    # --- 回帰線の追加 ---
    coef = np.polyfit(subjective, td_values, 1)
    poly1d_fn = np.poly1d(coef)
    x_line = np.array([min(subjective), max(subjective)])
    y_line = poly1d_fn(x_line)
    plt.plot(x_line, y_line, color='tab:blue', linestyle='--', label='regression line')

    # --- 相関係数 ---
    corr = np.corrcoef(subjective, td_values)[0, 1]
    plt.text(0.05, 0.95, f'r = {corr:.2f}', transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    # --- 軸・タイトル ---
    plt.xlabel("Evaluation (1–7)")
    plt.ylabel("TD error")
    plt.title(f"{no}-{ep}: TD error vs Evaluation (α=0.5, γ=0.5)")
    plt.grid(True, linestyle=':')
    plt.legend()

    # --- 保存 ---
    save_path = os.path.join(save_dir, f"{no}_{ep}_TD_vs_eval_scatter.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ {save_path} を保存しました。")

print("\n🎉 全24×3件の散布図＋回帰線作成が完了しました！")
