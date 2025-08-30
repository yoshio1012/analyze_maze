import json
import numpy as np
import matplotlib.pyplot as plt

# --- データ読み込み ---
def load_td_errors(path, alpha=0.1, gamma=0.9):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    label = f"alpha={alpha}, gamma={gamma}"
    return data.get(label, [])

def load_choices(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- データ読み込み ---
td_ep1 = load_td_errors("Ay2/y201_TD_trial.json", 0.1, 0.9)
td_ep2 = load_td_errors("Ay2/y202_TD_trial.json", 0.1, 0.9)
td_ep3 = load_td_errors("Ay2/y203_TD_trial.json", 0.1, 0.9)

ch_ep1 = load_choices("yobi2/ep1_result/choice_history.json")
ch_ep2 = load_choices("yobi2/ep2_result/choice_history.json")
ch_ep3 = load_choices("yobi2/ep3_result/choice_history.json")

# --- 長さを揃える ---
max_len = max(len(td_ep1), len(td_ep2), len(td_ep3),
              len(ch_ep1), len(ch_ep2), len(ch_ep3))

def pad_with_nan(data, length):
    return data + [np.nan]*(length - len(data))

td_ep1, td_ep2, td_ep3 = [pad_with_nan(d, max_len) for d in [td_ep1, td_ep2, td_ep3]]
ch_ep1, ch_ep2, ch_ep3 = [pad_with_nan(d, max_len) for d in [ch_ep1, ch_ep2, ch_ep3]]

# --- グラフ描画 ---
fig, ax1 = plt.subplots(figsize=(12,6))
ax2 = ax1.twinx()

colors = ["blue", "orange", "green"]

# TD誤差（左軸）
ax1.plot(td_ep1, color=colors[0], marker="o", label="EP1 TD")
ax1.plot(td_ep2, color=colors[1], marker="s", label="EP2 TD")
ax1.plot(td_ep3, color=colors[2], marker="^", label="EP3 TD")
ax1.set_xlabel("Trial")
ax1.set_ylabel("TD Error")
ax1.grid(True)

# choice（右軸）
ax2.plot(ch_ep1, color=colors[0], marker="x", linestyle="--", label="EP1 Choice")
ax2.plot(ch_ep2, color=colors[1], marker="x", linestyle="--", label="EP2 Choice")
ax2.plot(ch_ep3, color=colors[2], marker="x", linestyle="--", label="EP3 Choice")
ax2.set_ylabel("Choice (1-7)")
ax2.set_ylim(0.5, 7.5)

# 凡例をまとめる
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.title("TD Error and Choice History (α=0.1, γ=0.9)")
plt.tight_layout()
plt.show()
