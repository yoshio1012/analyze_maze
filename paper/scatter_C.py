import json
from scipy.stats import pearsonr

with open("data/processed/grouped/TD_grouped.json", encoding="utf-8") as f:
    stepTD = json.load(f)

with open("data/processed/grouped/blink_grouped.json", encoding="utf-8") as f:
    blink = json.load(f)

with open("data/processed/grouped/choice_grouped.json", encoding="utf-8") as f:
    choice = json.load(f)

# -----------------------------
# 相関とp値を participant ごとに計算
# -----------------------------
def calc_participant_correlation(dict_x, dict_y):
    result = {}

    for p_id in dict_x.keys():
        if p_id not in dict_y:
            continue

        x = dict_x[p_id]
        y = dict_y[p_id]

        # 長さチェック
        if not isinstance(x, list) or not isinstance(y, list):
            continue
        if len(x) < 2 or len(y) < 2 or len(x) != len(y):
            continue

        r, p = pearsonr(x, y)
        result[p_id] = [round(r, 2), round(p, 3)]

    return result

Blink_Evaluation_correlation = calc_participant_correlation(blink, choice)

TDerror_Blink_correlation = calc_participant_correlation(stepTD, blink)

TDerror_Evaluation_correlation = calc_participant_correlation(stepTD, choice)

print("Blink × Evaluation")
print(Blink_Evaluation_correlation)

print("\nTDerror × Blink")
print(TDerror_Blink_correlation)

print("\nTDerror × Evaluation")
print(TDerror_Evaluation_correlation)
