import json
import numpy as np
import matplotlib.pyplot as plt

# --- データの読み込み ---
def load_td_errors(path, alpha=0.1, gamma=0.9):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    label = f"alpha={alpha}, gamma={gamma}"
    return data.get(label, [])

# --- データ読み込み ---
td_ep1 = load_td_errors("Ay1/y101_TD_trial.json", 0.1, 0.9)
td_ep2 = load_td_errors("Ay1/y102_TD_trial.json", 0.1, 0.9)
td_ep3 = load_td_errors("Ay1/y103_TD_trial.json", 0.1, 0.9)

# --- 長さを揃えるため NaN で補完 ---
max_len = max(len(td_ep1), len(td_ep2), len(td_ep3))

def pad_with_nan(data, length):
    return data + [np.nan]*(length - len(data))

td_ep1_padded = pad_with_nan(td_ep1, max_len)
td_ep2_padded = pad_with_nan(td_ep2, max_len)
td_ep3_padded = pad_with_nan(td_ep3, max_len)

# --- グラフ描画 ---
plt.figure(figsize=(12,6))

plt.plot(td_ep1_padded, marker="o", label="EP1 (α=0.1, γ=0.9)")
plt.plot(td_ep2_padded, marker="s", label="EP2 (α=0.1, γ=0.9)")
plt.plot(td_ep3_padded, marker="^", label="EP3 (α=0.1, γ=0.9)")

plt.xlabel("Trial")
plt.ylabel("TD Error")
plt.title("Comparison of TD Errors (α=0.1, γ=0.9, Original Trial Lengths)")
plt.legend()
plt.grid(True)
plt.show()
