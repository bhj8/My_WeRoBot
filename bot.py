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
client = robot.client
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret

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
    get_response(message)
    return werobot.replies.SuccessReply()


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()



# import werobot.utils

# print(werobot.utils.generate_token())