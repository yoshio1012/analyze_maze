# TD誤差を試行ごとに集約して保存するスクリプト（No1〜No24、ep1〜ep3対応）

import json
import os

# 対象の被験者番号とエピソード
participants = range(1, 25)  # No1〜No24
episodes = [1, 2, 3]         # ep1〜ep3

for i in participants:
    for ep in episodes:
        input_path = f"data/raw/No{i}/ep{ep}_result/TD_error.json"
        output_path = f"data/raw/No{i}/ep{ep}_result/aveTD_error.json"

        # ファイルが存在しない場合スキップ
        if not os.path.exists(input_path):
            print(f"⚠️ {input_path} が見つかりません。スキップします。")
            continue

        # TD誤差を読み込み
        with open(input_path, "r") as f:
            step_TD = json.load(f)

        trial_TD = {}

        # 各パラメータごとに試行単位へ集約
        for params, trials in step_TD.items():
            trial_results = []
            for td_list in trials:
                if len(td_list) > 0:
                    trial_results.append(sum(td_list) / len(td_list))  # 試行内の平均
                else:
                    trial_results.append(0.0)
            trial_TD[params] = trial_results

        # 保存
        with open(output_path, "w") as f:
            json.dump(trial_TD, f, indent=2)

        print(f"✅ No{i} ep{ep}: 試行ごとにまとめた結果を {output_path} に保存しました。")

print("\n🎉 全ての被験者・エピソードの処理が完了しました！")
