'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-04 17:32:25
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 12:00:37
FilePath: /server/app/utils/aes.py
'''
import base64
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np

AES_CHARS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X',
    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'w',
    'x', 'y', 'z', '2', '3', '4', '5', '6', '7', '8'
]


def encrypt(pwd: str, key: str):
    '''
    Author: 邵佳泓
    msg: 模拟SSO单点登录AES加密
    param {str} key
    param {str} aes_str
    '''
    regex = re.compile(r'(^\s+)|(\s+$)')
    key = regex.sub('', key)
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC,
                  ''.join(np.random.choice(AES_CHARS, size=16)).encode('utf-8'))
    pwd = ''.join(np.random.choice(AES_CHARS, size=64)) + pwd
    pad_pkcs7 = pad(pwd.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypt_aes = aes.encrypt(pad_pkcs7)
    encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8').replace("\n", "")
    return encrypt_text


def decrypt(key: str, encrypted_text: str):
    '''
    Author: 邵佳泓
    msg: AES解密
    param {str} key
    param {str} aes_str
    '''
    aes = AES.new(key[:32].encode('utf-8'), AES.MODE_ECB)
    decrypt_aes = aes.decrypt(base64.b64decode(encrypted_text.encode('utf-8')))
    decrypted_text = unpad(decrypt_aes, AES.block_size, style='pkcs7').decode('utf-8')
    return decrypted_text
