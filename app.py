from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=['GET'])
def hello_world():
    return "<h1>hellow world</h1>"
