from flask import (
    Flask,
    request,
    abort
)
from linebot.exceptions import (
    InvalidSignatureError
)
import logging
from utils import (
    line_webhook,
)

import user_request

app = Flask(__name__)
logging.basicConfig(
    level = logging.INFO,
    filename = 'runtime.log',
    filemode = 'w',
    format = '%(asctime)s %(levelname)s: %(message)s'
)
@app.route("/", methods=['GET'])
def hello_world():
    return "<h1>hellow world</h1>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logging.debug(f"raw msg:{body}")
    # handle webhook body
    try:
        line_webhook.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'