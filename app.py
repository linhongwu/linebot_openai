# from flask import Flask, request, abort

# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import *

# #======python的函數庫==========
# import tempfile, os
# import datetime
# import openai
# import time
# import traceback
# #======python的函數庫==========

# app = Flask(__name__)
# static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# # Channel Access Token
# line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# # Channel Secret
# handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# # OPENAI API Key初始化設定
# openai.api_key = os.getenv('OPENAI_API_KEY')


# def GPT_response(text):
#     # 接收回應
#     response = openai.Completion.create(model="gpt-4", prompt=text, temperature=0.5, max_tokens=500)
#     print(response)
#     # 重組回應
#     answer = response['choices'][0]['text'].replace('。','')
#     return answer


# # 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'


# # 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text
#     try:
#         GPT_answer = GPT_response(msg)
#         print(GPT_answer)
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
#     except:
#         print(traceback.format_exc())
#         line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))
        

# @handler.add(PostbackEvent)
# def handle_message(event):
#     print(event.postback.data)


# @handler.add(MemberJoinedEvent)
# def welcome(event):
#     uid = event.joined.members[0].user_id
#     gid = event.source.group_id
#     profile = line_bot_api.get_group_member_profile(gid, uid)
#     name = profile.display_name
#     message = TextSendMessage(text=f'{name}歡迎加入')
#     line_bot_api.reply_message(event.reply_token, message)
        
        
# import os
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
    
    
    
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, MemberJoinedEvent
import os
import openai
import traceback

# Flask 應用初始化
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OpenAI API Key 初始化
openai.api_key = os.getenv('OPENAI_API_KEY')

# GPT-4 回應函數
def GPT_response(text):
    try:
        # 使用 ChatCompletion 來呼叫 gpt-4 模型
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}],
            temperature=0.5,
            max_tokens=500
        )
        print(response)  # 列印完整回應以供調試
        # 重組回應
        answer = response['choices'][0]['message']['content'].replace('。', '')
        return answer
    except Exception as e:
        print("GPT 回應錯誤:", str(e))
        print(traceback.format_exc())
        return "抱歉，目前無法處理您的請求，請稍後再試。"

# 監聽來自 /callback 的 POST Request
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature header 的值
    signature = request.headers['X-Line-Signature']
    # 取得請求的主體內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 處理 webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        GPT_answer = GPT_response(msg)
        print("GPT 回應:", GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        print("訊息處理錯誤:")
        print(traceback.format_exc())
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的 OPENAI API key 額度可能已經超過，請於後台 Log 內確認錯誤訊息'))

# 處理 Postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    print("Postback data:", event.postback.data)

# 處理群組成員加入事件
@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name} 歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

# 主程式入口
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)