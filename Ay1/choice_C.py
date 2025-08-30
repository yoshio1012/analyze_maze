import json
import matplotlib.pyplot as plt

# --- choice_history 読み込み ---
def load_choices(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)  # 例: [6,6,6,7,...]

# --- データ読み込み ---
ch_101 = load_choices("yobi1/ep1_result/choice_history.json")
ch_102 = load_choices("yobi1/ep2_result/choice_history.json")
ch_103 = load_choices("yobi1/ep3_result/choice_history.json")

# --- グラフ描画 ---
plt.figure(figsize=(12,5))

# trial数を揃える
n = min(len(ch_101), len(ch_102), len(ch_103))

plt.plot(ch_101[:n], marker="o", label="EP1 Choice")
plt.plot(ch_102[:n], marker="s", label="EP2 Choice")
plt.plot(ch_103[:n], marker="^", label="EP3 Choice")

plt.xlabel("Trial")
plt.ylabel("Choice")
plt.title("Comparison of Choices Across Episodes")
plt.ylim(0.5, 7.5)  # 選択肢が1〜7の場合
plt.legend()
plt.grid(True)
plt.show()
