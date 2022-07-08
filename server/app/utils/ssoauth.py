'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 12:05:13
FilePath: /server/app/utils/ssoauth.py
'''
import re
from urllib.parse import quote
import requests
from .aes import encrypt


def loginsso(username: str, password: str) -> bool:
    '''
    Author: 邵佳泓
    msg: 使用中传SSO单点登录
    param {str} username
    param {str} password
    '''

    sess = requests.session()
    sess.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;' +
        'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'sso.cuc.edu.cn',
        'Origin': 'https://sso.cuc.edu.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://sso.cuc.edu.cn/authserver/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
        '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua': '.Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    login_html = sess.get("https://sso.cuc.edu.cn/authserver/login").text

    execution = re.findall(r'<input type="hidden" id="execution" name="execution" value="(.*)" />',
                           login_html)[0]
    salt = re.findall(r'<input type="hidden" id="pwdEncryptSalt" value="(.*)" /><input ',
                      login_html)[0]

    pwd = quote(encrypt(password, salt))

    url = "https://sso.cuc.edu.cn/authserver/login"

    payload = f'username={username}&password={pwd}' + \
        f'&captcha=&_eventId=submit&cllt=userNameLogin&dllt=generalLogin&lt=&execution={execution}'

    response = sess.request("POST", url, data=payload, allow_redirects=False)
    if 'Set-Cookie' in response.headers:
        return True
    else:
        return False
