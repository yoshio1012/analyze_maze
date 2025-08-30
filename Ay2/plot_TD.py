# TD誤差と選択肢履歴を同じグラフに描画するスクリプト

import json
import matplotlib.pyplot as plt

# --- TD誤差データの読み込み ---
with open("Ay2/y201_TD_trial.json", "r", encoding="utf-8") as f:
    td_data = json.load(f)

# --- choice_history の読み込み ---
with open("yobi2/ep1_result/choice_history.json", "r", encoding="utf-8") as f:
    choice_history = json.load(f)  # 例: [6,6,6,7,5,4,...]

# --- グラフ描画 ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# TD誤差を折れ線で描画
for label, values in td_data.items():
    ax1.plot(values, marker="o", label=f"TD Error {label}")
ax1.set_xlabel("Trial")
ax1.set_ylabel("TD Error")
ax1.grid(True)

# 2軸目を追加（選択肢履歴用）
ax2 = ax1.twinx()
ax2.plot(choice_history, marker="x", color="red", linestyle="--", label="Choice History")
ax2.set_ylabel("Choice (1-7)")
ax2.set_ylim(0.5, 7.5)  # 選択肢が1〜7なので範囲固定

# 凡例をまとめて表示
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="upper right")

plt.title("TD Error and Choice History")
plt.tight_layout()
plt.show()
