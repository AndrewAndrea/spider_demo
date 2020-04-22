# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
import base64
class aescrypt():
    def __init__(self,key,model,iv,encode_):
        self.encode_ = encode_
        self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
        self.key = self.add_16(key)
        if model == 'ECB':
            self.aes = AES.new(self.key,self.model) #创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key,self.model,iv) #创建一个aes对象

        #这里的密钥长度必须是16、24或32，目前16位的就够用了

    def add_16(self,par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self,text):
        text = self.add_16(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()

    def aesdecrypt(self,text):
        text = base64.decodebytes(text.encode(self.encode_))
        self.decrypt_text = self.aes.decrypt(text)
        return self.decrypt_text.decode(self.encode_).strip('\0')

if __name__ == '__main__':
    pr = aescrypt('12345','ECB','','gbk')
    en_text = pr.aesencrypt('好好学习')
    print('密文:',en_text)
    print('明文:',pr.aesdecrypt(en_text))

