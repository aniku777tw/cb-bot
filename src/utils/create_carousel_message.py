
from linebot.models import FlexSendMessage
def create_carousel_message(data: list,code: str) -> FlexSendMessage:
    """根據爬取的資料創建 LINE Flex Message 格式"""
    
    # 建立 Flex Message 內容
    flex_message = {
        "altText": f"{code} 可轉債資訊",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": []
            }
        }
    }

    # 從資料中生成表格的每一行
    for row in data:
        flex_message["contents"]["body"]["contents"].append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": row[0],  # 顯示左邊的標題（例如 可轉債名稱）
                    "size": "sm",
                    "flex": 2   ,
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": row[1],  # 顯示右邊的值（例如 92.99）
                    "size": "sm",
                    "flex": 1
                }
            ]
        })

    return FlexSendMessage(alt_text=flex_message['altText'], contents=flex_message['contents'])


