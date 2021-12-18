from linebot import (
    LineBotApi, WebhookHandler
)
from os import getenv

line_bot_api = LineBotApi(getenv("LINE_BOT_API"))
line_webhook = WebhookHandler(getenv("WEBHOOK_HANDLER"))

