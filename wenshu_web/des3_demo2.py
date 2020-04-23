# -*- coding: utf-8 -*-

from Crypto.Cipher import DES3

import base64

BS = DES3.block_size
import json
import requests


def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


# 定义 padding 即 填充 为PKCS7

def unpad(s):
    return s[0:-ord(s[-1])]


class prpcrypt():
    def __init__(self, key, IV):
        self.key = key
        self.mode = DES3.MODE_CBC
        self.iv = IV.encode('utf8')

    # DES3的加密模式为CBC
    def encrypt(self, text):
        text = pad(text)
        cryptor = DES3.new(self.key, self.mode, self.iv)
        # self.iv 为 IV 即偏移量
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        # print(text)
        self.ciphertext = cryptor.encrypt(text.encode('utf8'))
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = DES3.new(self.key, self.mode, self.iv)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = unpad(st)
        return out
        # 上面注释内容解密如果运行报错，就注释掉试试
        # return plain_text
