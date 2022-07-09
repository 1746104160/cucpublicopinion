'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-09 17:13:47
FilePath: /server/app/managers/personal_manager/resetemail_manager.py
'''
import binascii
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, reqparse
from flask_restx.inputs import email, regex
from app.model import Users
from app.utils.redisdb import redis
from app.utils.limiter import limiter
from app.utils.aes import decrypt
from app.utils.ssoauth import loginsso
from app.managers.model import standardmodel as model

resetemail_ns = Namespace('resetemail', description='重置邮箱')
resetemail_ns.models[model.name] = model
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('account',
                    type=regex(pattern=r'\S{4,15}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='账号不能为空')
parser.add_argument('verify',
                    type=regex(pattern=r'\S{24}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='验证凭据不能为空')
parser.add_argument('email',
                    type=email(check=True),
                    location='json',
                    nullable=False,
                    required=True,
                    help='新的邮件地址不能为空')
parser.add_argument('emailcode',
                    type=regex(pattern=r'\S{6}$'),
                    location='json',
                    nullable=False,
                    required=True,
                    help='邮件验证码不能为空')
parser.add_argument('captcha',
                    type=regex(pattern=r'\S{4}$'),
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
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@resetemail_ns.route('')
@resetemail_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", model)
@resetemail_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", model)
@resetemail_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                        model)
class ResetEmail(Resource):
    '''
    Author: 邵佳泓
    msg: 修改邮箱
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @resetemail_ns.expect(parser)
    @resetemail_ns.marshal_with(model)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 修改邮箱
        param {*} self
        '''
        request_data = parser.parse_args()
        requestid = request_data.get('requestid')
        try:
            cucpassword = decrypt(requestid, request_data.get('verify'))
        except UnicodeDecodeError:
            return {'code': 1, 'message': 'CUC用户名或密码错误', 'success': False}
        except binascii.Error:
            return {'code': 1, 'message': 'CUC用户名或密码错误', 'success': False}
        except ValueError:
            return {'code': 1, 'message': 'CUC用户名或密码错误', 'success': False}
        account = request_data.get('account')
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
        elif not loginsso(account, cucpassword):
            return {'code': 6, 'message': 'CUC用户名或密码错误', 'success': False}
        else:
            user = Users.query.filter_by(userid=get_jwt_identity()).first()
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('userinfo')
            ]
            if Users.query.filter_by(cucaccount=account).first().userid != user.userid:
                return {'code': 7, 'message': '用户不匹配', 'success': False}
            else:
                Users.query.filter_by(userid=user.userid).update({'email': emailaddr})
                return {
                    'code': 0,
                    'message': '修改邮箱成功',
                    'success': True,
                }
