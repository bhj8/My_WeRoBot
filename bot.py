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
    画图 美少女"""

@robot.text
def hello_world(message): 
    # get_response(message)
    #asyncio.run(deal_message(message))
    
    loop = asyncio.new_event_loop()

    # 创建一个任务并将其添加到事件循环中
    task = loop.create_task(deal_message(message))

    # 关闭事件循环并返回结果
    loop.close()
    return ""


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()



# import werobot.utils

# print(werobot.utils.generate_token())