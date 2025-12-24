import json

with open("data/processed/stepTD_dict_before.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)

with open("data/processed/stepTD_dict_after.json", "r", encoding="utf-8") as f:
    data2 = json.load(f)

merged = {k: (data1[k] or []) + (data2.get(k) or []) for k in data1}


with open("data/processed/TD.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)
