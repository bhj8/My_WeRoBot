import asyncio
import io
import os
import tempfile

import webuiapi

# create API client
#api = webuiapi.WebUIApi()

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
api_url = "127.0.0.1:7860"

# create API client with custom host, port and https
# api = webuiapi.WebUIApi(host='https://5c2a0775-930e-4f2c.gradio.live', port=443, use_https=True)

# create API client with default sampler, steps.
#api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

# optionally set username, password when --api-auth is set on webui.
# api.set_auth('username', 'password')
first_txt = " <(masterpiece, realistic:1.3), (extremely intricate:1.2)>,  "
end_txt = ",looking at viewer"
ban_txt= ", bad feet,glans, nsfw, nipples,underwear, panties"
def handle_prompt(prompt):
    prompt= first_txt + prompt + end_txt
    print(prompt)
    return prompt

async def get_image(prompt:str):
    result1 = None
    result1 = api.txt2img(prompt=handle_prompt(prompt),#"cute squirrel"
                        negative_prompt="""((worst quality, low quality:1.4), (depth of field, blurry:1.2), (greyscale, monochrome:1.1), extra fingers,fewer fingers, extra legs, extra hands,3D face, cropped, lowres, text, jpeg artifacts, signature, watermark, username, blurry, artist name, trademark, watermark, title, multiple view, Reference sheet, curvy, plump, fat, muscular female, strabismus,"""+ban_txt,
                        seed=-1,
                        styles=[],
                        cfg_scale=15,
                        width=512,
                        height=768,
                        sampler_index='DPM++2M Karras',
                        steps=38,
                        #  enable_hr=True,
                        #  hr_scale=2,
                        #  hr_upscaler=webuiapi.HiResUpscaler.Latent,
                        #  hr_second_pass_steps=20,
                        #  hr_resize_x=512,
                        #  hr_resize_y=512,
                        #  denoising_strength=0.4,

                        )
    # images contains the returned images (PIL images)

    #这里很有问题啊！！！！！！！因为还没画好，我也不知道怎么办？先这样弄一下好了。
    time = 0
    while result1 is None:
        time += 1
        if time > 30:
            return None
        await asyncio.sleep(1)
    
    save_path = os.path.join(os.getcwd(), 'images')
    # 创建保存文件的文件夹
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, str(result1.info["seed"]) + ".png")
    result1.image.save(save_file)
    return [save_file,result1.info]

# result1.images
# import requests

# # 设置API地址
# api_url = "http://localhost:7860"

# # 获取可用检查点列表
# response = requests.get(f"{api_url}/sdapi/v1/availablecheckpoints")
# checkpoints = response.json()
# print("Available checkpoints:", checkpoints)

# # 设置当前检查点
# checkpoint_to_set = checkpoints[1] 
# response = requests.post(f"{api_url}/sdapi/v1/checkpoint", json={"checkpoint": checkpoint_to_set})
# print("Response:", response.text)
# result1.image
if __name__ == '__main__':
    asyncio.run(get_image("cute squirrel"))