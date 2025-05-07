import os
import re
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage
from dotenv import load_dotenv
from utils.create_carousel_message import create_carousel_message
from crawler.convertbond import fetch_convertbond_info_with_cache,fetch_convertbond_info,set_cache

load_dotenv()  

# 讀取你的 token & secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

group_ids = set()

# Webhook 訊息處理
@handler.add(MessageEvent, message=TextMessage )
def handle_message(event):
    if event.source.type == 'group':
        group_id = event.source.group_id
        group_ids.add(group_id) 
        print("加入群組：", group_id)
        
        if re.match(r'^\d{5}\sdata$', event.message.text):
            code = event.message.text.split()[0] 
 

            cb_data = fetch_convertbond_info_with_cache(code)
            if cb_data is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'沒有 {code} 快取，正在爬取資料...'))
                cb_data = fetch_convertbond_info(code)
                set_cache(cb_data, code)
                flex_message = create_carousel_message(cb_data)
                line_bot_api.push_message(group_id,flex_message)
            else:           
                flex_message = create_carousel_message(cb_data)
                line_bot_api.reply_message(event.reply_token, flex_message)
                return
    

def get_group_ids():
    return group_ids