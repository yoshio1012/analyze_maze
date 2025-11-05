import json
import os

with open("data/raw/gaze_all.json", "r", encoding="utf-8") as gaze_all_file:
    gaze_all = json.load(gaze_all_file)

stepTD_dict_before = {}
stepTD_dict_after = {}

for key, blink_times in gaze_all.items():
    first = int(key[1:3])
    second = int(key[4])

    step_path = f"data/raw/No{first}/ep{second}_result/step.json"
    stepTD_path = f"data/raw/No{first}/ep{second}_result/stepTD_ave.json"

    with open(step_path, "r", encoding="utf-8") as time_file:
        step_data = json.load(time_file)

    with open(stepTD_path, "r", encoding="utf-8") as stepTD_file:
        stepTD_data = json.load(stepTD_file)
        stepTD_data = stepTD_data["alpha=0.5, gamma=0.5"]


    # --- 数値に変換（重要）---
    step_data = [int(x) for x in step_data]

    # 最初に main の値が 65 以下になる位置を探す
    split_index = None
    for i, value in enumerate(step_data):
        if value <= 65:
            split_index = i
            break

    if split_index is not None:
        stepTD_before = stepTD_data[:split_index]
        stepTD_after  = stepTD_data[split_index:]
    else:
        print("⚠️ None split index for", key)
        stepTD_before = None
        stepTD_after  = None
    
    stepTD_dict_before[key] = stepTD_before
    stepTD_dict_after[key] = stepTD_after   

#それぞれの辞書をonline_dataファイルに保存
os.makedirs("data/processed", exist_ok=True)
with open("data/processed/stepTD_dict_before.json", "w", encoding="utf-8") as f:
    json.dump(stepTD_dict_before, f, ensure_ascii=False, indent=4)

with open("data/processed/stepTD_dict_after.json", "w", encoding="utf-8") as f:
    json.dump(stepTD_dict_after, f, ensure_ascii=False, indent=4)


    
    
