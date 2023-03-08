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

@robot.filter("示例")
def show_help(message):
    return """
画图 少女肖像, 脸, 特写, 尖耳朵, 连衣裙, 半闭眼, 首饰, 坐姿, 露肩, 露肩连衣裙, 水印, 皇冠，灰色连衣裙，长发，辫子，白发，长睫毛，独奏，小精灵

画图 两个女孩的肖像，脸，特写，尖耳朵，连衣裙，珠宝，坐姿，裸肩，头饰，灰色连衣裙, 长发, 辫子, 白发, 长睫毛, 侧脸, 精灵, 写实色彩,公主, 卷发，长发，闭上眼睛，
    """

#新用户关注
@robot.subscribe
def subscribe(message,session):
    return """以画图开头开始画图，如：
画图 美少女
故意发送不雅词汇将被警告并拉黑"""
    
@robot.text
def hello_world(message, session): 

    if message.content.startswith("画图"):
        if not session["in_paint"] or session["in_paint"] ==False :
            session["in_paint"] =True
            get_response(message,session) 
            return """请稍等，图片生成大约要10秒。
今日画风推荐核心关键词：少女，露肩连衣裙，坐姿，小精灵
输入“示例”查看优秀关键词"""
        else:
            return "正在有图片绘制中，请稍等再发送画图消息！"
    # asyncio.run(deal_message(message))
    return "目前只支持画图功能。请发送“画图 XXX”"
    # return werobot.replies.SuccessReply() # 用于响应微信服务器，不然会重试三次 

@robot.handler
def echo(message):
    return "暂时没这个功能，别试了"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

