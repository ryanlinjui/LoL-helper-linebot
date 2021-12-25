from .access import(
    login,
    is_login,
    logout,
    get_player_data,
    update_db
)

update_db()

def behavior(line_user_id:str,mode:str):
    return get_player_data(line_user_id,mode)