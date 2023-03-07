# -*- coding: utf-8 -*-

import os

import werobot
from dotenv import load_dotenv

# import repeater

load_dotenv()
AppID = os.getenv("MY_WEROBOT_APPID")
AppSecret = os.getenv("MY_WEROBOT_APPSECRET")
token=os.getenv("MY_WEROBOT_TOKEN")

robot = werobot.WeRoBot( token=token)
client = robot.client
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret


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
    return 'Hello My Friend!'

@robot.text
def hello_world(message, session): 
    # repeater.get_response(message.content)
    #构建一个success的返回
    print(message.content)
    pass

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()



# import werobot.utils

# print(werobot.utils.generate_token())