
import asyncio
import io
import os
import tempfile

import webuiapi

import mytxt


# create API client
#api = webuiapi.WebUIApi()
class SDapi:
    def __init__(self,host='127.0.0.1', port=7860,*args,**kwargs):
        self.host = host
        self.port = port
        self.api = webuiapi.WebUIApi(host=self.host, port=self.port, use_https=False)
        self.first_txt = "masterpiece, best quality, ultra-detailed,  "
        self.end_txt = ", foreground, middle ground, background, perspective, light, color, texture, detail, beauty, wonder,<lora:gachaSplashLORA_gachaSplashFarShot:0.6>"#,<lora:gachaSplashLORA_gachaSplashFarShot:1>
        self.ban_txt= "nsfw,worst quality, low quality:1.4), (depth of field, blurry:1.2), (greyscale, monochrome:1.1), extra fingers,fewer fingers, extra legs, extra hands,3D face, cropped, lowres, text, jpeg artifacts, signature, watermark, username, blurry, artist name, trademark, watermark, title, multiple view, Reference sheet, curvy,  plump, fat, muscular female, strabismus,bad feet,glans,nipples,nsfw,NSFW,"
        # self.api.set_auth('bao', '123')

    # create API client with custom host, port
    

    # create API client with custom host, port and https
    # api = webuiapi.WebUIApi(host='https://5c2a0775-930e-4f2c.gradio.live', port=443, use_https=True)

    # create API client with default sampler, steps.
    #api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

    def handle_prompt(self,prompt):
        prompt= self.first_txt + prompt + self.end_txt
        return prompt

    async def get_image(self,prompt:str,seed:int):
        result1 = None
        result1 = self.api.txt2img(prompt=self.handle_prompt(prompt),#"cute squirrel"
                            negative_prompt=self.ban_txt,
                            seed=seed,
                            styles=[],
                            cfg_scale=8,
                            width=512,
                            height=832,
                            sampler_index="DMP++ SDE Karras", #'DPM++2M Karras'
                            steps=20,
                            enable_hr=True,
                            hr_scale=1.5,
                            hr_upscaler=webuiapi.HiResUpscaler.Latent,
                            hr_second_pass_steps=15,
                            hr_resize_x=768,
                            hr_resize_y=1248,
                            denoising_strength=0.5,
                            restore_faces = True,
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
    sdapi = SDapi()
    asyncio.run(sdapi.get_image("cute squirrel",196414898))