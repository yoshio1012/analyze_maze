#TD誤差を試行ごとに集約して保存するスクリプト

import json

# すでに保存したTD誤差を読み込む
with open("Ay2/y202_TD_error.json", "r") as f:
    step_TD = json.load(f)

trial_TD = {}

# 各パラメータごとに試行単位へ集約
for params, trials in step_TD.items():
    trial_results = []
    for td_list in trials:
        if len(td_list) > 0:
            trial_results.append(sum(td_list))  # 合計
        else:
            trial_results.append(0.0)
    trial_TD[params] = trial_results

# 保存
with open("Ay2/y202_TD_trial.json", "w") as f:
    json.dump(trial_TD, f, indent=2)

print("試行ごとにまとめた結果を y202_TD_trial.json に保存しました。")
