'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-07 01:41:28
LastEditors: 邵佳泓
LastEditTime: 2022-07-12 22:29:30
FilePath: /server/app/managers/visualize_manager/__init__.py
'''
from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended.exceptions import JWTExtendedException
from app.managers.admin_manager.user_manager import user_ns
from app.managers.admin_manager.role_manager import role_ns
from app.managers.admin_manager.news_manager import news_ns
from app.managers.admin_manager.security_manager import security_ns
from app.managers.admin_manager.log_manager import log_ns
admin = Blueprint("admin", __name__, url_prefix='/admin')
api = Api(admin, version='1.0', title='Admin API',description='Admin API',doc='/swagger/')
api.add_namespace(user_ns,path='/user')
api.add_namespace(role_ns,path='/role')
api.add_namespace(news_ns,path='/news')
api.add_namespace(security_ns,path='/security')
api.add_namespace(log_ns,path='/log')
@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    """
    If the error is a JWT error, return a 401 response with the error message
    :param error: The error that was raised
    """
    return {'message': str(error)}, getattr(error, 'code', 401)