# TD2.py
import json
import os

with open("maze_data/maze2.json", 'r') as f:
    maze_data = json.load(f)  
goal_rows = 27
goal_cols = 3

#行動履歴データ
with open("data/raw/No24/ep2_result/move_history.json", 'r') as f:
    move_data = json.load(f)

with open("data/raw/No24/ep2_result/visited_history.json", 'r') as f:
    visited_data = json.load(f)

#TD学習のパラメータ
alpha = [0.1, 0.5, 0.9]
gamma = [0.1, 0.5, 0.9]
Reward = 0.0
penalty = -1.0

#価値関数を入れるための迷路リストの作製
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

#関数にする
def TD_maze(ALPHA, GAMMA):
    maze_all = init_value_maze()  # 
    TDerror_history = []

    for i in range(len(move_data)):
        y = 1
        x = 1
        TDerror = []

        # 0=="UP", 1=="DOWN", 2=="LEFT", 3=="RIGHT"
        for action in move_data[i]:
            old_y, old_x = y, x

            if action == 0:   y -= 1
            elif action == 1: y += 1
            elif action == 2: x -= 1
            elif action == 3: x += 1
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
    

All_TD = {}
for Alp in alpha:
    for Gam in gamma:
        TDerror_history = TD_maze(Alp, Gam)
        All_TD[f"alpha={Alp}, gamma={Gam}"] = TDerror_history


# ===== 保存 =====
with open("data/raw/No24/ep2_result/TD_error.json", "w") as f:
    json.dump(All_TD, f, indent=2)

print("TD誤差を TD_error_results.json に保存しました。")