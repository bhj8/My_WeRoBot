# -*- coding: utf-8 -*-

import os

import werobot
from dotenv import load_dotenv

load_dotenv()
AppID = os.getenv("MY_WEROBOT_APPID")
AppSecret = os.getenv("MY_WEROBOT_APPSECRET")
token=os.getenv("MY_WEROBOT_TOKEN")
print(AppID, AppSecret, token)

robot = werobot.WeRoBot( token=token)

@robot.handler
def hello(message):
    return 'Hello World!'

@robot.filter("帮助")
def show_help(message):
    return """
    帮助
    XXXXX
    """


@robot.text
def hello_world(message):
    return 'Hello World!'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()



# import werobot.utils

# print(werobot.utils.generate_token())