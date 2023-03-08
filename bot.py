# -*- coding: utf-8 -*-

import os

import werobot
from dotenv import load_dotenv

from repeater import *

load_dotenv()
AppID = os.getenv("MY_WEROBOT_APPID")
AppSecret = os.getenv("MY_WEROBOT_APPSECRET")
token=os.getenv("MY_WEROBOT_TOKEN")
have_paint =os.getenv("MY_IS_PAINT")

robot = werobot.WeRoBot( token=token)
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret
client = robot.client

set_client(client)
if have_paint == "True":
    have_paint = True
else:
    have_paint = False
set_config(have_paint)
# @robot.handler
# def hello(message):
#     return message.content

@robot.filter("帮助")
def show_help(message):
    return """
    帮助
    XXXXX
    """

#新用户关注
@robot.subscribe
def subscribe(message):
    return """以画图开头开始画图，如：
画图 美少女
故意发送不雅词汇将被警告并拉黑"""
    
@robot.text
def hello_world(message): 
    get_response(message)
    # asyncio.run(deal_message(message))
    return "请稍等，图片生成大约要10秒。"
    # return werobot.replies.SuccessReply() # 用于响应微信服务器，不然会重试三次 

@robot.handler
def echo(message):
    return "暂时没这个功能，别试了"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

