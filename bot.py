# -*- coding: utf-8 -*-

import os

# import cryptography
import werobot
from dotenv import load_dotenv

from repeater import *

load_dotenv()
AppID = os.getenv("MY_WEROBOT_APPID")
AppSecret = os.getenv("MY_WEROBOT_APPSECRET")
token=os.getenv("MY_WEROBOT_TOKEN")
have_paint =os.getenv("MY_IS_PAINT")
aes_key=os.getenv('MY_ENCODING_AES_KEY')


robot = werobot.WeRoBot( token=token)
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret
robot.config['ENCODING_AES_KEY'] = aes_key
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
user_status = {}
def no_in_paint(user_status,user_id):
    user_status.pop(user_id)
def execute_after_five_seconds(user_status,user_id):
    time.sleep(10)
    no_in_paint(user_status,user_id)
def later_no_paint(user_id):
    thread = threading.Thread(target=execute_after_five_seconds,args=(user_status,user_id))
    thread.start()

@robot.filter("示例")
def show_help(message):
    return """
人物优秀示例：
画图 女孩，独奏，幻想，飞行，扫帚，夜空，户外，魔法，咒语，月亮，星星，云，风，头发，斗篷，帽子，靴子，扫帚，发光， 神秘的，迷人的，异想天开的，好玩的，冒险的，自由的，奇迹的，想象力的，决心的，技能的，速度的，运动的，能量的，现实主义的，自然主义的，比喻的，具象的，美丽的，幻想文化，神话，童话，民间传说，传说，女巫， 巫师,魔法生物,

风景优秀示例：
画图 户外，森林，岩石，河流，木材，烟雾，阴影，对比，晴朗的天空，星座，银河系，和平，宁静，安静，宁静，遥远，僻静，冒险， 构图,颜色,光,阴影,反射,折射,色调


题词技巧，按入下顺序题词：
1.主体：AI会以先人后物，先大后小的方式，选择构图。只写大的，例如山,湖也可以画风景。主体不够填充画面，AI会加入奇怪的东西。。。
2.人物的穿着打扮等细节和动作：金发，法袍，站姿，微笑，看向镜头等等
3.环境描写：城堡，童话世界，海洋，森林等等
4.镜头和光线：前景，中景，背景，日光，夜光等等

题词后台会自动帮您优化，不必要加太多不属于以上类别的词汇。不支持改变长宽比。
    """

#新用户关注
@robot.subscribe
def subscribe(message,session):
    return """我是小慧，目前提供画图功能。请输入：
画图 XXX
开始画图。支持语音输入。
请勿发送不雅词汇

公众号正在开发中，有时会突然停机更新。几分钟就好了。
更多更强大功能开发中！
"""

@robot.voice #我也并不知道语音识别有没有用
def handler_voice(message):
    message.content = message.recognition
    return hello_world(message)


@robot.text
def hello_world(message): 

    if message.content.startswith("画图"):
        if message.source not in user_status:
            user_status[message.source] =True
            later_no_paint(message.source)
            get_response(message) 
            return """请稍等，图片生成大约要20秒。
输入“示例”查看优秀关键词,题词技巧。
全新画风！限时开启超高清模式，画面会更加完美，但是生成时间会更长。
高清图微信会自动压缩，请点开图片后在左下角点击“查看原图”查看高清原图。"""
        else:
            return "请求过于频繁，请稍后再试。超高清模式下，10秒内只能画一张。请谅解"
    # asyncio.run(deal_message(message))
    return "目前只支持画图功能。请发送“画图 XXX”"



@robot.handler
def echo(message):
    return "暂时没这个功能，别试了。后期会支持上下文对话聊天,图片修复等等功能。"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

