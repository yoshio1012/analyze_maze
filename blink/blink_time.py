import json
import os

with open("data/raw/gaze_all.json", "r", encoding="utf-8") as gaze_all_file:
    gaze_all = json.load(gaze_all_file)


for key, blink_times in gaze_all.items():
    first = int(key[1:3])
    second = int(key[4])

    time_path = f"data/raw/No{first}/ep{second}_result/step.json"
    with open(time_path, "r", encoding="utf-8") as time_file:
        step_data = json.load(time_file)

    step_results = step_data["alpha=0.1, gamma=0.1"]
    step_time=[a/b for a,b in zip(blink_times, step_results)]

    with open(time_path, "w", encoding="utf-8") as time_file:
        #step_timeをtime_pathに新たにjson形式で保存
        json.dump(step_time, time_file, ensure_ascii=False, indent=4)

    
