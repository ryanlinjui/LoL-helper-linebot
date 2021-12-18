from utils import (
    line_bot_api,
    line_webhook
)
from linebot.models import (
    MessageEvent, TextMessage,
)
import logging

@line_webhook.add(MessageEvent, message=TextMessage)
def user_text_request(event:MessageEvent):
    msg = str(event.message.text)
    logging.info(f"receive message:{msg}")
    line_bot_api.reply_message(
        event.reply_token,
        messages = TextMessage(text=msg)
    )