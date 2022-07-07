'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-07 01:41:28
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 23:24:16
@FilePath: /server/app/managers/admin_manager/__init__.py
'''
from flask import Blueprint
from flask_restx import Api
from app.managers.admin_manager.user_manager import user_ns
from app.managers.admin_manager.role_manager import role_ns
admin = Blueprint("admin", __name__, url_prefix='/admin')
api = Api(admin, version='1.0', title='Admin API',description='Admin API',doc='/swagger/')
api.add_namespace(user_ns,path='/user')
api.add_namespace(role_ns,path='/role')
