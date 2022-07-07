'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-06 22:49:05
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 01:09:10
@FilePath: /server/app/managers/personal_manager/__init__.py
'''
from flask import Blueprint
from flask_restx import Api
from app.managers.personal_manager.updateinfo_manager import update_ns
from app.managers.personal_manager.uploadavatar_manager import upload_ns
from app.managers.personal_manager.resetemail_manager import resetemail_ns
from app.managers.personal_manager.resetpw_manager import resetpw_ns
from app.managers.personal_manager.resetsso_manager import resetsso_ns
personal = Blueprint("personal", __name__, url_prefix='/personal/user')
api = Api(personal, version='1.0', title='Personal API',description='Personal API',doc='/swagger/')
api.add_namespace(update_ns, path='/update')
api.add_namespace(upload_ns, path='/upload')
api.add_namespace(resetemail_ns, path='/resetemail')
api.add_namespace(resetpw_ns, path='/resetpw')
api.add_namespace(resetsso_ns, path='/resetsso')