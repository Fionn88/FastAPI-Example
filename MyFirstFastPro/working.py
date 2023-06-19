from fastapi import FastAPI, Request, HTTPException

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# Line Bot config
accessToken = "your access token to line bot which get from line biz"
secret = "your secret token to access line bot webhook get from line developer"

app = FastAPI()

line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler(secret)

@app.post("/")
async def echoBot(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    replyToken = event.reply_token
    
    if isinstance(event.message, TextMessage):
        messages = event.message.text
        
        echoMessages = TextSendMessage(text=messages)
        line_bot_api.reply_message(reply_token=replyToken, messages=echoMessages)
