from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from bot import handler,get_group_ids
from schedulers.daliy_scheduler import start_scheduler

app = Flask(__name__)



@app.route("/", methods=['GET'])
def index():
    return "healthy"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


start_scheduler(get_group_ids())

# 啟動伺服器
if __name__ == "__main__":
    app.run()
