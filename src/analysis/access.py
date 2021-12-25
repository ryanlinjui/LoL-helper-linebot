import pandas as pd
import os
from .get_data import(
    get_player_id,
    get_player_matches
)

database_dir = "./analysis/database/"
analysis_data_db_path = database_dir + "analysis_data.csv"
game_db_path = database_dir + "game.csv"
mode_db_path = database_dir + "mode.csv"
status_db_path = database_dir + "status.csv"
analysis_data_db = None
game_db = None
mode_db = None
status_db = None

def update_db():
    global analysis_data_db,game_db,mode_db,status_db
    if not(os.path.exists(analysis_data_db_path)):
        pd.DataFrame(columns=["player","mode","rate","most_used","rank_champion","game_time","kda","cspm","dpm","gpm"]).to_csv(analysis_data_db_path,index=False)
    if not(os.path.exists(game_db_path)):
        pd.DataFrame(columns=["player_id","battle_id","match_res","gamemode","gametip","start_time","character","K/D/A","money","CS","damage","view"]).to_csv(game_db_path,index=False)
    if not(os.path.exists(status_db_path)):
        pd.DataFrame(columns=["line_id","player_id"]).to_csv(status_db_path,index=False)
    analysis_data_db = pd.read_csv(analysis_data_db_path)
    game_db = pd.read_csv(game_db_path)
    mode_db = pd.read_csv(mode_db_path,dtype=str)
    status_db = pd.read_csv(status_db_path,dtype=str)

def login(line_user_id:str,lol_player_id:str)->bool:
    '''
    更新該line id目前所查詢的lol玩家，如status_db中未存在該line id，新增該line id
    如未存在該lol玩家，檢查是否存在此lol玩家，如果存在，利用爬蟲抓取資料新增至game_db並且呼叫analysis函數做分析新增至analysis_data_db，如果不存在該lol玩家，raise error
    '''
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    if not(line_user_id in status_db["line_id"].values): 
        #新增line id
        status_db = status_db.append({"line_id": line_user_id,"player_id":None},ignore_index=True)
        status_db.to_csv(status_db_path,index=False)
        print("["+line_user_id+"]: "+"Append new line id: "+line_user_id)
    
    if not(lol_player_id in game_db["player_id"].values):
        try:
            #新增lol玩家對戰資料至game_db並作分析後新增至analysis_data_db
            player_id  = get_player_id(lol_player_id)
            match_data = get_player_matches(player_id)
            game_db = game_db.append(match_data[0],ignore_index=True).to_csv(game_db_path,index=False)
            print("["+line_user_id+"]: "+"Append game data of "+lol_player_id)
        except IndexError:
            #不存在此lol玩家
            print("["+line_user_id+"]: "+lol_player_id+" is not exist")
            return False
    
    if not(lol_player_id in analysis_data_db["player"].values):
        analysis(lol_player_id)
        print("["+line_user_id+"]: "+"Append analysing data of "+lol_player_id)
    
    status_db.loc[status_db.line_id == line_user_id,"player_id"] = lol_player_id
    status_db.to_csv(status_db_path,index=False)
    print("["+line_user_id+"]: "+"Login with "+lol_player_id)
    return True

def is_login(line_user_id:str)->bool:
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    if not(line_user_id in list(status_db["line_id"].values)): #如果不存在該line id
        return False
    if status_db[(status_db["line_id"]==line_user_id)]["player_id"].isnull()[0]: #如果該line id的狀態為空白(未登入)
        return False
    return True
    
def logout(line_user_id:str)->bool:
    '''
    清空該line id目前所查詢的玩家，如該line id不存在，回傳False，反之True
    '''
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    if not(line_user_id in list(status_db["line_id"].values)): #如果不存在該line id
        return False
    status_db.loc[status_db.line_id == line_user_id,"player_id"] = None
    status_db.to_csv(status_db_path,index=False)
    print("["+line_user_id+"]: "+"Logout")
    return True

def get_player_data(line_user_id:str,game_mode:str)->dict:
    '''
    拿取analysis_data_db中玩家該遊戲模式的各項數據。(kda,cspm,dpm,gpm需轉換為百分比，該母群體為玩家中的最高數據)
    '''
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    game_mode = list(mode_db[(mode_db["code"]==game_mode)]["zh-tw"])[0]
    try:
        player_id = list(status_db[(status_db["line_id"]==line_user_id)]["player_id"])[0]
        data = analysis_data_db[(analysis_data_db["player"]==player_id)&(analysis_data_db["mode"]==game_mode)].iloc[-1].to_dict()
        kda_population = analysis_data_db[(analysis_data_db["mode"]==game_mode)]["kda"].max()
        cspm_population = analysis_data_db[(analysis_data_db["mode"]==game_mode)]["cspm"].max()
        dpm_population = analysis_data_db[(analysis_data_db["mode"]==game_mode)]["dpm"].max()
        gpm_population = analysis_data_db[(analysis_data_db["mode"]==game_mode)]["gpm"].max()
        if kda_population==0: kda_population = 1
        if cspm_population==0: cspm_population = 1
        if dpm_population==0: dpm_population = 1
        if gpm_population==0: gpm_population = 1
        data["kda"]  = data["kda"]/kda_population
        data["cspm"] = data["cspm"]/cspm_population
        data["dpm"]  = data["dpm"]/dpm_population
        data["gpm"]  = data["gpm"]/gpm_population
    except IndexError:
        data = {}
    print("["+line_user_id+"]: "+"Look for "+game_mode+" of "+player_id)
    return data

def analysis(player_name:str):
    '''
    將玩家的四個遊戲模式的各項數據存進analysis_data_db。如不存在某遊戲模式數據，則忽略
    '''
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    player_data = game_db[(game_db["player_id"]==player_name)].sort_values(by=["gamemode"])
    for mode in mode_db["zh-tw"]:
        data = player_data[(player_data["gamemode"]==mode)]
        if not(analysis_data_db[(analysis_data_db["player"]==player_name)&(analysis_data_db["mode"]==mode)].empty):
            continue
        if data.empty:
            continue
        print("Analysis mode "+mode +" of "+ player_name)
        total = data.shape[0]
        try:
            win = data["match_res"].value_counts()['勝']
        except KeyError:
            win = 0
        for i in range(5):
            try:
                playing_time = pd.to_numeric(data["gametip"].str[0:5-i]).sum() + (pd.to_numeric(data["gametip"].str[-3:-1]).sum())/60
                break
            except:
                continue
        damage = data["damage"].sum()
        kda = 0
        money = 0
        cs = 0
        for _ in data["K/D/A"]:
            kda_data = [int(i) for i in _.split("/")]
            if kda_data[1] == 0: kda_data[1] = 1
            kda += (kda_data[0]+kda_data[2])/kda_data[1]

        for _ in data["money"]:
            money +=  float(_.split("k")[0][1:])*1000

        for _ in data["CS"]:
            cs +=  float(_.split("(")[0])
        
        character_counter = data["character"].value_counts()
        most_used = []
        rank_champion = []
        for i in range(3):
            try:
                most_used.append(character_counter.keys()[i])
            except IndexError:
                pass
        character_rate = {}
        for _ in character_counter.keys():
            character_rate[_] =  data[(data["character"]==_)&(data["match_res"]=="勝")].shape[0] / data[(data["character"]==_)].shape[0]
        character_rate = sorted(character_rate.items(), key=lambda x:x[1], reverse=True)
        for i in range(3):
            try:
                rank_champion.append(character_rate[i][0])
            except IndexError:
                pass
        analysis_data_db = analysis_data_db.append({
        "player":player_name,
        "mode":mode,
        "rate":win/total,
        "most_used":most_used,
        "rank_champion":rank_champion,
        "game_time":playing_time/total,
        "kda":kda/total,
        "cspm":cs/playing_time,
        "dpm":damage/playing_time,
        "gpm":money/playing_time
        },ignore_index=True)
    analysis_data_db.to_csv(analysis_data_db_path,index=False)


'''
TESTING CODE
'''
# line_of_id = "22"
# playername = "特務小熊熊"
# print(is_login(line_of_id))
# print(login(line_of_id,playername))
# print(get_player_data(line_of_id,"一般對戰"))
# print(is_login(line_of_id))
# print(logout(line_of_id))