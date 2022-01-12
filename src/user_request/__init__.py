from linebot.models.events import PostbackEvent
from utils import *
from linebot.models import (
    MessageEvent, TextMessage
)
from .misc import print_menu
from ui.status_eval import user_perf_pic
import logging
import random
from utils import (
    line_bot_api,
    line_webhook,
    create_tmpfile_name,
    send_msg,
    send_pic
)
from utils.imgur.upload import (
    upload
)
import os
from analysis import (
    login,
    is_login,
    logout,
    behavior,
    get_user_status,
    get_mode_zh_tw,
    get_player_total_num
)

@line_webhook.add(MessageEvent, message=TextMessage)
def user_text_request(event:MessageEvent):
    user_id = event.source.user_id
    msg = str(event.message.text)
    logging.info(f"receive message:{msg}")
    # TODO:login check
    
    if is_login(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            messages = TextMessage(text="目前正在查看的玩家:\n"+get_user_status(user_id)+"\n(不要想搞事ㄟ，請好好善待這個系統)"
        ))
        print_menu(user_id)
        return
    if login(user_id,msg):
        logging.info(f"[{user_id}]: Login with {msg}")
        line_bot_api.reply_message(
            event.reply_token,
            messages = TextMessage(text="目前正在查看的玩家:\n"+get_user_status(user_id)
        ))
        print_menu(user_id)
        return
    else:
        line_bot_api.reply_message(
            event.reply_token,
            messages = TextMessage(text=f"查不到最近任何{msg}的對戰紀錄\n無法分析!")
        )
        return
        

@line_webhook.add(PostbackEvent)
def user_postback_request(event:PostbackEvent):
    user_id = event.source.user_id
    logging.info(f"receive postback message:{event}")
    if not(is_login(user_id)):
        send_msg(user_id,"歡迎來到LoL線上分析系統，請輸入玩家名分析\n(你不要想搞事ㄟ，請好好善待這個系統)")
        return
    mode = event.postback.data

    if mode in ["blindpick","rank","flex","aram"]:
        send_msg(user_id,f"正在分析\n{get_user_status(user_id)}的\n{get_mode_zh_tw(mode)}\n請稍候......")
        # get data
        logging.info(f"[{user_id}]: Look for {mode} of {get_user_status(user_id)}")
        data = behavior(user_id,mode)
        if len(data)==0:
            send_msg(user_id,f"{get_user_status(user_id)}\n最近沒有任何{get_mode_zh_tw(mode)}的對戰紀錄\n無法分析!")
            print_menu(user_id)
            return
        rate = data["rate"]
        most_used = data["most_used"].split('%')
        top_hero = data["rank_champion"].split('%')
        avg_time = data["game_time"]
        graph_data = {
            "KDA": data["kda"],
            "CSPM": data["cspm"],
            "DPM": data["dpm"],
            "GPM": data["gpm"],
        }
        # craft response
        logging.warning(f"user performance: {graph_data}")
        dst_fname = create_tmpfile_name(".png")
        user_perf_pic(graph_data, dst_fname)
        rlink = upload(dst_fname)
        
        most_used_str = ""
        top_hero_str = ""
        for i in range(len(most_used)):
            most_used_str += "("+str(i+1)+"): "+ most_used[i] + "\n"
            
        for i in range(len(top_hero)):
            top_hero_str += "("+str(i+1)+"): "+ top_hero[i] + "\n"

        send_msg(user_id,
            f"根據目前資料庫中總共{get_player_total_num()}名LoL玩家資料進行分析:\n"+ \
            f"{get_mode_zh_tw(mode)}勝率：{int(rate*10000+0.5)/100}%\n"+ \
            f"前三使用最高的英雄為：\n"+ \
            most_used_str+ \
            f"前三勝率最高的英雄為：\n"+ \
            top_hero_str+ \
            "{:s}平均遊戲時間：{:d}:{:d}".format(get_mode_zh_tw(mode),int(avg_time),(int((avg_time-int(avg_time))*60)))
        )
        send_pic(user_id, rlink)
        os.remove(dst_fname)
        print_menu(user_id)
    elif mode == 'logout':
        send_msg(user_id,"切換使用者\n歡迎來到LoL線上分析系統，請輸入玩家名分析")
        logout(user_id)
        logging.info(f"[{user_id}]: Logout")
