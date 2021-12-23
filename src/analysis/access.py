import pandas as pd
from get_data import(
    get_player_id,
    get_player_matches
)

database_dir = "database/"
analysis_data_db = pd.read_csv(database_dir+"analysis_data.csv")
game_db = pd.read_csv(database_dir+"game.csv")
mode_db = pd.read_csv(database_dir+"mode.csv")
status_db = pd.read_csv(database_dir+"status.csv")

def login(line_user_id:str,lol_player_id:str):
    '''
    更新該line id目前所查詢的玩家，如status_db中未存在該line id，新增該line id
    如未存在該玩家，檢查是否存在此玩家，如果存在，利用爬蟲抓取資料新增至game_db並且呼叫analysis函數做分析新增至analysis_data_db，如果不存在該玩家，raise error
    '''
    if not(line_user_id in status_db["line_id"]): 
        #新增line id
        pass
    try:
        player_id =  get_player_id(lol_player_id)
        match_data += get_player_matches(player_id)
    except IndexError:
        pass



    status_db[line_user_id] = lol_player_id
    status_db.to_csv("status.csv",index=False)

def is_login(line_user_id:str,lol_player_id:str):
    if line_user_id in status_db["line_id"]:
        return True
    return False
    
def logout(line_user_id:str)->bool:
    '''
    清空該line id目前所查詢的玩家，如該line id不存在，回傳False，反之True
    '''
    try:
        status_db[line_user_id] = ""
        status_db.to_csv("status.csv",index=False)
        return True
    except:
        return False

def get_player_data(line_user_id:str,game_mode:str)->list:
    '''
    拿取analysis_data_db中玩家該遊戲模式的各項數據。(kda,cspm,dpm,gpm需轉換為百分比，該母群體為玩家中的最高數據)
    '''
    pass

def analysis(player_name:str):
    '''
    將玩家的四個遊戲模式的各項數據存進analysis_data_db。如不存在某遊戲模式數據，做初始化
    '''
    player_data = game_db[(game_db["player_id"]==player_name)].sort_values(by=["gamemode"])
    for mode in mode_db["zh-tw"]:
        data = player_data[(player_data["gamemode"]==row)]
        if data.empty:
            continue
        total = data.shape[0]
        win = data["match_res"].value_counts()['勝']
        playing_time = pd.to_numeric(data["gametip"].str[0:2]).sum() + (pd.to_numeric(data["gametip"].str[-3:-1]).sum())/60
        kda = list(data["K/D/A"])
        money = 0
        damage = data["damage"].sum()
        print(damage)
        input()
        analysis_data_db.append(pd.DataFrame({
        "player":player_name,
        "mode":mode,
        "rate":win/total,
        "most_used":0,
        "rank_champion":0,
        "game_time":playing_time/total,
        "kda":sum(kda)/total,
        "cspm":cs/playing_time,
        "dpm":damage/playing_time,
        "gpm":money/playing_time
        })).to_csv("test.csv",index=False)

#analysis("特務小熊熊")
playername = "特務小熊熊"
print(get_player_matches(get_player_id(playername)))
