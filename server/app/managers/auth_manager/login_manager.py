'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 12:51:20
FilePath: /server/app/managers/auth_manager/login_manager.py
'''
import binascii
import datetime
from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended.utils import create_access_token
from sqlalchemy import or_
from app.utils.redisdb import redis
from app.utils.mysqldb import db
from app.model import Users
from app.utils.limiter import limiter
from app.utils.aes import decrypt

login_ns = Namespace('login', description='登录')
data_model = login_ns.model('logindata', {
    "accessToken": fields.String(required=True, description='accessToken'),
})
model = login_ns.model(
    'login', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(data_model, description='数据')
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('account',
                    type=str,
                    location='json',
                    nullable=False,
                    required=True,
                    help='账号不能为空')
parser.add_argument('password',
                    type=str,
                    location='json',
                    nullable=False,
                    required=True,
                    help='密码不能为空')
parser.add_argument('captcha',
                    type=str,
                    location='json',
                    nullable=False,
                    required=True,
                    help='验证码不能为空')
parser.add_argument('requestid', type=str, location='cookies', nullable=False, help='会话开始id')
parser.add_argument('X-CSRFToken',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='csrf_token不能为空')


@login_ns.route('')
@login_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@login_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@login_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class LoginSystem(Resource):
    '''
    Author: 邵佳泓
    msg: 登录系统账号
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @login_ns.expect(parser)
    @login_ns.marshal_with(model)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 登录系统账号
        param {*} self
        '''
        request_data = parser.parse_args()
        requestid = request_data.get('requestid')
        try:
            password = decrypt(requestid, request_data.get('password'))
        except UnicodeDecodeError:
            return {'code': 1, 'message': '用户名或密码错误', 'success': False}
        except binascii.Error:
            return {'code': 1, 'message': '用户名或密码错误', 'success': False}
        except ValueError:
            return {'code': 1, 'message': '用户名或密码错误', 'success': False}
        account = request_data.get('account')
        captcha = request_data.get('captcha')

        code = redis.get("captcha/" + requestid)
        if code is None:
            return {'code': 2, 'message': '验证码已失效', 'success': False}
        elif code.decode('utf-8').lower() != captcha.lower():
            return {'code': 3, 'message': '验证码错误', 'success': False}
        else:
            user = Users.query.filter(or_(Users.name == account, Users.email == account)).first()
            if user is None:
                return {'code': 4, 'message': '用户名或密码错误', 'success': False}
            elif not user.check_password(password=password):
                return {'code': 5, 'message': '用户名或密码错误', 'success': False}
            else:
                user.last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user.last_login_ip = request.remote_addr
                db.session.commit()
                token = create_access_token(identity=user.userid,
                                            expires_delta=datetime.timedelta(days=1))
                return {
                    'code': 0,
                    'message': '登录成功',
                    'data': {
                        'accessToken': token,
                    },
                    'success': True,
                }
