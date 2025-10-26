import matplotlib.pyplot as plt
import json

# --- データ読み込み ---
with open("data/raw/No7/ep1_result/choice_history.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)  # 主観評価（1～7程度）

data2 = [90, 8, 13, 11, 10, 10, 17, 10, 16, 61, 14, 9, 46, 9, 40, 7, 12, 9]  # 瞬き回数など

# --- 長さを揃える ---
min_len = min(len(data1), len(data2))
data1 = data1[:min_len]
data2 = data2[:min_len]
x = range(min_len)

# --- グラフ作成 ---
fig, ax1 = plt.subplots(figsize=(8, 5))

# 左軸：主観評価
ax1.plot(x, data1, color='tab:blue', marker='o', label='主観評価')
ax1.set_xlabel("trial")
ax1.set_ylabel("evaluation(1-7)", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 右軸：瞬き
ax2 = ax1.twinx()
ax2.plot(x, data2, color='tab:red', linestyle='--', marker='x', label='瞬き')
ax2.set_ylabel("gaze", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# --- タイトルと装飾 ---
plt.title("No7-1 Evaluation vs gaze")
fig.tight_layout()
plt.grid(True, axis='x')

plt.show()
