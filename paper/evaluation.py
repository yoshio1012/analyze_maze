import json
import os
import matplotlib.pyplot as plt

# --- 主観評価のみを描画 ---
eval_path = "data/raw/gaze_all.json"
with open(eval_path, "r", encoding="utf-8") as f:
    blink_data = json.load(f)

# 保存先
save_dir = "subjective_evaluations/figures"
os.makedirs(save_dir, exist_ok=True)

# ★ 論文用に軸を固定（ここが重要）
X_MAX = 50          # trial 数の最大（実データに合わせて調整）
Y_MIN, Y_MAX = 1, 7

for key, _ in blink_data.items():

    first = int(key[1:3])
    second = int(key[4])

    subj_path = f"data/raw/No{first}/ep{second}_result/choice_history.json"
    if not os.path.exists(subj_path):
        print(f"⚠️ {first}{second} が見つかりません。スキップします。")
        continue

    with open(subj_path, "r", encoding="utf-8") as f:
        subjective = json.load(f)

    # x を 1 始まりに
    x = range(1, len(subjective) + 1)


    # --- 図作成 ---
    fig, ax = plt.subplots(figsize=(7, 3.5))  # 論文向けサイズ

    ax.plot(x, subjective, marker='o', linewidth=1.5)

    # 軸ラベル
    ax.set_xlabel("Trial")
    ax.set_ylabel("subjective_evaluation (1–7)")

    # ★ 軸範囲・目盛を統一
    ax.set_xlim(0.5, X_MAX + 0.5)

    xticks = [1] + list(range(10, X_MAX + 1, 10))
    ax.set_xticks(xticks)


    ax.set_ylim(0.5, 7.5)
    ax.set_yticks(range(1, 8))

    # 装飾（控えめ）
    ax.grid(True, linestyle=':', linewidth=0.8)
    ax.set_title(f"No{first}-ep{second}")

    fig.tight_layout()

    save_path = os.path.join(save_dir, f"No{first}_ep{second}_evaluation.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ {save_path} を保存しました。")

print("\n🎉 主観評価のみのグラフ作成が完了しました！")
