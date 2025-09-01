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
td_ep1 = load_td_errors("Ay1/y101_TD_trial.json", 0.1, 0.9)
td_ep2 = load_td_errors("Ay1/y102_TD_trial.json", 0.1, 0.9)
td_ep3 = load_td_errors("Ay1/y103_TD_trial.json", 0.1, 0.9)

ch_ep1 = load_choices("yobi1/ep1_result/choice_history.json")
ch_ep2 = load_choices("yobi1/ep2_result/choice_history.json")
ch_ep3 = load_choices("yobi1/ep3_result/choice_history.json")

# --- 長さを揃える ---
max_len = max(len(td_ep1), len(td_ep2), len(td_ep3),
              len(ch_ep1), len(ch_ep2), len(ch_ep3))

def pad_with_nan(data, length):
    return data + [np.nan]*(length - len(data))

td_ep1, td_ep2, td_ep3 = [pad_with_nan(d, max_len) for d in [td_ep1, td_ep2, td_ep3]]
ch_ep1, ch_ep2, ch_ep3 = [pad_with_nan(d, max_len) for d in [ch_ep1, ch_ep2, ch_ep3]]

# --- 散布図描画 ---
plt.figure(figsize=(8,6))
colors = ["blue", "orange", "green"]
labels = ["EP1", "EP2", "EP3"]

td_min, td_max = -200, 0  # TD誤差の範囲を限定

for td, ch, color, label in zip([td_ep1, td_ep2, td_ep3],
                                [ch_ep1, ch_ep2, ch_ep3],
                                colors, labels):
    mask = ~np.isnan(td) & ~np.isnan(ch)
    mask &= (np.array(td) >= td_min) & (np.array(td) <= td_max)
    td_clean = np.array(td)[mask]
    ch_clean = np.array(ch)[mask]

    plt.scatter(td_clean, ch_clean, c=color, alpha=0.6, label=label)

plt.xlabel("TD Error (restricted to -200 ~ 0)")
plt.ylabel("Choice (1–7)")
plt.title("TD Error vs Choice (α=0.1, γ=0.9, range -200~0)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
