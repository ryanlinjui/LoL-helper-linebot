from bot_func import player_imformation

user_state = {}
player = player_imformation()

def login(line_user_id:str,lol_player_id:str):
    player.id = lol_player_id
    player.set_data()
    if player.is_not_exist():
        raise ValueError("This LoL player id is not found")
    user_state[line_user_id] = lol_player_id

def behavior(line_user_id:str,mode:str):
    return player.get_data(mode)

def is_login(line_user_id:str):
    if line_user_id in user_state:
        return True
    return False
    

print(login("3","特務小熊熊"))
print(behavior("3","blind_pick"))
print(is_login("3"))

    


