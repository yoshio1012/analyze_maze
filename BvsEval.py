import json
import os
import matplotlib.pyplot as plt

# --- ① TD誤差（alpha=0.5, gamma=0.5）の全データを読み込み ---
td_path = "data/raw/gaze_all.json"
with open(td_path, "r", encoding="utf-8") as f:
    blink_data = json.load(f)

# --- ② 保存先フォルダを作成 ---
save_dir = "figures/blink_vs_evaluation"
os.makedirs(save_dir, exist_ok=True)

# --- ③ 各No×epごとに処理 ---
for key, Blink in blink_data.items():
    
    first=int(key[1:3])
    second=int(key[4])

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
    x = range(min_len)
    subjective = subjective[:min_len]
    Blink = Blink[:min_len]

    # --- グラフ作成 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 主観評価（左軸）
    ax1.plot(x, subjective, color='tab:blue', marker='o', label='evaluation')
    ax1.set_xlabel("trial")
    ax1.set_ylabel("evaluation (1–7)", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # TD誤差（右軸）
    ax2 = ax1.twinx()
    ax2.plot(x, Blink, color='tab:red', linestyle='--', label='blink')
    ax2.set_ylabel("Blink", color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # --- タイトル・凡例 ---
    plt.title(f"No{first}-ep{second}: Evaluation vs blink", fontsize=13)
    fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize=9)
    plt.grid(True, axis='x', linestyle=':')
    fig.tight_layout()

    # --- 保存 ---
    save_path = os.path.join(save_dir, f"No{first}_ep{second}_blink_vs_eval.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ {save_path} を保存しました。")

print("\n🎉 全24×3件のグラフ作成が完了しました！")
