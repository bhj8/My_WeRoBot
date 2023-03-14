class mytxt	 :
    #示例
    welcometxt = """
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

    #模式说明
    panint_modeltxt= """遇到好看的画，请保存好（种子）和整段（提示词）的消息。
未来开通4k8k分辨率后，可以再次细绘该图。
种子绘高清图功能还在发开中！！！目前无法使用。但是您可以保存好种子，以便开放后绘制。"""

    #新用户关注
    newusertxt = """我是AI小慧，拥有全人类公开知识，擅长解答问题。
问我任何问题，我都会尽力回复你。你可以问我：
1."如何在阳台种植草莓？",
2."翻译一下“Ich bin ein intelligenter Assistent”",
3."写一篇工作日报",
4."帮我优化英文语法：“i like play game”",
5."帮我创作一片散文，形容春天。不少于1000个字",
6."我的电脑网络无法连接，该怎么办？",
7."请帮我写一份应聘互联网工程师的简历。"
输入数字快捷提问。

我也特别擅长根据你的题词，进行作画。
请输入："画图 女孩" 即可开始画图。

支持语音输入。请勿发送不雅词汇。
您作为新用户已自动获得100永久积分，可以免费使用。
任何时候都可以输入“帮助”查看帮助。
"""

    #开始生成图片
    start_paint_txt = f"""请稍等，图片生成大约要20秒。
输入“示例”查看优秀关键词,题词技巧。
输入“种子”查看种子说明。
全新画风！限时开启超高清模式，画面会更加完美，但是生成时间会更长。
高清图微信会自动压缩，请点开图片后在左下角点击“查看原图”查看高清原图。
本次作画画风为：真彩动漫 种子为：

小慧已经支持文字聊天了！！她能记住你最近说过的一些话，解答各种你的问题！
快试试！你甚至可以叫她帮你题词！
"""
    #快捷回复
    quick_question = ["如何在阳台种植草莓？",
                "翻译一下“Ich bin ein intelligenter Assistent”",
                "写一篇工作日报",
                "帮我优化英文语法：“i like play game”",
                "帮我创作一片散文，形容春天。不少于1000个字",
                "我的电脑网络无法连接，该怎么办？",
                "请帮我写一份应聘互联网工程师的简历。"]
    
    #帮助
    help_txt = """我是AI小慧，拥有全人类公开知识，擅长解答问题    
输入“邀请码”获得当前邀请码。
输入“积分”查看当前积分。
输入“示例”查看优秀关键词,题词技巧
"""

    #发送邀请码的文本
    invite_txt = """请复制后发送给好友，任意好友对小慧发送您的邀请码即可获得积分。每个好友只能使用一次邀请码"""


    #意外消息的文本
    unexpected_txt = """暂时小慧还理解不了您的表情和图片哦，您可以输入“帮助”查看帮助。
小慧以后会读懂表情和图片的，敬请期待！
后期还会支持照片修复、照片画图等功能哦！"""


    #画图 先文本
    first_txt = "masterpiece, best quality, ultra-detailed,  "
    #画图 后文本
    end_txt = ", foreground, middle ground, background, perspective, light, color, texture, detail, beauty, wonder,<lora:gachaSplashLORA_gachaSplashFarShot:0.6>"