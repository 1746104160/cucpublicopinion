'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-05 01:07:40
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-06 21:02:29
@FilePath: /server/app/utils/__init__.py
'''
from .aes import encrypt,decrypt
from .limiter import limiter
from .mail import mail
from .mysqldb import db
from .redisdb import redis
from .requestid import requestid
from .ssoauth import loginsso
from .default_avatar import blob