import asyncio
import os

import openai
from dotenv import load_dotenv

load_dotenv()
#openai.organization = "org-FJzlkB2FVUgCd3naiH46NQT2"
openai.api_key = os.getenv("OPENAI_API_KEY")
# Set up the OpenAI API parameters for the conversation model

async def get_moderation(imessage: str):#是否有不当内容  True 有不当内容
  moderation = await openai.Moderation.acreate(
  input=imessage,
  )
  return moderation.results[0].flagged

#进来的list的排序从最旧到最新
def prepare_message(last_messages: list = []):
  old_message = ""
  if len(last_messages) == 0: return []
  messages=[
    {"role": "system", "content": "你是一个叫小慧个人的助手。"}]
  token = 0
  for i in range(len(last_messages)-1):
    old_message = last_messages[i] + "\n"    
    token = token + len(last_messages[i])
    if token > 200:      
      break
  messages.append({"role": "user", "content":"以下我之前和你说过的话："+ old_message})
  messages.append({"role": "assistant", "content": "好的，我知道了。"})
  messages.append({"role": "user", "content": last_messages[-1]})
  return messages


async def get_chat_response(last_messages: list = [])->str:
  completions = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    #temperature = 0.5,
    presence_penalty = 1,
    #frequency_penalty = 0.5,

    top_p = 0.2,     
    #n = 1,
    #stream = False,
    #stop =" ",# [ " User:", " Assistant:"],
    max_tokens = 500,
    messages=prepare_message(last_messages),
    
  )
  # Return the response
  return [completions.choices[0].message.content.strip(),completions.usage.total_tokens]


      # messages=[
      #     {"role": "system", "content": "You are a talking Tommy cat."},
      #     {"role": "user", "content": "Please play a talking Tommy cat and chat with child.please say yes if you can"},#You can briefly decline to answer uncomfortable questions.
      #     {"role": "assistant", "content": "yes"},
      #     # {"role": "user", "content": "Who are you?"},
      #     # {"role": "assistant", "content": "i am talking tom cat."},
      #     {"role": "user", "content": "请帮我翻译以下英文，谢谢"},
      #     {"role": "assistant", "content": "好的，请你告诉我要翻译的内容"},
      # ]
async def get_translation(last_messages: list = []):
  completions = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    presence_penalty = 0,
    top_p = 0.2, 
    messages=[
        # {"role": "system", "content": "you are a translator."},
        # {"role": "user", "content": "Please translate the content I send you into English."},
        # {"role": "assistant", "content": "yes"},
        {"role": "user", "content": "Translate the following Chinese text to English: "+last_messages[0]},
        
    ]    
  )
  # Return the response
  return completions.choices[0].message.content.strip()

if __name__ == "__main__":
  openai.proxy=  {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
}
  # print(asyncio.run(get_translation(["一个美少女,jk,金色头发,带着眼镜"])))
  print(asyncio.run(get_chat_response(["你好","武汉好还是杭州好","最火的抖音音乐"])))
  # print(asyncio.run(get_moderation(["审核能力测试"])))
# 处理生成的文本输出
#print(message)


