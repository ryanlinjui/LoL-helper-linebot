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
from get_data.func import (
    login,
    is_login,
    behavior
)


@line_webhook.add(MessageEvent, message=TextMessage)
def user_text_request(event:MessageEvent):
    msg = str(event.message.text)
    user_id = event.source.user_id
    logging.info(f"receive message:{msg}")
    # TODO:login check
    if is_login(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            messages= TextMessage(text="還想搞我啊 菜雞")
        )
    else:
        try:
            login(user_id, msg)
            line_bot_api.reply_message(
                event.reply_token,
                messages = TextMessage(text=f"登入成功 當前召喚師:{msg}")
            )
            print_menu(user_id)
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token,
                messages= TextMessage(text="登入失敗")
            )

@line_webhook.add(PostbackEvent)
def user_postback_request(event:PostbackEvent):
    logging.info(f"receive postback message:{event}")
    mode = event.postback.data
    if mode in ['blind_pick', 'ranked_solo/duo', 'aram']:
        # get data
        data = behavior(event.source.user_id, mode)
        rate = data['rate']
        most_used = data['used_champion_rank3']
        top_hero = data['rate_champion_rank3']
        avg_time = data['avg_game_time']

        graph_data = {
            "KDA": data['avg_kda'],
            "CSPM": data['cspm'],
            "DPM": data['dpm'],
            "GPM": data['gpm']
        }

        # craft response
        logging.warning(f"user performance: {graph_data}")
        dst_fname = create_tmpfile_name(".png")
        user_perf_pic(graph_data, dst_fname)
        rlink = upload(dst_fname)
        
        user_id = event.source.user_id
        send_msg(user_id,
        "一般對戰勝率：{:.2f}%\n".format(rate*100)+ \
        f"前三使用最高的英雄為：{','.join(most_used)}\n"+ \
        f"前三勝率最高的英雄為：{','.join(top_hero)}\n"+ \
        "一般對戰平均遊戲時間：{:.2f} min".format(avg_time)
        )
        send_pic(user_id, rlink)
        os.remove(dst_fname)
        print_menu(user_id)
    elif mode == 'logout':
        if behavior(event.source.user_id, mode):
            send_msg(event.source.user_id, "登出成功")
        else:
            send_msg(event.source.user_id, "還想搞阿 菜雞")
