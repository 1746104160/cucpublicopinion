'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-09 12:28:20
FilePath: /server/app/managers/auth_manager/resetpw_manager.py
'''
import binascii
from http import HTTPStatus
from flask_restx import Namespace, Resource, reqparse
from flask_restx.inputs import regex,email
from app.utils.redisdb import redis
from app.utils.mysqldb import db
from app.model import Users
from app.utils.limiter import limiter
from app.utils.aes import decrypt
from app.managers.model import standardmodel as model
resetpw_ns = Namespace('resetpw', description='重置密码')
resetpw_ns.models[model.name] = model
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('email',
                    type=email(check=True),
                    location='json',
                    nullable=False,
                    required=True,
                    help='邮箱不能为空')
parser.add_argument('emailcode',
                    type=regex(r'^\S{6}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='邮件验证码不能为空')
parser.add_argument('password',
                    type=regex(r'^\S{24}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='密码不能为空')
parser.add_argument('captcha',
                    type=regex(r'^\S{4}$'),
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


@resetpw_ns.route('')
@resetpw_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", model)
@resetpw_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", model)
@resetpw_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", model)
class ResetPW(Resource):
    '''
    Author: 邵佳泓
    msg: 修改密码
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @resetpw_ns.expect(parser)
    @resetpw_ns.marshal_with(model)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 修改密码
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
        emailaddr = request_data.get('email')
        emailcode = request_data.get('emailcode')
        captcha = request_data.get('captcha')
        redisemail = redis.get('/'.join(["email", requestid, emailaddr]))
        code = redis.get("captcha/" + requestid)
        if code is None:
            return {'code': 2, 'message': '验证码已失效', 'success': False}
        elif code.decode('utf-8').lower() != captcha.lower():
            return {'code': 3, 'message': '验证码错误', 'success': False}
        elif redisemail is None:
            return {'code': 4, 'message': '邮件验证码已失效', 'success': False}
        elif redisemail.decode('utf-8') != emailcode:
            return {'code': 5, 'message': '邮件验证码错误', 'success': False}
        else:
            user = Users.query.filter_by(email=emailaddr).first()
            if user is None:
                return {'code': 6, 'message': '用户未注册', 'success': False}
            else:
                user.set_password(password)
                db.session.commit()
                return {
                    'code': 0,
                    'message': '修改密码成功',
                    'success': True,
                }
