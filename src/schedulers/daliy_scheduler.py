import schedule
import time
import threading
from bot import line_bot_api
from datetime import datetime, timedelta
from utils.create_button_message import create_button_message  

def push_to_groups(group_ids):
    for gid in group_ids:
        yesterday = (datetime.today() - timedelta(hours = 16)).strftime('%Y%m%d')
        flex_message = create_button_message(f'昨日 CBAS 拆解',f'{yesterday}',f'https://www.tpex.org.tw/www/zh-tw/extendProduct/statTrDl?type=daily&fileName=CBdas001&date={yesterday}')  # 取得 Flex 訊息
        line_bot_api.push_message(gid, flex_message)

def start_scheduler(group_ids):
    def job():
        today = datetime.today().weekday()   
        if today >= 5:
            print("It's weekend! Skipping job.")
            return  
        push_to_groups(group_ids)

    schedule.every().day.at("13:00").do(job)

    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run).start()

