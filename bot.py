# -*- coding: utf-8 -*-

import hashlib
import os
import threading
import time

# import cryptography
import werobot
from dotenv import load_dotenv

from ChatHistory import chathistory
from mytxt import mytxt
from repeater import *
from Utils import utils

load_dotenv()
try:
    AppID = os.getenv("MY_WEROBOT_APPID")
    AppSecret = os.getenv("MY_WEROBOT_APPSECRET")
    token=os.getenv("MY_WEROBOT_TOKEN")
    have_paint =os.getenv("MY_IS_PAINT")
    aes_key=os.getenv('MY_ENCODING_AES_KEY')
except:
    print("请在根目录下创建.env文件，并在.env文件中填写相关信息.别tm在忘记了，受不了了")
    exit()


robot = werobot.WeRoBot( token=token)
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret
robot.config['ENCODING_AES_KEY'] = aes_key
client = robot.client

sql = robot.session_storage#实例化数据库  openai：1."score"积分2."freescore"每日免费积分 3."inrmb"总充值金额 4."friendkey"邀请码 5."chats"总聊天次数 6."paints"总画画次数 7."all_invite"总邀请次数




set_client(client)
if have_paint == "True":
    have_paint = True
else:
    have_paint = False
set_config(have_paint)
set_sql(sql)
# @robot.handler
# def hello(message):
#     return message.content


#并发限制
user_status = {}
def no_in_paint(user_status,user_id):
    user_status.pop(user_id)
def execute_after_five_seconds(user_status,user_id):
    time.sleep(5)
    no_in_paint(user_status,user_id)
def later_no_paint(user_id):
    thread = threading.Thread(target=execute_after_five_seconds,args=(user_status,user_id))
    thread.start()

#储存聊天记录到内存
user_chats = {}
#设置新用户的sql
def set_newuser_sql(message, session):
    fkey = utils.get_friendkey()
    session['friendkey'] = fkey #先绑定一个邀请码
    if not 'score' in session:
        session['score'] = price.new_user#就这里预设了新用户的积分
    if not 'freescore' in session:
        session['freescore'] = 0
    if not 'inrmb' in session:
        session['inrmb'] = 0
    if not 'chats' in session:
        session['chats'] = 0
    if not 'paints' in session:
        session['paints'] = 0
    if not 'all_invite' in session:
        session['all_invite'] = 0
    sql.set(fkey,{"user_id":message.source})
    if  "count" not in  sql.get(fkey):
        sql.set(fkey,{"count":0})
#设置邀请码的sql
def set_invite_sql(user_id):
    sql.set(user_id,{"all_invite":sql.get(user_id)["all_invite"]+1})
    sql.set(user_id,{"score":sql.get(user_id)["score"]+price.invite_user})
    pass


@robot.filter("示例")
def show_shili(message):
    return mytxt.welcometxt

@robot.filter("模式")
def show_zhongzi(message):
    return mytxt.panint_modeltxt

@robot.filter("管理员")
def show_guanliyuan(message):
    with open("admin.txt","w") as f:
        f.write(client._token)
    return werobot.replies.SuccessReply()

@robot.filter("积分")
def show_score(message, session):
    if sql.get(message.source) == {}:
        set_newuser_sql(message, session)
    return f"""你的永久积分为{sql.get(message.source)['score']} 永久积分通过充值和邀请好友获得。
免费积分为:{ sql.get(message.source)['freescore']}) 免费积分通过获得领取。优先使用免费积分。
你已经邀请了{sql.get(message.source)['all_invite']}个用户"""#(每日6点重置为{price.daily_user}

@robot.filter("帮助")
def show_help(message):
    return  mytxt.help_txt

@robot.filter("邀请码")
def show_invite(message, session):
    if sql.get(message.source) == {}:
        set_newuser_sql(message, session)
    client.send_text_message(message.source,mytxt.invite_txt)
    return f"{sql.get(message.source)['friendkey']}"


#新用户关注
@robot.subscribe
def subscribe(message,session):
    set_newuser_sql(message, session)
    return mytxt.newusertxt


@robot.voice #语音转文字后发送到文字处理函数
def handler_voice(message,session):
    message.content = message.recognition
    return hello_world(message,session)

@robot.text #文字处理函数
def hello_world(message,session): 
    if message.content.startswith("id"):#输入验证邀请码
        if  utils.is_valid_invite_code(message.content.strip()) :
            key_dic = sql.get(message.content.strip())
            if  key_dic != {}:
                user_id =  key_dic["user_id"]
                if sql.get(user_id)  != {}:
                    set_invite_sql(user_id)                    
                    return "邀请码输入成功！感谢你的支持！"
        return "邀请码不存在，确认后重新输入。一个正常的邀请码为  id_a665a459  。你只需要输入邀请码，不用任何多余的字符"

    #看看积分还够不够
    if message.source not in sql:
        set_newuser_sql(message, session)
    
    if sql.get(message.source)["score"] + sql.get(message.source)["freescore"] < 0:
        client.send_text_message(message.source,sql.get(message.source)["friendkey"])
        return"""积分不足，无法继续聊天。请充值后再使用。
你也可以邀请任意好友关注 小慧很智慧 
并将您的邀请码发送给小慧,即可获得免费{price.invite_user}永久积分"""

    if not utils.is_allow_paint_txt(message.content) :
        return "很抱歉，经过AI判断，您的问题中可能包含不雅语义，我不会做出任何回答。出图后，AI会再次审核图片，意图违规使用将会被限制使用。no zuo no die！！！"

    if message.content.startswith("画图"):#画图
        message.content = message.content[2:].strip()#去掉画图两字
        if message.source not in user_status:#请求频率限制
            user_status[message.source] =True
            later_no_paint(message.source)
            seed = utils.generate_seed(message.source + message.content)
            # session[str(seed)] = message.content
            # asyncio.run(deal_message(message,{"seed":seed})) #临时测试用
            get_response(message,{"seed":seed,"mode":"paint","session":session})

            return mytxt.start_point_txt
        else:
            return "请求过于频繁，请稍后再试。超高清模式下，20秒内只能画一张。请谅解"
    # messages.content = replace_badword(message.content)
    if message.source not in user_chats:
        user_chats[message.source] = chathistory()
    user_chats[message.source].add(message.content)
    get_response(message,{"chathistory":user_chats[message.source],"mode":"chat"})
    
    if "图" in message.content or "画" in message.content :
        return "想要画图，请以画图会开头。例如：画图 金发女孩"
    if "邀" in message.content or "码" in message.content  or "邀请" in message.content:
        return show_invite(message, session)

    #一个success的return，不然会报错
    return werobot.replies.SuccessReply()

@robot.handler#意外处理函数
def echo(message):
    return mytxt.unexpected_txt



robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

