import json
import matplotlib.pyplot as plt

# --- データの読み込み ---
def load_td_errors(path, alpha=0.1, gamma=0.9):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    label = f"alpha={alpha}, gamma={gamma}"
    return data.get(label, [])

# --- データ読み込み ---
td_ep1 = load_td_errors("yobi1/ep1_result/y101_TD_trial.json", 0.1, 0.9)
td_ep2 = load_td_errors("yobi1/ep2_result/y102_TD_trial.json", 0.1, 0.9)
td_ep3 = load_td_errors("yobi1/ep3_result/y103_TD_trial.json", 0.1, 0.9)

# --- グラフ描画 ---
plt.figure(figsize=(10,6))

n = min(len(td_ep1), len(td_ep2), len(td_ep3))  # 長さを揃える
plt.plot(td_ep1[:n], marker="o", label="EP1 (α=0.1, γ=0.9)")
plt.plot(td_ep2[:n], marker="s", label="EP2 (α=0.1, γ=0.9)")
plt.plot(td_ep3[:n], marker="^", label="EP3 (α=0.1, γ=0.9)")

plt.xlabel("Trial")
plt.ylabel("TD Error")
plt.title("Comparison of TD Errors (alpha=0.1, gamma=0.9)")
plt.legend()
plt.grid(True)
plt.show()
