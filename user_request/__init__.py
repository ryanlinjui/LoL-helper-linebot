from linebot.models.sources import SourceUser
from linebot.models.template import ButtonsTemplate
from utils import (
    line_bot_api,
    line_webhook
)
from linebot.models import (
    MessageEvent, TextMessage,TemplateSendMessage, PostbackAction
)
import logging

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

def print_menu(line_id:str):
    line_bot_api.push_message(
        line_id,
        TemplateSendMessage(
            alt_text="歡迎來到LoL雷包分析系統",
            template=ButtonsTemplate(
                type="buttons",
                thumbnail_image_url="https://i.imgur.com/zFeydUT.jpg",
                title="歡迎來到LoL雷包分析系統",
                text="請選擇分析項目",
                actions=[
                    PostbackAction(
                        label="一般對戰",
                        data="blindpick"
                    ),
                    PostbackAction(
                        label="積分對戰",
                        data="rank"
                    ),
                    PostbackAction(
                        label="隨機單中",
                        data="aram"
                    ),
                    PostbackAction(
                        label="切換召喚師",
                        data="logout"
                    )
                ]
            )
        )
    )