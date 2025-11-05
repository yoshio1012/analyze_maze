import json
import os

# 対象参加者と条件
participants = range(1, 25)  # No1～No24
episodes = range(1, 4)       # ep1～ep3

for pid in participants:
    for ep in episodes:
        stepTD_path = f"data/raw/No{pid}/ep{ep}_result/stepTD_error.json"
        save_path = f"data/raw/No{pid}/ep{ep}_result/stepTD_ave.json"

        if not os.path.exists(stepTD_path):
            print(f"⚠️ スキップ: {stepTD_path} が存在しません")
            continue

        # --- 読み込み ---
        with open(stepTD_path, "r", encoding="utf-8") as f:
            step_TD = json.load(f)

        trial_TD = {}

        # --- 各パラメータごとに試行単位へ集約 ---
        for params, trials in step_TD.items():
            trial_results = []
            for td_list in trials:
                if len(td_list) > 0:
                    trial_results.append(sum(td_list)/len(td_list))  # 合計
                else:
                    trial_results.append(0.0)
            trial_TD[params] = trial_results

        # --- 保存 ---
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(trial_TD, f, indent=2, ensure_ascii=False)

        print(f"✅ 保存完了: {save_path}")

print("\n🎉 全24人×3条件の処理が完了しました。")
