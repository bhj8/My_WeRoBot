
import time
from concurrent.futures import (ALL_COMPLETED, FIRST_EXCEPTION,
                                ThreadPoolExecutor, wait)
from queue import Queue

from werobot import messages

import stable_diffusion_api
from mystrings import *
from openai_api import *

queue = Queue(1024)

def __init__(self):
    pass
def set_client(c):
    global client
    client = c

def set_config(h_paint=False):
    global have_paint
    have_paint = h_paint

def replace_quick_question(txt: str):
    if txt in ["1", "2", "3", "4", "5", "6", "7"]:
        return quick_question[int(txt)-1]
    return txt

def is_paint(txt: str):
    if txt.startswith("画图"):
        return True
    return False

async def handle_paint(user_id, txt): #这些接口会卡住，我也不知道怎么解决。晚点再说吧
    if await get_moderation(txt) == True:
        client.send_text_message(user_id, "很抱歉，您的问题中可能包含不雅词汇，我不会做出任何回答。请您千万不要瞎搞搞啊！")
        return
    client.send_text_message(user_id, "请稍等，图片生成大约要10秒。")
    txt = await get_translation([txt[3:]]) # 翻译
    if not have_paint or have_paint  == False:
        print("have_paint == False")
        with open("test.jpg", "rb") as image_file:
            # 在这里执行对图片文件的操作
            image_data = image_file.read()
            imageinfo = [image_data, "test.jpg"]
    else:
        imageinfo =  await stable_diffusion_api.get_image(txt)# 生成图片
        if not imageinfo: # 生成失败
            client.send_text_message(user_id, "很抱歉，图片生成失败。")
            return 
    print("image",imageinfo[1])
    r_json =  client.upload_media(imageinfo[0],"image")# 上传图片
    print("image",r_json)
    client.send_image_message(user_id, r_json["media_id"])# 发送图片
    print("image",r_json["media_id"])

async def deal_message(msg:messages):
    user_id =  msg.source
    txt = msg.content
    print("user_id:",user_id,"txt:",txt) 

    txt =  replace_quick_question(txt)# 替换快捷问题
    if is_paint(txt) :# 画图
        await handle_paint(user_id, txt)
        return
    return
    # reply = await get_response([txt])# 生成回复
    # client.send_text_message(user_id, reply)# 发送回复


async def on_message():
    try:
        while True:
            (msg) = queue.get()
            await deal_message(msg)
            time.sleep(3)
    except Exception as e:
        print("\r" + e)


pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="on_message")
pool.submit(asyncio.run, on_message())



def get_response( msg:messages) -> None:
    queue.put((msg))