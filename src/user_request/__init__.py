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

@line_webhook.add(MessageEvent, message=TextMessage)
def user_text_request(event:MessageEvent):
    msg = str(event.message.text)
    logging.info(f"receive message:{msg}")
    # TODO:login check
    line_bot_api.reply_message(
        event.reply_token,
        messages = TextMessage(text=msg)
    )
    print_menu(event.source.user_id)

@line_webhook.add(PostbackEvent)
def user_postback_request(event:PostbackEvent):
    logging.info(f"receive postback message:{event}")
    mode = event.postback.data
    if mode in ['blindpick', 'rank', 'aram']:
        # get data
        rate = 0.87
        most_used = ['a', 'b', 'c']
        top_hero = ['c', 'd', 'e']
        avg_time = 4.87639

        graph_data = {
            "KDA": random.random(),
            "CSPM": random.random(),
            "DPM": random.random(),
            "GPM": random.random()
        }

        # craft response
        logging.warning(f"user performance: {graph_data}")
        dst_fname = create_tmpfile_name(".png")
        user_perf_pic(graph_data, dst_fname)
        rlink = upload(dst_fname)
        
        user_id = event.source.user_id
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
        pass
