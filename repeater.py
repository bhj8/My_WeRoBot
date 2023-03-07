from typing import Optional

from quart import Quart
from wechaty import Message, WechatyPlugin, WechatyPluginOptions
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty_puppet import FileBox

from openai_api import *
from stable_diffusion_api import *

from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION, ALL_COMPLETED
import time

queue = Queue(1024)


async def deal_message(self: WechatyUIPlugin,  msg: Message):
    talker, room = msg.talker(), msg.room()
    if not talker.is_personal() or talker.get_id() == my_id or talker.name == "微信团队" or talker.name == "文件传输助手":
        return
    txt = msg.text()
    if txt in ["1", "2", "3", "4", "5", "6", "7"]:
        txt = quick_question[int(msg.text())-1]
        await msg.say("您的问题是："+txt + "\n请稍等，答案生成中")
    elif txt.startswith("画图"):
        is_allow = await get_moderation(txt)
        if is_allow == True:
            await msg.say("您的问题中可能包含敏感词汇，我不会做出任何回答。请您千万不要瞎搞搞啊！")
            return
        await msg.say("请稍等，图片生成大约要10秒。描述越详细，AI会更有目的性，画出来的图更好！\n以下是一个很好的参考 \n画图 照片，杰作，最佳质量，墙纸，4k，8k，高分辨率，1个女孩，白发，ahoge，长发，辫子，蓝眼睛，衬衫，毛衣，扫帚，城镇，建筑物，房屋，花朵，蝴蝶，阳光，阳光 斑纹，\n\n画图需要消耗巨量计算资源，高峰期处理不过来可能会吞消息。30秒内无回复请重新发送请求。短时间发送大量恶意请求，系统将会自动拉黑。")
        txt = await get_translation([txt[3:]])
        print(txt)
        await msg.say(FileBox.from_base64(await get_image(txt[3:]), name="you.png"))
        return

    reply = await get_response([txt])
    await msg.say(reply)
    await msg.say("请注意，我没有记忆，不会记住您前面的提问。每次请完整提问。要求越准确，我回答的越详细。我只支持文字。只知道2021年之前的事情")
    print(talker.name, "   ", txt)

    setting = self.get_setting()
    conv_id = room.room_id if room else talker.contact_id

    if conv_id not in setting.get('admin_ids', []):
        return

    await msg.forward(talker)


def on_message():
    try:
        while True:
            (self, msg) = queue.get()
            deal_message(self, msg)
            time.sleep(3)
    except Exception as e:
        print("\r" + e)


pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="on_message")
pool.submit(on_message)




class RepeaterPlugin(WechatyUIPlugin):
    global quick_question
    quick_question = ["如何在阳台种植草莓？",
                      "翻译一下“Ich bin ein intelligenter Assistent”",
                      "写一篇工作日报",
                      "帮我优化英文语法：“i like play game”",
                      "帮我创作一片散文，形容春天。不少于1000个字",
                      "我的电脑网络无法连接，该怎么办？",
                      "请帮我写一份应聘互联网工程师的简历。"]

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        queue.put((self, msg))
        message_controller.disable_all_plugins(msg)
