#最初に迷路を選択する
#その後どの実験者のデータを使用するかを決める
#学習率と割引率の種類はファイルを複数個作成するのが良さそう
#実験画面と同様に色で分布がわかるといいかも
#主観評価のところにTD誤差が表示されればいい（割引率と学習率ごとに表示するのもいいかも）
#データとグラフは別で保存したい
#V(s_t)\leftarrow V(s_t)+\alpha[r_{t+1}+\gamma V(s_{t+1})-V(s_t)]put
import json
import os

MAZE = input("どの迷路か選択して下さい:P or 1 or 2 or 3")
if MAZE == "1":
    with open("maze_data\maze1.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 3
    goal_cols = 27

elif MAZE == "2":
    with open("maze_data\maze2.json", 'r') as f:
        maze_data = json.load(f)  
    goal_rows = 23
    goal_cols = 15

elif MAZE == "3":
    with open("maze_data\maze3.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 17
    goal_cols = 21

elif MAZE == "P":
    with open("maze_data\mazeP.json", 'r') as f:
        maze_data = json.load(f)
    goal_rows = 17
    goal_cols = 17

else:
    print("1, 2, 3のいずれかを入力して下さい")
    exit()

#実験者の選択
experiment = input("どの実験者のデータを使用しますか:P or 1 or 2 or 3 or 4 or 5・・・")
if experiment == "P":
    with open("action_data \ P \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ P \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ P \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "1":
    with open("action_data \ No1 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No1 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No1 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "2":
    with open("action_data \ No2 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No2 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No2 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "3":
    with open("action_data \ No3 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No3 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No3 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "4":
    with open("action_data \ No4 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No4 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No4 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "5":
    with open("action_data \ No5 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No5 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No5 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "6":
    with open("action_data \ No6 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No6 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No6 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "7":
    with open("action_data \ No7 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No7 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No7 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "8":
    with open("action_data \ No8 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No8 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No8 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "9":
    with open("action_data \ No9 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No9 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No9 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "10":
    with open("action_data \ No10 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No10 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No10 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "11":
    with open("action_data \ No11 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No11 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No11 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)

elif experiment == "12":
    with open("action_data \ No12 \ move_history.json", 'r') as f:
        move_data = json.load(f)

    with open("action_data \ No12 \ time_result.json", 'r') as f:
        time_data = json.load(f)

    with open("action_data \ No12 \ visited_history.json", 'r') as f:
        visited_data = json.load(f)
else:
    print("P, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12のいずれかを入力して下さい")
    exit()

#学習率と割引率の設定
alpha = [0.1, 0.5, 0.9]
gamma = [0.1, 0.5, 0.9]

#価値関数を入れるための迷路リストの作製
maze_rows = []
maze_all = []

Reward = 0.0
penalty = -1.0

for rows in maze_data:
    for grid in rows:
        if grid == 9:
            maze_rows.append(None)
        else:
            maze_rows.append(0.0)
    maze_all.append(maze_rows)
    maze_rows = []

#関数にする
def TD_maze(ALPHA, GAMMA):
    TDerror_history = []

    for i in range(len(move_data)):
        y = 1
        x = 1
        TDerror = []

        # 0=="UP", 1=="DOWN", 2=="LEFT", 3=="RIGHT"
        for j in range(len(move_data[i])):
            old_y = y
            old_x = x

            action = move_data[i][j]
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
        #"再度探索開始"

        return TDerror_history
    

All_TD = []
#alphaとgammaの組み合わせで実行
for Alp in alpha:
    for Gam in gamma:
        TDerror_history = TD_maze(Alp, Gam)
        All_TD.append(TDerror_history)
            
print(All_TD)