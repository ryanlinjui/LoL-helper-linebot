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
    behavior
)

@line_webhook.add(MessageEvent, message=TextMessage)
def user_text_request(event:MessageEvent):
    user_id = event.source.user_id
    msg = str(event.message.text)
    logging.info(f"receive message:{msg}")
    # TODO:login check
    if not(login(user_id,msg)):
        raise Exception("Login Error")
    line_bot_api.reply_message(
        event.reply_token,
        messages = TextMessage(text=msg)
    )
    print_menu(user_id)

@line_webhook.add(PostbackEvent)
def user_postback_request(event:PostbackEvent):
    user_id = event.source.user_id
    logging.info(f"receive postback message:{event}")
    mode = event.postback.data
    if mode in ['blindpick', 'rank', 'aram']:
        # get data
        data = behavior(user_id,mode)
        rate = data["rate"]
        most_used = data["most_used"]
        top_hero = data["rank_champion"]
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
        
        
        send_msg(user_id,
        f"一般對戰勝率：{rate}\n"+ \
        f"前三使用最高的英雄為：{','.join(most_used)}\n"+ \
        f"前三勝率最高的英雄為：{','.join(top_hero)}\n"+ \
        "一般對戰平均遊戲時間：{:.2f}".format(avg_time)
        )
        send_pic(user_id, rlink)
        os.remove(dst_fname)
        print_menu(user_id)
    elif mode == 'logout':
        logout(user_id)
