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
accessToken = "0wBRFXP0oNcwOfxRjhVuOKY8VQvN7vpxM8MkQ2ghSMYj0eU6ZX/PtP56+plxwultEgH//ghIf8k/ZlKQLIXIoh6D3ZNo8lSiSIS7ZBDaQpjMPir3hdqxNcjqMrBE5ZaUYG0WIhLKdBXcSEgzfWd7bwdB04t89/1O/w1cDnyilFU="
secret = "4dc4dbdf9735525dd8b9aef5f86a415d"

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