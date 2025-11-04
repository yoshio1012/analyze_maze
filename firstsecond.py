import json
import os

with open("data/raw/gaze_all.json", "r", encoding="utf-8") as gaze_all_file:
    gaze_all = json.load(gaze_all_file)

with open("data/raw/TD_error_alpha0.5_gamma0.5.json", "r", encoding="utf-8") as TD_file:
    TD_data = json.load(TD_file)

step_dict_before = {}
step_dict_after = {}    
blink_dict_before = {}
blink_dict_after = {}
TD_dict_before = {}
TD_dict_after = {}
choice_dict_before = {}
choice_dict_after = {}


for key, blink_times in gaze_all.items():
    first = int(key[1:3])
    second = int(key[4])

    step_path = f"data/raw/No{first}/ep{second}_result/step.json"
    blink_path = f"data/raw/No{first}/ep{second}_result/blinkstep.json"
    choice_path = f"data/raw/No{first}/ep{second}_result/choice_history.json"

    with open(step_path, "r", encoding="utf-8") as time_file:
        step_data = json.load(time_file)

    with open(blink_path, "r", encoding="utf-8") as blink_file:
        blink_data = json.load(blink_file)

    with open(choice_path, "r", encoding="utf-8") as choice_file:
        choice_data = json.load(choice_file)

    td_data= TD_data[f"No{first}_ep{second}"]

    # --- 数値に変換（重要）---
    step_data = [int(x) for x in step_data]

    # 最初に main の値が 65 以下になる位置を探す
    split_index = None
    for i, value in enumerate(step_data):
        if value <= 65:
            split_index = i
            break

    if split_index is not None:
        step_before = step_data[:split_index]
        step_after  = step_data[split_index:]
        blink_before = blink_data[:split_index]
        blink_after  = blink_data[split_index:]
        td_before = td_data[:split_index]
        td_after  = td_data[split_index:]
        choice_before = choice_data[:split_index]
        choice_after = choice_data[split_index:]
    else:
        print("⚠️ None split index for", key)
        step_before = None
        step_after  = None
        blink_before = None
        blink_after  = None
        td_before = None
        td_after  = None
        choice_before = None
        choice_after = None
    
    step_dict_before[key] = step_before
    step_dict_after[key] = step_after   
    blink_dict_before[key] = blink_before
    blink_dict_after[key] = blink_after
    TD_dict_before[key] = td_before
    TD_dict_after[key] = td_after
    choice_dict_before[key] = choice_before
    choice_dict_after[key] = choice_after

#それぞれの辞書をonline_dataファイルに保存
os.makedirs("data/processed", exist_ok=True)
with open("data/processed/step_dict_before.json", "w", encoding="utf-8") as f:
    json.dump(step_dict_before, f, ensure_ascii=False, indent=4)

with open("data/processed/step_dict_after.json", "w", encoding="utf-8") as f:
    json.dump(step_dict_after, f, ensure_ascii=False, indent=4)

with open("data/processed/blink_dict_before.json", "w", encoding="utf-8") as f:
    json.dump(blink_dict_before, f, ensure_ascii=False, indent=4)

with open("data/processed/blink_dict_after.json", "w", encoding="utf-8") as f:
    json.dump(blink_dict_after, f, ensure_ascii=False, indent=4)

with open("data/processed/TD_dict_before.json", "w", encoding="utf-8") as f:
    json.dump(TD_dict_before, f, ensure_ascii=False, indent=4)

with open("data/processed/TD_dict_after.json", "w", encoding="utf-8") as f:
    json.dump(TD_dict_after, f, ensure_ascii=False, indent=4)

with open("data/processed/choice_dict_before.json", "w", encoding="utf-8") as f:
    json.dump(choice_dict_before, f, ensure_ascii=False, indent=4)
    
with open("data/processed/choice_dict_after.json", "w", encoding="utf-8") as f:
    json.dump(choice_dict_after, f, ensure_ascii=False, indent=4)

    
    
