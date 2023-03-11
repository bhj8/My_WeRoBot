# -*- coding: utf-8 -*-

import hashlib
import os
import time

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
    time.sleep(20)
    no_in_paint(user_status,user_id)
def later_no_paint(user_id):
    thread = threading.Thread(target=execute_after_five_seconds,args=(user_status,user_id))
    thread.start()
# 将字符串和当前时间的毫秒数作为种子
def generate_seed(string):
    # 将当前时间的毫秒数转换为字符串，并追加到原始字符串后面
    string_with_time = string + str(int(round(time.time() * 1000)))
    
    # 使用SHA-256哈希函数计算字符串的哈希值
    hash_object = hashlib.sha256(string_with_time.encode())
    hash_hex = hash_object.hexdigest()
    
    # 将哈希值转换为一个32位的无符号整数作为种子
    seed = int(hash_hex, 16) % 2**32
    return seed
def is_valid_seed(seed_str):
    """
    Check if a string is a valid seed.
    A valid seed must have the following properties:
    - Length must be 9.
    - Only digits are allowed.
    - The sum of digits must be even.
    """
    if len(seed_str) != 9:
        return False
    if not seed_str.isdigit():
        return False
    return True
@robot.filter("示例")
def show_help(message):
    return """
人物优秀示例：
画图 女孩，独奏，幻想，飞行，扫帚，夜空，户外，魔法，咒语，月亮，星星，云，风，头发，斗篷，帽子，靴子，扫帚，发光， 神秘的，迷人的，异想天开的，好玩的，冒险的，自由的，奇迹的，想象力的，决心的，技能的，速度的，运动的，能量的，现实主义的，自然主义的，比喻的，具象的，美丽的，幻想文化，神话，童话，民间传说，传说，女巫， 巫师,魔法生物,

风景优秀示例：
画图 户外，森林，岩石，河流，木材，烟雾，阴影，对比，晴朗的天空，星座，银河系，和平，宁静，安静，宁静，遥远，僻静，冒险， 构图,颜色,光,阴影,反射,折射,色调


题词技巧，按如下顺序题词：
1.主体：AI会以先人后物，先大后小的方式，选择构图。只写大的，例如山,湖也可以画风景。主体不够填充画面，AI会加入奇怪的东西。。。
2.人物的穿着打扮等细节和动作：金发，法袍，站姿，微笑，看向镜头等等
3.环境描写：城堡，童话世界，海洋，森林等等
4.镜头和光线：前景，中景，背景，日光，夜光等等

题词后台会自动帮您优化，不必要加太多不属于以上类别的词汇。不支持改变长宽比。
    """

@robot.filter("种子")
def show_help(message):
    return"""遇到好看的画，请保存好（种子）和整段（提示词）的消息。
未来开通4k8k分辨率后，可以再次细绘该图。
种子绘高清图功能还在发开中！！！目前无法使用。但是您可以保存好种子，以便开放后绘制。"""

#新用户关注
@robot.subscribe
def subscribe(message,session):
    return """我是小慧，可以聊天和提供画图功能。请输入：
"画图 女孩" 即可开始画图。支持语音输入。
请勿发送不雅词汇

公众号正在开发中，有时会突然停机更新。几分钟就好了。
更多更强大功能开发中！
后期会支持图片修复等等功能。
"""

@robot.voice #我也并不知道语音识别有没有用
def handler_voice(message,session):
    message.content = message.recognition
    return hello_world(message,session)

#文本审核的regex
with open('badword.txt', 'r',encoding='UTF-8') as f:
    bad_words = [line.strip() for line in f]
regex = r'\b\S*(' + '|'.join(bad_words) + r')\S*\b'
def is_allowtxt(user_id,txt: str):
    if re.search(regex, txt, re.IGNORECASE) :
        return False
    return True
def replace_badword(txt: str):
    return re.sub(regex, '*', txt, flags=re.IGNORECASE)

@robot.text
def hello_world(message,session): 
    if 'user_id' not in session:
        session['user_id'] = message.source
    if 'use_num' not in session:
        session['use_num'] = 1
    else:
        session['use_num'] += 1

    # if not is_allowtxt(message.source,message.content) :
    #     return "很抱歉，您的问题中可能包含不雅词汇，我不会做出任何回答。所有图片都会经过AI自动审核违规内容，多次尝试画出法律不允许的内容，将可能会被限制使用"

    if message.content.startswith("画图"):
        message.content = message.content[2:].strip()#去掉画图两字
        if message.source not in user_status:#请求频率限制
            user_status[message.source] =True
            later_no_paint(message.source)
            # if message.content.startswith("种子"):#确定是否为种子模式
            #     seed_str = message.content[2:].strip()#获取种子字符串
            #     print(seed_str,"      ",type(seed_str))
            #     if is_valid_seed(seed_str) and  seed_str in session:
            #        message.content =  session[seed_str] 
            #        get_response(message,{"seed":int(seed_str)})
            #        return f"请稍等，图片生成大约要20秒。已经开始以种子{seed_str}绘制"
            #     else:
            #         return "种子错误，或无法读取。请重新输入。例如：画图 种子 196414898 "

            seed = generate_seed(message.source + message.content)
            # session[str(seed)] = message.content
            # asyncio.run(deal_message(message,{"seed":seed})) #临时测试用
            get_response(message,{"seed":seed,"mode":"paint","session":session})

            return f"""请稍等，图片生成大约要20秒。
输入“示例”查看优秀关键词,题词技巧。
输入“种子”查看种子说明。
全新画风！限时开启超高清模式，画面会更加完美，但是生成时间会更长。
高清图微信会自动压缩，请点开图片后在左下角点击“查看原图”查看高清原图。
本次作画画风为：真彩动漫 种子为：{seed} 
"""
        else:
            return "请求过于频繁，请稍后再试。超高清模式下，20秒内只能画一张。请谅解"
    messages.content = replace_badword(message.content)
    get_response(message,{"session":session,"mode":"chat"})
    
    if "图" in message.content or "画" in message.content :
        return "想要画图，请以画图会开头。例如：画图 金发女孩"

    #一个success的return，不然会报错
    return werobot.replies.SuccessReply()

    



@robot.handler
def echo(message):
    return "暂时没这个功能，别试了。后期会支持上下文对话聊天,图片修复等等功能。"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

