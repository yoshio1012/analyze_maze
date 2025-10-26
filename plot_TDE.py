import matplotlib.pyplot as plt
import json

# --- データ読み込み ---
# 主観評価（1〜7程度）
with open("data/raw/No6/ep1_result/choice_history.json", "r", encoding="utf-8") as f:
    subjective = json.load(f)

# TD誤差（辞書形式）
with open("data/raw/No6/ep1_result/RETD_error.json", "r", encoding="utf-8") as f:
    td_error_dict = json.load(f)

# --- x軸（試行番号） ---
# 主観評価とTD誤差の長さを合わせる
first_td = next(iter(td_error_dict.values()))
min_len = min(len(subjective), len(first_td))
x = range(min_len)
subjective = subjective[:min_len]

# --- グラフ作成 ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# 左軸：主観評価
ax1.plot(x, subjective, color='tab:blue', marker='o', label='evaluation')
ax1.set_xlabel("trial")
ax1.set_ylabel("evaluation(1-7)", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 右軸：TD誤差（各条件）
ax2 = ax1.twinx()
colors = plt.cm.tab10.colors  # カラーマップから10色
for i, (key, values) in enumerate(td_error_dict.items()):
    ax2.plot(x, values[:min_len], linestyle='--', marker='', color=colors[i % 10], label=f"TD({key})")

ax2.set_ylabel("TD", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# --- タイトル・凡例・装飾 ---
plt.title("No6-1 evaluation vs TD ", fontsize=13)
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize=9)
plt.grid(True, axis='x', linestyle=':')
fig.tight_layout()

plt.show()
