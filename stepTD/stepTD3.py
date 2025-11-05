import json
import os

# --- ① 迷路データの読み込み ---
with open("maze_data/maze3.json", 'r', encoding="utf-8") as f:
    maze_data = json.load(f)

goal_rows = 17
goal_cols = 21

# --- ② TD学習のパラメータ ---
alpha = 0.5
gamma = 0.5
penalty = -1.0


# --- ③ 価値関数を入れるための迷路リスト初期化関数 ---
def init_value_maze():
    maze_all = []
    for rows in maze_data:
        maze_row = []
        for grid in rows:
            if grid == 9:
                maze_row.append(None)
            else:
                maze_row.append(0.0)
        maze_all.append(maze_row)
    return maze_all


# --- ④ TD誤差計算関数 ---
def TD_maze(move_data, step_data, ALPHA, GAMMA):
    maze_all = init_value_maze()
    TDerror_history = []
    Reward = step_data[0]

    for i in range(len(move_data)):
        y, x = 1, 1
        TDerror = []

        # 0=="UP", 1=="DOWN", 2=="LEFT", 3=="RIGHT"
        for action in move_data[i]:
            old_y, old_x = y, x

            if action == 0:
                y -= 1
            elif action == 1:
                y += 1
            elif action == 2:
                x -= 1
            elif action == 3:
                x += 1
            else:
                print("actionの値が不正です")
                exit()

            is_goal = (y == goal_rows and x == goal_cols)
            R = Reward if is_goal else penalty

            td = R + GAMMA * maze_all[y][x] - maze_all[old_y][old_x]
            maze_all[old_y][old_x] += ALPHA * td
            TDerror.append(td)

        TDerror_history.append(TDerror)

    return TDerror_history


# --- ⑤ 全被験者ループ ---
for i in range(1, 25):
    participant = f"No{i}"
    base_dir = f"data/raw/{participant}/ep3_result"

    move_path = os.path.join(base_dir, "move_history.json")
    visited_path = os.path.join(base_dir, "visited_history.json")
    step_path = os.path.join(base_dir, "step.json")
    save_path = os.path.join(base_dir, "stepTD_error.json")

    # ファイルが存在しない場合はスキップ
    if not all(os.path.exists(p) for p in [move_path, step_path]):
        print(f"{participant} のデータが見つかりません。スキップします。")
        continue

    # --- データ読み込み ---
    with open(move_path, "r", encoding="utf-8") as f:
        move_data = json.load(f)
    with open(step_path, "r", encoding="utf-8") as f:
        step_data = json.load(f)

    # --- TD誤差計算 ---
    TDerror_history = TD_maze(move_data, step_data, alpha, gamma)
    All_TD = {f"alpha={alpha}, gamma={gamma}": TDerror_history}

    # --- 結果保存 ---
    os.makedirs(base_dir, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(All_TD, f, indent=2)

    print(f"{participant} のTD誤差を保存しました。")

print("✅ 全参加者（No1〜No24）のTD誤差計算が完了しました。")
