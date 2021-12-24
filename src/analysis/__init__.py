from access import(
    login,
    is_login,
    logout,
    get_player_data,
    update_db
)

def behavior(line_user_id:str,mode:str):
    if mode == "切換玩家":
        return logout(line_user_id)
    return get_player_data(line_user_id,mode)
update_db()