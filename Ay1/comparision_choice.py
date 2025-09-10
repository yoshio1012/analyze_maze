import json
import numpy as np
import matplotlib.pyplot as plt

# --- choice_history 読み込み ---
def load_choices(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)  # 例: [6,6,6,7,...]

# --- データ読み込み ---
ch_101 = load_choices("yobi1/ep1_result/choice_history.json")
ch_102 = load_choices("yobi1/ep2_result/choice_history.json")
ch_103 = load_choices("yobi1/ep3_result/choice_history.json")

# --- 長さを揃えるため NaN で補完 ---
max_len = max(len(ch_101), len(ch_102), len(ch_103))

def pad_with_nan(data, length):
    return data + [np.nan]*(length - len(data))

ch_101_padded = pad_with_nan(ch_101, max_len)
ch_102_padded = pad_with_nan(ch_102, max_len)
ch_103_padded = pad_with_nan(ch_103, max_len)

# --- グラフ描画 ---
plt.figure(figsize=(12,5))

plt.plot(ch_101_padded, marker="o", label="EP1 Choice")
plt.plot(ch_102_padded, marker="s", label="EP2 Choice")
plt.plot(ch_103_padded, marker="^", label="EP3 Choice")

plt.xlabel("Trial")
plt.ylabel("Choice")
plt.title("Comparison of Choices Across Episodes (Original Trial Lengths)")
plt.ylim(0.5, 7.5)  # 選択肢が1〜7の場合
plt.legend()
plt.grid(True)
plt.show()
