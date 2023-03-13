
import math
import time
from concurrent.futures import (ALL_COMPLETED, FIRST_EXCEPTION,
                                ThreadPoolExecutor, wait)
from queue import Queue

from nsfw_api import *
from openai_api import *
from price import price
from stable_diffusion_api import SDapi
from Utils import utils

queue = Queue()

def set_client(c):
    global client
    client = c

def set_config(h_paint=False):
    global have_paint
    have_paint = h_paint
def set_sql(by_sql):
    global sql
    sql = by_sql

#临时创建一个sdapi实例
sdapi = SDapi()

#只能传int啊，千万别传字符串
def sql_score_change(id,**kwargs):
    if not sql.get(id):
        sql[id] = {}
    for key in kwargs:
        if key == "score_change":
            if not sql[id].get("freescore"):
                sql[id]["freescore"] = 0
            if not sql[id].get("score"):
                sql[id]["score"] = 0
            if sql[id]["freescore"] + kwargs[key] < 0:
                sql[id]["score"] += sql[id]["freescore"] + kwargs[key]
                sql[id]["freescore"] = 0
                if sql[id]["score"] < 0:
                    sql[id]["score"] = 0
            else:
                sql[id]["freescore"] += kwargs[key]
        if not sql[id].get(key):
            sql[id][key] = 0
        sql[id][key] += kwargs[key]
    

#画图全部堆在里面。。。
async def handle_paint(user_id, txt,seed)->bool: 
    count = 0
    while count < 3:
        try:
            if await get_moderation(txt) == True:
                print(user_id,"bad word")
                client.send_text_message(user_id, "很抱歉，经过AI判断，您的问题中可能包含不雅语义，我不会做出任何回答。出图后，AI会再次审核图片，意图违规使用将会被限制使用。no zuo no die！！！")
                return False
            txt = await get_translation([txt[:]]) # 翻译
            if not have_paint or have_paint  == False:#测试环境拿测试图片
                img_path =os.path.join(os.getcwd(), "test.png")
            else:
                imageinfo =  await sdapi.get_image(txt,seed)# 生成图片        
                if not imageinfo: # 生成失败
                    client.send_text_message(user_id, "很抱歉，图片生成失败。")
                    return False
                img_path =imageinfo[0]
            #print(img_path)
            try :
                p1 = img_path.split('/')[-1]
                if not  is_safe('./images/'+p1):                
                    print(user_id,"bad image")
                    client.send_text_message(user_id, "很抱歉，虽然图片已生成。但经过AI自行判断，您关键词生成的图片可能含有不雅内容。意图违规使用将会被限制使用")
                    return False
            except Exception as e:
                print(e)
            with open(img_path, "rb") as img:
                r_json =  client.upload_media("image",img)# 上传图片
                img.close()
                client.send_image_message(user_id, r_json["media_id"])# 发送图片
                with open('./media_id.txt', "a") as f:
                    f.write(time.strftime('%Y-%m-%d', time.localtime()) +" "+  r_json["media_id"] + '\n')
                print(user_id,"send image  ",len(txt),r_json["media_id"]) 
            return True
        except Exception as e:
            print(e)
        count += 1
    return False


async def try2paint(msg, dic):
    try:
        user_id =  msg.source
        txt = msg.content
        seed = dic["seed"]
        print(user_id,"   paint   ",txt) 

        await handle_paint(user_id, txt,seed )        
        sql_score_change(user_id,{"score_change":-price.high_pic})#高清图扣费
        return
            # reply = await get_response([txt])# 生成回复
            # client.send_text_message(user_id, reply)# 发送回复
            
    except Exception as e:
        print(e)
            
async def try2chat(msg, dic): 
    user_id =  msg.source
    chathistory_class = dic["chathistory"]
    lis = chathistory_class.history
    lis[-1]=  utils.replace_quick_question(lis[-1])# 替换快捷问题
    print(user_id,"  chat  ",lis[-1])
    try:
        result =  await get_chat_response(lis)        
        re_chat = result[0]
        use_token = result[1]
        # if await get_moderation(result) :#chatgpt的回复好像并不用过滤
        #     client.send_text_message(user_id, "很抱歉，我不喜欢聊这个话题。让我们换换其它话题吧！")
        #     return        
        re_chat =  utils.replace_badword_all(re_chat)    
        client.send_text_message(user_id, re_chat)

        sql_score_change(user_id,{"score_change":- math.ceil(use_token * price.per1000_chat/1000)})#聊天扣费
        print(user_id,"send","  chat message  ",len(re_chat))
    except Exception as e:
        print(e)

async def deal_message(msg,dic):
    if dic["mode"] =="paint":
        return await try2paint(msg, dic)
    if dic["mode"] =="chat":
        return await try2chat(msg, dic)

async def on_message():    
    try:
        while True:
            (msg,dic) = queue.get()
            await deal_message(msg,dic)
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


def get_response(msg,dic) -> None:
    queue.put((msg,dic))
