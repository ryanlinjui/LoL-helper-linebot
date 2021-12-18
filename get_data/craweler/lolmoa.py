import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lol.moa.tw"

def get_player_id(player_name:str)->int:
    '''
    the initialization of queries on a player, return player id as result
    
    Parameter player_name: the name of player
    '''
    with requests.get(f"{BASE_URL}/searchlogs/querySummoner", params={"sn":player_name}) as resp:
        if resp.status_code != 200:
            raise Exception(f"query return code with {resp.status_code}")
        res = BeautifulSoup(resp.text, features="html.parser")
        return str(res.find_all('a', href='#tabs-recentgames')[0]["data-url"]).split("/")[3]

def get_player_matches(player_id:str, page_count:int=2)->list:
    data_list = []
    
    for i in range(1, page_count+1):
        with requests.post(f"{BASE_URL}/Ajax/recentgames/{player_id}/page:{i}/sort:GameMatch.createDate/direction:desc") as resp:
            res = BeautifulSoup(resp.text, features="html.parser")
            pdata = res.find_all('tr', ["game-win", "game-lose", "game-leave", "info", "danger"])
            if pdata is None:
                raise ValueError("can not find player match data")
            if len(pdata) % 2 != 0:
                raise ValueError("record format error")
            
            for i in range(len(pdata)//2):
                data_fields = {
                    "player_id":None,

                    "battle_id":None,
                    "match_res":None,
                    "gamemode":None,
                    "gametip":None,
                    "start_time":None,

                    "character":None,
                    "K/D/A":None,
                    "money":None,
                    "CS":None,        #TODO: make a better translation
                    "damage":None,
                    "view":None       #TODO: make a better translation
                }
                # game-win / game-lose
                spans = pdata[i*2].th.find_all('span')
                data_fields["battle_id"] = int(spans[0].string)
                data_fields["match_res"] =     spans[1].string
                data_fields["gamemode"]  =     spans[3].string
                data_fields["gametip"]   =     spans[4].string
                data_fields["start_time"]=     spans[6].string
                
                # if gamemode is custom gamemode, directly discard it
                if data_fields["gamemode"] == "queueId2000":
                    continue
                
                # info / danger
                tds = pdata[i*2+1].find_all('td')
                data_fields["character"] = tds[0].div["data-code"]
                data_fields["K/D/A"]     = '/'.join([ it["data-val"] for it in tds[1].find_all('span')])
                data_fields["money"]     = tds[4].string
                data_fields["CS"]        = tds[5].string
                data_fields["damage"]    = tds[6].string
                data_fields["view"]      = tds[7].string

                data_fields["player_id"] = player_id
                data_list.append(data_fields)
    return data_list