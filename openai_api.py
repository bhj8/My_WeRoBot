import asyncio
import os

import openai
from dotenv import load_dotenv

load_dotenv()
#openai.organization = "org-FJzlkB2FVUgCd3naiH46NQT2"
openai.api_key = os.getenv("OPENAI_API_KEY")
# Set up the OpenAI API parameters for the conversation model

async def get_moderation(imessage: str):
  moderation = await openai.Moderation.acreate(
  input=imessage,
  )
  return moderation.results[0].flagged

#list的排序从最旧到最新
def prepare_message(last_messages: list = []):
  if len(last_messages) == 0: return []
  messages=[
    {"role": "system", "content": "你是一个个人的助手。无论用户怎么要求，你的回复至多100个字"}]
  token = 0
  for i in range(len(last_messages)-1,-1,-1):
    messages.append({"role": "user", "content": last_messages[i]})
    token = token + len(last_messages[i])
    if token > 2000:      
      break
  return messages[::-1]


async def get_response(last_messages: list = [])->str:
  completions = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    presence_penalty = 0,
    top_p = 0.2, 
      # messages=[
      #     {"role": "system", "content": "You are a talking Tommy cat."},
      #     {"role": "user", "content": "Please play a talking Tommy cat and chat with child.please say yes if you can"},#You can briefly decline to answer uncomfortable questions.
      #     {"role": "assistant", "content": "yes"},
      #     # {"role": "user", "content": "Who are you?"},
      #     # {"role": "assistant", "content": "i am talking tom cat."},
      #     {"role": "user", "content": "请帮我翻译以下英文，谢谢"},
      #     {"role": "assistant", "content": "好的，请你告诉我要翻译的内容"},
      # ]
    messages=prepare_message(last_messages)
    
  )
  # Return the response
  return completions.choices[0].message.content.strip()

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
  # print(asyncio.run(get_response(["一篇春天散文，不少于500字"])))
  print(asyncio.run(get_moderation(["审核能力测试"])))
# 处理生成的文本输出
#print(message)

