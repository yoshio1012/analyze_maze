import json
import os
import matplotlib.pyplot as plt

# --- データ読み込み ---
with open("data/processed/blink_dict_before.json", "r", encoding="utf-8") as f:
    choice_dict_before = json.load(f)
with open("data/processed/blink_dict_after.json", "r", encoding="utf-8") as f:
    choice_dict_after = json.load(f)

with open("data/processed/TD_dict_before.json", "r", encoding="utf-8") as f:
    blink_dict_before = json.load(f)
with open("data/processed/TD_dict_after.json", "r", encoding="utf-8") as f:
    blink_dict_after = json.load(f)


# --- 保存フォルダ作成 ---
save_dir = "figures/blink_TD_scatter_compare"
os.makedirs(save_dir, exist_ok=True)

for key in choice_dict_before.keys():
    cb = choice_dict_before[key]
    ca = choice_dict_after[key]
    bb = blink_dict_before[key]
    ba = blink_dict_after[key]

    if cb is None or ca is None or bb is None or ba is None:
        print(f"⚠️ Skip {key} (missing data)")
        continue

    plt.figure(figsize=(6, 6))
    plt.scatter(cb, bb, color="skyblue", label="Before", alpha=0.7)
    plt.scatter(ca, ba, color="salmon", label="After", alpha=0.7)
    plt.title(f"{key} - blink vs TD (Before/After)")
    plt.xlabel("blink")
    plt.ylabel("TD")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(save_dir, f"{key}.png")
    plt.savefig(save_path)
    plt.close()

print("✅ 散布図を全参加者分保存しました！")
