import hashlib
import re
import time

from mytxt import mytxt


class utils :
    regex_paint = None
    invite_code_pattern = r"^id_[0-9a-fA-F]{8}$"
    bad_words_all = None
    @staticmethod
    def initialize():
        with open('badword_paint.txt', 'r', encoding='UTF-8') as f:
            bad_words_paint = [line.strip() for line in f]
        utils.regex_paint = r'\b\S*(' + '|'.join(bad_words_paint) + r')\S*\b'
        with open('badword.txt', 'r',encoding='UTF-8') as f:
            utils.bad_words_all = [line.strip() for line in f]
    
    def is_allow_paint_txt(txt: str):#判断是否允许出图
        if re.search(utils.regex_paint, txt, re.IGNORECASE) :
            return False
        return True
    def replace_badword_all(text):#全局屏蔽字
        return re.sub("|".join(utils.bad_words_all), "***", text)
    # 将字符串和当前时间的毫秒数作为种子
    def generate_seed(string):
        # 将当前时间的毫秒数转换为字符串，并追加到原始字符串后面
        string_with_time = string #+ str(int(round(time.time() * 1000)))
        
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
    # 将字符串和当前时间的毫秒数作为种子
    def get_friendkey(string):
        # 使用 SHA256 哈希函数计算输入字符串的哈希值
        h = hashlib.sha256(string.encode()).hexdigest()
        # 取哈希值前 8 位作为邀请码
        invite_code = h[:8]
        return "id" +invite_code
    # 检查邀请码是否合法
    def is_valid_invite_code(invite_code):
        return re.match(utils.invite_code_pattern, invite_code) is not None
    #替换快捷问题
    def replace_quick_question(txt: str):
        if txt in ["1", "2", "3", "4", "5", "6", "7"]:
            return mytxt.quick_question[int(txt)-1]
        return txt