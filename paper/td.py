import json
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# ===============================
# 妥協案：見た目調整（共通）
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
    td_data = json.load(f)

# 保存先
save_dir = "paper/TD"
os.makedirs(save_dir, exist_ok=True)

pdf_path_main = os.path.join(save_dir, "TD_5x2.pdf")
pdf_path_last = os.path.join(save_dir, "TD_last_1x2.pdf")

# --- 軸固定 ---
X_MAX = 55
Y_MIN, Y_MAX = -30, 30

# cm → inch
W_MAIN = 14 / 2.54
H_MAIN = 17.5 / 2.54
H_LAST = 3.5 / 2.54

# ===============================
# メインPDF（5×2）
# ===============================
with PdfPages(pdf_path_main) as pdf:

    fig, axes = plt.subplots(5, 2, figsize=(W_MAIN, H_MAIN))
    axes = axes.flatten()

    idx = 0
    leftover_data = []

    for key, _ in td_data.items():

        first = int(key[1:3])
        second = int(key[4])

        subj_path = f"data/raw/No{first}/ep{second}_result/stepTD_ave.json"
        if not os.path.exists(subj_path):
            continue

        with open(subj_path, "r", encoding="utf-8") as f:
            td = json.load(f)
            td = td["alpha=0.5, gamma=0.5"]

        x = range(1, len(td) + 1)

        ax = axes[idx]
        ax.plot(x, td, marker='o')

        ax.set_xlim(0.5, X_MAX + 0.5)
        ax.set_xticks([1] + list(range(10, X_MAX + 1, 10)))

        ax.set_ylim(Y_MIN, Y_MAX)
        ax.set_yticks(np.arange(-30, 31, 10))

        ax.set_title(f"No{first}-ep{second}", pad=2)
        ax.grid(True, linestyle=':', linewidth=0.5)

        if idx // 2 == 4:
            ax.set_xlabel("Trial")
        if idx % 2 == 0:
            ax.set_ylabel("TD error")

        leftover_data.append((x, td, f"No{first}-ep{second}"))
        idx += 1

        if idx == 10:
            fig.tight_layout(pad=0.6)
            pdf.savefig(fig)
            plt.close(fig)

            fig, axes = plt.subplots(5, 2, figsize=(W_MAIN, H_MAIN))
            axes = axes.flatten()
            idx = 0
            leftover_data = []

    plt.close(fig)

# ===============================
# 最後の2枚専用PDF（1×2）
# ===============================
if len(leftover_data) == 2:

    with PdfPages(pdf_path_last) as pdf:

        fig, axes = plt.subplots(1, 2, figsize=(W_MAIN, H_LAST))

        for ax, (x, td, title) in zip(axes, leftover_data):
            ax.plot(x, td, marker='o')
            ax.set_xlim(0.5, X_MAX + 0.5)
            ax.set_xticks([1] + list(range(10, X_MAX + 1, 10)))
            ax.set_ylim(Y_MIN, Y_MAX)
            ax.set_yticks(np.arange(-30, 31, 10))
            ax.set_title(title, pad=2)
            ax.grid(True, linestyle=':', linewidth=0.5)

        axes[0].set_ylabel("TD error")
        axes[0].set_xlabel("Trial")
        axes[1].set_xlabel("Trial")

        fig.tight_layout(pad=0.6)
        pdf.savefig(fig)
        plt.close(fig)

print("🎉 TD error PDF 作成完了")
print(f"・メイン : {pdf_path_main}")
print(f"・最後用 : {pdf_path_last}")
