'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-06 21:01:55
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-06 21:02:11
@FilePath: /server/app/utils/default_avatar.py
'''
from PIL import Image
import io
image = Image.open('avatar-default.png')
image_byte = io.BytesIO()
image.save(image_byte, 'png')
blob = image_byte.getvalue()