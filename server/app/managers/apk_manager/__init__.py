'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-14 14:40:45
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 14:43:48
FilePath: /server/app/managers/apk_manager/__init__.py
'''

from flask import Blueprint
from flask_restx import Api
from app.managers.apk_manager.qrcode_manager import qrcode_ns
apk = Blueprint("apk", __name__, url_prefix='/apk')
api = Api(apk, version='1.0', title='APK API',description='APK API',doc='/swagger/')
api.add_namespace(qrcode_ns,path='/qrcode')
