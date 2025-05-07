from linebot.models import FlexSendMessage, URIAction

def create_button_message(title ='',subTitle='', url = ''):
    return FlexSendMessage(
        alt_text=title,
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md", 
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": subTitle,
                        "size": "sm",
                        "color": "#555555",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "paddingTop": "md",
                        "contents": [
                            {
                                "type": "button",
                                "action": URIAction(
                                    label=f'{title}: {subTitle}',
                                    uri=url
                                ),
                                "style": "primary"
                            }
                        ]
                    }
                ]
            }
        }
    )
