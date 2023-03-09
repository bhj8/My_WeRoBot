
import io
import re
import threading
import time
from concurrent.futures import (ALL_COMPLETED, FIRST_EXCEPTION,
                                ThreadPoolExecutor, wait)
from queue import Queue

from werobot import messages

from mystrings import *
from openai_api import *
from stable_diffusion_api import *

queue = Queue()

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

#正则检查文本
with open('badword.txt', 'r',encoding='UTF-8') as f:
    bad_words = [line.strip() for line in f]
regex = r'\b(' + '|'.join(bad_words) + r')\b'
def is_allowtxt(user_id,txt: str):
    if re.search(regex, txt, re.IGNORECASE) :
        client.send_text_message(user_id, "很抱歉，您的问题中可能包含不雅词汇，我不会做出任何回答。请您千万不要瞎搞搞啊！短时间内频繁检测到将可能会被限制使用。")
        return False
    return True

def is_paint(txt: str):
    if txt.startswith("画图"):
        return True
    return False

async def handle_paint(user_id, txt): #这些接口会卡住，我也不知道怎么解决。晚点再说吧
    count = 0
    while count < 3:
        try:
            if await get_moderation(txt) == True:
                print(user_id,"bad word")
                client.send_text_message(user_id, "很抱歉，您的问题中可能包含不雅词汇，我不会做出任何回答。请您千万不要瞎搞搞啊！短时间内频繁检测到将可能会被限制使用。no zuo no die！！！")
                return
            txt = await get_translation([txt[3:]]) # 翻译

            if not have_paint or have_paint  == False:
                img_path =os.path.join(os.getcwd(), "test.png")
            else:
                imageinfo =  await get_image(txt)# 生成图片        
                if not imageinfo: # 生成失败
                    client.send_text_message(user_id, "很抱歉，图片生成失败。")
                    return 
                img_path =imageinfo[0]
            print(img_path)
            with open(img_path, "rb") as img:
                r_json =  client.upload_media("image",img)# 上传图片
                img.close()
                client.send_image_message(user_id, r_json["media_id"])# 发送图片
                print("send image",txt, user_id, r_json["media_id"]) 
            return
        except Exception as e:
            print(e)
        count += 1

async def deal_message(msg):
    try:
        user_id =  msg.source
        txt = msg.content
        print("user_id:",user_id,"txt:",txt) 
        if not is_allowtxt(user_id,txt):
            return
        txt =  replace_quick_question(txt)# 替换快捷问题

        if is_paint(txt) :# 画图
            await handle_paint(user_id, txt)
            return
        # reply = await get_response([txt])# 生成回复
        # client.send_text_message(user_id, reply)# 发送回复
        
    except Exception as e:
        print(e)
        


async def on_message():    
    try:
        while True:
            (msg) = queue.get()
            await deal_message(msg)
            await asyncio.sleep(2)
    except Exception as e:
        print("\r" + e)


pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="on_message")
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())


def get_response(msg) -> None:
    queue.put((msg))
