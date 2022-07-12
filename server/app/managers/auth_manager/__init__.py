'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:50:55
LastEditors: 邵佳泓
LastEditTime: 2022-07-12 22:12:11
FilePath: /server/app/managers/auth_manager/__init__.py
'''
from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended.exceptions import JWTExtendedException
from app.managers.auth_manager.captcha_manager import captcha_ns
from app.managers.auth_manager.email_manager import email_ns
from app.managers.auth_manager.login_manager import login_ns
from app.managers.auth_manager.register_manager import register_ns
from app.managers.auth_manager.resetpw_manager import resetpw_ns
from app.managers.auth_manager.userinfo_manager import userinfo_ns
from app.managers.auth_manager.logout_manager import logout_ns
auth = Blueprint("auth", __name__, url_prefix='/auth/user')
api = Api(auth, version='1.0', title='Auth API',description='Auth API',doc='/swagger/')
api.add_namespace(captcha_ns, path='/captcha')
api.add_namespace(email_ns, path='/email')
api.add_namespace(login_ns, path='/login')
api.add_namespace(register_ns, path='/register')
api.add_namespace(resetpw_ns, path='/resetpw')
api.add_namespace(userinfo_ns, path='/userinfo')
api.add_namespace(logout_ns, path='/logout')
@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    """
    If the error is a JWT error, return a 401 response with the error message
    :param error: The error that was raised
    """
    return {'message': str(error)}, getattr(error, 'code', 401)
