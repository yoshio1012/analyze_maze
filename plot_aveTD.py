import json
import os
import matplotlib.pyplot as plt

# --- ① TD誤差（alpha=0.5, gamma=0.5）の全データを読み込み ---
td_path = "data/raw/TD_error_alpha0.5_gamma0.5.json"
with open(td_path, "r", encoding="utf-8") as f:
    td_data = json.load(f)

# --- ② 保存先フォルダを作成 ---
save_dir = "figures/TD_vs_evaluation"
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
    x = range(min_len)
    subjective = subjective[:min_len]
    td_values = td_values[:min_len]

    # --- グラフ作成 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 主観評価（左軸）
    ax1.plot(x, subjective, color='tab:blue', marker='o', label='evaluation')
    ax1.set_xlabel("trial")
    ax1.set_ylabel("evaluation (1–7)", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # TD誤差（右軸）
    ax2 = ax1.twinx()
    ax2.plot(x, td_values, color='tab:red', linestyle='--', label='TD error')
    ax2.set_ylabel("TD error", color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # --- タイトル・凡例 ---
    plt.title(f"{no}-{ep}: Evaluation vs TD error (α=0.5, γ=0.5)", fontsize=13)
    fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize=9)
    plt.grid(True, axis='x', linestyle=':')
    fig.tight_layout()

    # --- 保存 ---
    save_path = os.path.join(save_dir, f"{no}_{ep}_TD_vs_eval.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ {save_path} を保存しました。")

print("\n🎉 全24×3件のグラフ作成が完了しました！")
