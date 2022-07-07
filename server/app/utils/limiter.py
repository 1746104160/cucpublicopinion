'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-04 16:24:01
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-04 16:40:47
@FilePath: /server/app/utils/limiter.py
'''

import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address,
				  storage_uri=os.environ['REDIS_URL'])
