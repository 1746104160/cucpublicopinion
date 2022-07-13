'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 10:53:28
FilePath: /server/app/managers/auth_manager/register_manager.py
'''
import binascii
import datetime
from http import HTTPStatus
import re
from flask_restx import Namespace, Resource, reqparse
from flask_restx.inputs import regex,email
from app.utils.redisdb import redis
from app.model import Users, Roles
from app.utils.limiter import limiter
from app.utils.aes import decrypt
from app.utils.ssoauth import loginsso
from app.managers.model import standardmodel as model
register_ns = Namespace('register', description='注册')
register_ns.models[model.name] = model
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username',
                    type=regex(pattern=r'^[a-zA-Z][a-zA-Z0-9_]{5,15}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='用户名不能为空')
parser.add_argument('password',
                    type=regex(pattern=r'\S{24}'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='密码不能为空')
parser.add_argument('email',
                    type=email(check=True),
                    location='json',
                    nullable=False,
                    required=True,
                    help='邮箱不能为空')
parser.add_argument('emailcode',
                    type=regex(pattern=r'\S{6}'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='邮件验证码不能为空')
parser.add_argument('captcha',
                    type=regex(pattern=r'\S{4}'),
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


@register_ns.route('/systemaccount')
@register_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", model)
@register_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", model)
@register_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", model)
class RegisterSystem(Resource):
    '''
    Author: 邵佳泓
    msg: 注册系统账号
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @register_ns.expect(parser)
    @register_ns.marshal_with(model)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 注册系统账号
        param {*} self
        '''
        request_data = parser.parse_args()
        requestid = request_data.get('requestid')
        try:
            password = decrypt(requestid, request_data.get('password'))
        except UnicodeDecodeError:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        except binascii.Error:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        except ValueError:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        username = request_data.get('username')
        captcha = request_data.get('captcha')
        emailaddr = request_data.get('email')
        emailcode = request_data.get('emailcode')
        code = redis.get("captcha/" + requestid)
        redisemail = redis.get('/'.join(["email", requestid, emailaddr]))
        if code is None:
            return {'code': 2, 'message': '验证码已失效', 'success': False}
        elif code.decode('utf-8').lower() != captcha.lower():
            return {'code': 3, 'message': '验证码错误', 'success': False}
        elif redisemail is None:
            return {'code': 4, 'message': '邮件验证码已失效', 'success': False}
        elif redisemail.decode('utf-8') != emailcode:
            return {'code': 5, 'message': '邮件验证码错误', 'success': False}
        else:
            if Users.query.filter_by(name=username).first():
                return {'code': 8, 'message': '用户名已注册', 'success': False}
            else:
                standard = Roles.query.filter_by(name='standard').first()
                user = Users(name=username,
                             email=emailaddr,
                             role=[standard],
                             created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                user.set_password(password)
                [
                    redis.delete(key) for key in redis.keys('userinfo/desc/*')
                ]
                Users.add(user)
                return {'code': 0, 'message': '注册成功', 'success': True}


ssoparser = reqparse.RequestParser(bundle_errors=True)
ssoparser.add_argument('username',
                       type=regex(pattern=r'\d{4,15}'),
                       location='json',
                       nullable=False,
                       required=True,
                       help='用户名不能为空')
ssoparser.add_argument('password',
                       type=regex(pattern=r'\S{24}'),
                       location='json',
                       nullable=False,
                       required=True,
                       help='密码不能为空')
ssoparser.add_argument('captcha',
                       type=regex(pattern=r'\S{4}'),
                       location='json',
                       nullable=False,
                       required=True,
                       help='验证码不能为空')
ssoparser.add_argument('requestid',
                       type=str,
                       location='cookies',
                       nullable=False,
                       required=True,
                       help='requestid不能为空')
ssoparser.add_argument('X-CSRFToken',
                       type=str,
                       location='headers',
                       nullable=False,
                       required=True,
                       help='csrf_token不能为空')


@register_ns.route('/cucaccount')
@register_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", model)
@register_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", model)
@register_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", model)
class RegisterSSO(Resource):
    '''
    Author: 邵佳泓
    msg: 利用中传账号注册
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @register_ns.expect(ssoparser)
    @register_ns.marshal_with(model)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 利用中传账号注册
        param {*} self
        '''
        request_data = ssoparser.parse_args()
        requestid = request_data.get('requestid')
        try:
            password = decrypt(requestid, request_data.get('password'))
        except UnicodeDecodeError:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        except binascii.Error:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        except ValueError:
            return {'code': 1, 'message': '密码不符合要求', 'success': False}
        username = request_data.get('username')
        captcha = request_data.get('captcha')
        code = redis.get("captcha/" + requestid)
        if code is None:
            return {'code': 2, 'message': '验证码已失效', 'success': False}
        elif code.decode('utf-8').lower() != captcha.lower():
            return {'code': 3, 'message': '验证码错误', 'success': False}
        elif not re.match(r"^\d{4,}$", username):
            return {'code': 4, 'message': '用户名或密码错误', 'success': False}
        elif not loginsso(username, password):
            return {'code': 5, 'message': '用户名或密码错误', 'success': False}
        elif Users.query.filter_by(name=username).first():
            return {'code': 6, 'message': '用户已注册', 'success': False}
        else:
            standard = Roles.query.filter_by(name='standard').first()
            user = Users(name=username,
                         email=username + '@cuc.edu.cn',
                         cucaccount=username,
                         role=[standard],
                         created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            user.set_password(password)
            [
                redis.delete(key) for key in redis.keys('userinfo/desc/*')
            ]
            Users.add(user)
            return {'code': 0, 'message': '注册成功', 'success': True}
