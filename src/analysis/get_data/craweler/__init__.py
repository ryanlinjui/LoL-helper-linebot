from typing import Tuple
# from .twlolstat import get_player_id as twlol_player_id
# from .twlolstat import get_player_matches as twlol_player_match

from .lolmoa import get_player_id as moa_player_id
from .lolmoa import get_player_matches as moa_player_match

import logging

def get_player_id(playername:str)->Tuple[str, str]:
    return (moa_player_id(playername), playername)

def get_player_matches(player_id:Tuple[str, str], page_count:int=1)->list:
    
    # twlol_pdata = twlol_player_match(player_id[0], page_count=page_count)
    # logging.info(f"successfully grab down {len(twlol_pdata)} from twlol")
    moa_pdata = moa_player_match(player_id[0], page_count=page_count*2)
    
    print(f"successfully grab down {len(moa_pdata)} from moa")
    logging.info(f"successfully grab down {len(moa_pdata)} from moa")
    
    for i in range(len(moa_pdata)):
        # twlol_pdata[i]["match_res"] = moa_pdata[i]["match_res"]
        # twlol_pdata[i]["gamemode"] = moa_pdata[i]["gamemode"]
        # twlol_pdata[i]["money"] = moa_pdata[i]["money"]
        # twlol_pdata[i]["CS"] = moa_pdata[i]["CS"]
        # twlol_pdata[i]["damage"] = moa_pdsata[i]["damage"]
        # twlol_pdata[i]["view"] = moa_pdata[i]["view"]
        # twlol_pdata[i]["start_time"] = moa_pdata[i]["start_time"]
        moa_pdata[i]["player_id"] = player_id[1]
    return moa_pdata