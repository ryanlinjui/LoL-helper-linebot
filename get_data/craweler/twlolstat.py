import requests
from bs4 import BeautifulSoup
from pprint import pprint
BASE_URL = "https://twlolstats.com"

def get_player_id(player_name:str)->str:
    '''
    the initialization of queries on a player, return player id as result
    
    Parameter player_name: the name of player
    '''
    with requests.get(f"{BASE_URL}/summoner/", params={"summoner":player_name}) as resp:
        if resp.status_code != 200:
            raise Exception(f"query return code with {resp.status_code}")
        res = BeautifulSoup(resp.text, features="html.parser")
        return str(res.find_all('input', ['loadMore', 'btn', 'btn-primary'])[0]["onclick"]).split("'")[5]

def get_player_matches(player_id:str, page_count:int=1)->list:
    data_list = []
    for i in range(1, page_count+1):
        with requests.get(f"{BASE_URL}/moreGames/{player_id}/game{i}") as resp:
            if resp.status_code != 200:
                raise Exception(f"query return code with {resp.status_code}")
            res = BeautifulSoup(resp.json()['posts_html'], "html.parser")
            trs = res.find_all('tr', ['table-info', 'table-danger'])
            if trs is None or trs == []:
                raise ValueError("can not find player match data")
            if len(trs) % 2 != 0:
                raise ValueError("record format error")
            
            for i in range(len(trs)//2):
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
                data_fields["player_id"] = player_id
                
                # first row
                first_row = trs[2*i].find_all('td')
                data_fields["character"] = str(first_row[0].div.a['href']).split('/')[3]
                
                battle_stats = first_row[2].find_all('div')
                data_fields["match_res"] = battle_stats[0].b.string
                data_fields["gamemode"]  = battle_stats[1].string
                data_fields["start_time"] = battle_stats[2].string
                data_fields["gametip"] = battle_stats[3].string

                kda = first_row[3].div.find_all('span')
                kill = int(kda[0].string)
                death = int(kda[2].string)
                assist = int(kda[4].string)
                data_fields["K/D/A"] = f"{kill}/{death}/{assist}"
                data_list.append(data_fields)
    
    return data_list