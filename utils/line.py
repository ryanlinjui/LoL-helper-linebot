from linebot import (
    LineBotApi, WebhookHandler
)
from os import getenv

from linebot.models.messages import TextMessage

line_bot_api = LineBotApi(getenv("LINE_BOT_API"))
line_webhook = WebhookHandler(getenv("WEBHOOK_HANDLER"))

from linebot.models import (
    ImageSendMessage
)

def pics_resp(url:str, preview=None)->ImageSendMessage:
    if preview is None:
        preview = url
    return ImageSendMessage(
        original_content_url=url,
        preview_image_url=preview
    )
def send_msg(line_id:str, msg:str):
    line_bot_api.push_message(line_id, TextMessage(text=msg))

def send_pic(line_id:str, url:str):
    line_bot_api.push_message(line_id, pics_resp(url))