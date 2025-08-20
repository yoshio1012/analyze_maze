#最初に迷路を選択する
#その後どの実験者のデータを使用するかを決める
#学習率と割引率の種類はファイルを複数個作成するのが良さそう
#実験画面と同様に色で分布がわかるといいかも
#主観評価のところにTD誤差が表示されればいい（割引率と学習率ごとに表示するのもいいかも）
#データとグラフは別で保存したい
#V(s_t)\leftarrow V(s_t)+\alpha[r_{t+1}+\gamma V(s_{t+1})-V(s_t)]put
import json
import os

#迷路の選択
MAZE = input("どの迷路か選択して下さい:P or 1 or 2 or 3")
if MAZE == "1":
    with open("maze_data/maze1.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 3
    goal_cols = 27

elif MAZE == "2":
    with open("maze_data/maze2.json", 'r') as f:
        maze_data = json.load(f)  
    goal_rows = 23
    goal_cols = 15

elif MAZE == "3":
    with open("maze_data/maze3.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 17
    goal_cols = 21

elif MAZE == "P":
    with open("maze_data/mazeP.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 17
    goal_cols = 17

else:
    print("1, 2, 3のいずれかを入力して下さい")
    exit()

#行動履歴データ
with open("action_data/P/move_history.json", 'r') as f:
    move_data = json.load(f)

with open("action_data/P/visited_history.json", 'r') as f:
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
with open("TD_error_results.json", "w") as f:
    json.dump(All_TD, f, indent=2)

print("TD誤差を TD_error_results.json に保存しました。")