import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ===============================
# 妥協案：見た目調整
# ===============================
plt.rcParams.update({
    "font.size": 6,
    "axes.titlesize": 8,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "lines.linewidth": 0.9,
    "lines.markersize": 2,
})

# --- データ読み込み ---
eval_path = "data/raw/gaze_all.json"
with open(eval_path, "r", encoding="utf-8") as f:
    blink_data = json.load(f)

save_dir = "paper/subjective_evaluations"
os.makedirs(save_dir, exist_ok=True)

pdf_path_main = os.path.join(save_dir, "subjective_evaluations_5x2.pdf")
pdf_path_last = os.path.join(save_dir, "subjective_evaluations_last_1x2.pdf")

X_MAX = 55

# cm → inch
W_MAIN = 14 / 2.54
H_MAIN = 17.5 / 2.54
H_LAST = 3.5 / 2.54   # ★ 最後用

# ===============================
# メインPDF（5×2）
# ===============================
with PdfPages(pdf_path_main) as pdf:

    fig, axes = plt.subplots(5, 2, figsize=(W_MAIN, H_MAIN))
    axes = axes.flatten()
    idx = 0

    leftover_axes_data = []  # ★ 最後の2枚を一時保存

    for key, _ in blink_data.items():

        first = int(key[1:3])
        second = int(key[4])

        subj_path = f"data/raw/No{first}/ep{second}_result/choice_history.json"
        if not os.path.exists(subj_path):
            continue

        with open(subj_path, "r", encoding="utf-8") as f:
            subjective = json.load(f)

        if idx < 10:
            ax = axes[idx]
        else:
            # 念のため（今回は来ない想定）
            break

        x = range(1, len(subjective) + 1)
        ax.plot(x, subjective, marker='o')

        ax.set_xlim(0.5, X_MAX + 0.5)
        ax.set_ylim(0.5, 7.5)
        ax.set_xticks([1] + list(range(10, X_MAX + 1, 10)))
        ax.set_yticks(range(1, 8))
        ax.set_title(f"No{first}-ep{second}", pad=2)
        ax.grid(True, linestyle=':', linewidth=0.5)

        if idx // 2 == 4:
            ax.set_xlabel("Trial")
        if idx % 2 == 0:
            ax.set_ylabel("Evaluation")

        # ★ データを保存（最後用）
        leftover_axes_data.append((x, subjective, f"No{first}-ep{second}"))

        idx += 1

        if idx == 10:
            fig.tight_layout(pad=0.6)
            pdf.savefig(fig)
            plt.close(fig)

            fig, axes = plt.subplots(5, 2, figsize=(W_MAIN, H_MAIN))
            axes = axes.flatten()
            idx = 0
            leftover_axes_data = []

    # ここでは保存しない（最後の2枚は別PDF）
    plt.close(fig)

# ===============================
# 最後の2枚専用PDF（1×2）
# ===============================
if len(leftover_axes_data) == 2:

    with PdfPages(pdf_path_last) as pdf:

        fig, axes = plt.subplots(1, 2, figsize=(W_MAIN, H_LAST))

        for ax, (x, subjective, title) in zip(axes, leftover_axes_data):

            ax.plot(x, subjective, marker='o')
            ax.set_xlim(0.5, X_MAX + 0.5)
            ax.set_ylim(0.5, 7.5)
            ax.set_xticks([1] + list(range(10, X_MAX + 1, 10)))
            ax.set_yticks(range(1, 8))
            ax.set_title(title, pad=2)
            ax.grid(True, linestyle=':', linewidth=0.5)

        axes[0].set_ylabel("Evaluation")
        axes[0].set_xlabel("Trial")
        axes[1].set_xlabel("Trial")

        fig.tight_layout(pad=0.6)
        pdf.savefig(fig)
        plt.close(fig)

print("🎉 PDF作成完了")
print(f"・メイン : {pdf_path_main}")
print(f"・最後用 : {pdf_path_last}")
