import pandas as pd
import os
import logging
from .get_data import(
    get_player_id,
    get_player_matches
)

database_dir = "./analysis/database/"
analysis_data_db_path = database_dir + "analysis_data.csv"
game_db_path = database_dir + "game.csv"
mode_db_path = database_dir + "mode.csv"
status_db_path = database_dir + "status.csv"
champion_db_path = database_dir + "champion.csv"
analysis_data_db = None
game_db = None
mode_db = None
status_db = None
champion_db = None

def update_db():
    global analysis_data_db,game_db,mode_db,status_db,champion_db
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
    champion_db = pd.read_csv(champion_db_path,dtype=str)

def get_player_total_num()->int:
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    return len(list(analysis_data_db.loc[:,'player'].value_counts()))

def get_user_status(line_user_id:str)->str:
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    if not(line_user_id in list(status_db["line_id"].values)):
        raise KeyError(f"{line_user_id} is not exist in database")
    return list(status_db[(status_db["line_id"]==line_user_id)]["player_id"])[0]

def get_mode_zh_tw(mode)->str:
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    if not(mode in list(mode_db["code"].values)):
        raise KeyError(f"{mode} is not exist in database")
    return list(mode_db[(mode_db["code"]==mode)]["zh-tw"])[0]

def get_player_data(line_user_id:str,game_mode:str)->dict:
    '''
    拿取analysis_data_db中玩家該遊戲模式的各項數據。(kda,cspm,dpm,gpm需轉換為百分比，該母群體為玩家中的最高數據)
    '''
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    try:
        game_mode = list(mode_db[(mode_db["code"]==game_mode)]["zh-tw"])[0]
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
    except:
        logging.info(f"[{line_user_id}]: There is no any match data of {game_mode} of {player_id} ")
        data = {}
    return data

def login(line_user_id:str,lol_player_id:str)->bool:
    '''
    更新該line id目前所查詢的lol玩家，如status_db中未存在該line id，新增該line id
    如未存在該lol玩家，檢查是否存在此lol玩家，如果存在，利用爬蟲抓取資料新增至game_db並且呼叫analysis函數做分析新增至analysis_data_db，如果不存在該lol玩家，raise error
    '''
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    if not(line_user_id in status_db["line_id"].values): 
        #新增line id
        status_db = status_db.append({"line_id": line_user_id,"player_id":None},ignore_index=True)
        status_db.to_csv(status_db_path,index=False)
        logging.info(f"[{line_user_id}]: Append new line id: {line_user_id}")
    
    if not(lol_player_id in game_db["player_id"].values):
        try:
            #新增lol玩家對戰資料至game_db並作分析後新增至analysis_data_db
            logging.info(f"[{line_user_id}]: Append game data of {lol_player_id}")
            player_id  = get_player_id(lol_player_id)
            match_data = get_player_matches(player_id)
            if len(match_data)==0:
                logging.info(f"[{line_user_id}]: There is no any match data of {lol_player_id}")
                return False
            game_db = game_db.append(match_data,ignore_index=True).to_csv(game_db_path,index=False)
        except IndexError:
            #不存在此lol玩家
            logging.info(f"[{line_user_id}]: {lol_player_id} is not exist")
            return False
    
    if not(lol_player_id in analysis_data_db["player"].values):
        analysis(lol_player_id)
        logging.info(f"[{line_user_id}]: Append analysing data of {lol_player_id}")
    
    status_db.loc[status_db.line_id == line_user_id,"player_id"] = lol_player_id
    status_db.to_csv(status_db_path,index=False)
    return True

def is_login(line_user_id:str)->bool:
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    if not(line_user_id in list(status_db["line_id"].values)): #如果不存在該line id
        return False
    return not(list(status_db[(status_db["line_id"]==line_user_id)]["player_id"])[0]=="%") #如果該line id的狀態為空白(未登入)
    
def logout(line_user_id:str):
    '''
    清空該line id目前所查詢的玩家，如該line id不存在，回傳False，反之True
    '''
    global analysis_data_db,game_db,mode_db,status_db
    update_db()
    if not(line_user_id in list(status_db["line_id"].values)): #如果不存在該line id
        raise Exception(f"Line ID: {line_user_id} is not exist")
    status_db.loc[status_db.line_id == line_user_id,"player_id"] = "%"
    status_db.to_csv(status_db_path,index=False)

def analysis(player_name:str):
    '''
    將玩家的四個遊戲模式的各項數據存進analysis_data_db。如不存在某遊戲模式數據，則忽略
    '''
    global analysis_data_db,game_db,mode_db,status_db,champion_db
    update_db()
    player_data = game_db[(game_db["player_id"]==player_name)].sort_values(by=["gamemode"])
    for mode in mode_db["zh-tw"]:
        data = player_data[(player_data["gamemode"]==mode)]
        if not(analysis_data_db[(analysis_data_db["player"]==player_name)&(analysis_data_db["mode"]==mode)].empty):
            continue
        if data.empty:
            continue
        logging.info(f"Analysis mode {mode} of {player_name}")
        total = data.shape[0]
        try:
            win = data["match_res"].value_counts()['勝']
        except KeyError:
            win = 0
        
        playing_time = 0
        for _ in data["gametip"]:
            playing_time_data = [int(i) for i in _.split(":")]
            playing_time += playing_time_data[0]+playing_time_data[1]/60
        
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
                most_used.append(list(champion_db[(champion_db["eng"]==character_counter.keys()[i])]["zh-tw"])[0])
            except IndexError:
                pass
        character_rate = {}
        for _ in character_counter.keys():
            character_rate[_] =  data[(data["character"]==_)&(data["match_res"]=="勝")].shape[0] / data[(data["character"]==_)].shape[0]
        character_rate = sorted(character_rate.items(), key=lambda x:x[1], reverse=True)
        for i in range(3):
            try:
                rank_champion.append(list(champion_db[(champion_db["eng"]==character_rate[i][0])]["zh-tw"])[0])
            except IndexError:
                pass
        analysis_data_db = analysis_data_db.append({
        "player":player_name,
        "mode":mode,
        "rate":win/total,
        "most_used":'%'.join(most_used),
        "rank_champion":'%'.join(rank_champion),
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