import logging
from pprint import pprint

from form import (
    export_to_xlsx,
    read_csv_reply
)
from craweler import (
    get_player_id,
    get_player_matches
)
from datetime import datetime

def get_currect_time()->str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f'{get_currect_time()}.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s [ %(name)s ] %(levelname)s : %(message)s'))
root_logger.addHandler(handler)

def main():
    player_data = read_csv_reply("LOL數據調查.csv")
    match_data = []
    for email, playername in player_data:
        try:
            print(f"conducting queries on {playername}")
            player_id =  get_player_id(playername)
            match_data += get_player_matches(player_id)
        except Exception as e:
            logging.error(f"error on processing {playername}")
            
    export_to_xlsx(match_data, "data.xlsx")
    
if __name__ == "__main__" :
    main()