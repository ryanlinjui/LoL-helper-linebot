from typing import Tuple

from .lolmoa import get_player_id as moa_player_id
from .lolmoa import get_player_matches as moa_player_match

import logging

def get_player_id(playername:str)->Tuple[str, str]:
    return (moa_player_id(playername), playername)

def get_player_matches(player_id:Tuple[str, str], page_count:int=1)->list:
    moa_pdata = moa_player_match(player_id[0], page_count=page_count*2)
    logging.info(f"successfully grab down {len(moa_pdata)} from moa")
    for i in range(len(moa_pdata)):
        moa_pdata[i]["player_id"] = player_id[1]
    return moa_pdata