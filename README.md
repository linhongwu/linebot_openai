# hello world# =============================================================================# #======讓heroku不會睡著======# import threading # import requests# def wake_up_heroku():#     while 1==1:#         url = '你的herokuapp網址' + 'heroku_wake_up'#         res = requests.get(url)#         if res.status_code==200:#             print('喚醒heroku成功')#         else:#             print('喚醒失敗')#         time.sleep(28*60) #28min*60second. Render 是50min 所以可以改為 48*60# # threading.Thread(target=wake_up_heroku).start()# #======讓heroku不會睡著======# =============================================================================# =============================================================================# chatGPt 重新寫過的程式# from flask import Flask, request, abort# from linebot import LineBotApi, WebhookHandler# from linebot.exceptions import InvalidSignatureError# from linebot.models import *# import openai# import os# import traceback# # # 初始化 Flask 應用# app = Flask(__name__)# # # Channel Access Token 和 Channel Secret# line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))# handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))# # # 初始化 OpenAI API Key# openai.api_key = os.getenv('OPENAI_API_KEY')# # def GPT_response(text):#     # 使用 ChatCompletion 呼叫 gpt-3.5-turbo 模型#     try:#         response = openai.ChatCompletion.create(#             model="gpt-3.5-turbo",#             messages=[{"role": "user", "content": text}],#             temperature=0.5,#             max_tokens=500#         )#         print(response)#         # 重組回應#         answer = response['choices'][0]['message']['content'].replace('。', '')#         return answer#     except Exception as e:#         print(f"OpenAI API 呼叫錯誤: {e}")#         return "抱歉，目前無法處理您的請求，請稍後再試。"# # # 監聽所有來自 /callback 的 Post Request# @app.route("/callback", methods=['POST'])# def callback():#     signature = request.headers['X-Line-Signature']#     body = request.get_data(as_text=True)#     app.logger.info("Request body: " + body)# #     try:#         handler.handle(body, signature)#     except InvalidSignatureError:#         abort(400)#     return 'OK'# # # 處理訊息事件# @handler.add(MessageEvent, message=TextMessage)# def handle_text_message(event):#     msg = event.message.text#     try:#         GPT_answer = GPT_response(msg)#         print(GPT_answer)#         line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))#     except Exception as e:#         print(traceback.format_exc())#         line_bot_api.reply_message(event.reply_token, TextSendMessage(f'發生錯誤：{str(e)}'))# # # 處理 Postback 事件# @handler.add(PostbackEvent)# def handle_postback(event):#     print(event.postback.data)# # # 歡迎新成員事件# @handler.add(MemberJoinedEvent)# def welcome_new_member(event):#     uid = event.joined.members[0].user_id#     gid = event.source.group_id#     profile = line_bot_api.get_group_member_profile(gid, uid)#     name = profile.display_name#     message = TextSendMessage(text=f'{name} 歡迎加入')#     line_bot_api.reply_message(event.reply_token, message)# # # 啟動應用# if __name__ == "__main__":#     port = int(os.environ.get('PORT', 5000))#     app.run(host='0.0.0.0', port=port)# =============================================================================