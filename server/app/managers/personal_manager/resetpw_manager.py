'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 22:24:36
@FilePath: /server/app/managers/personal_manager/resetpw_manager.py
'''
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.redisdb import redis
from app.utils.mysqldb import db
from flask_restx import Namespace, Resource, reqparse
from app.model import Users
from app.utils.limiter import limiter
from app.utils.aes import decrypt
from app.utils.ssoauth import loginsso
from app.managers.personal_manager.model import model
resetpw_ns = Namespace('resetpw', description='重置密码')
resetpw_ns.models[model.name] = model
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('account', type=str, location='json', nullable=False, required=True, help='账号不能为空')
parser.add_argument('mode', type=str, location='json', nullable=False, required=True, help='验证方式不能为空')
parser.add_argument('verify', type=str, location='json', nullable=False, required=True, help='验证凭据不能为空')
parser.add_argument('password', type=str, location='json', nullable=False, required=True, help='新的密码不能为空')
parser.add_argument('captcha', type=str, location='json', nullable=False, required=True, help='验证码不能为空')
parser.add_argument('requestid', type=str, location='cookies', nullable=False, help='会话开始id')
parser.add_argument('X-CSRFToken', type=str, location='headers', nullable=False, required=True, help='csrf_token不能为空')


@resetpw_ns.route('')
@resetpw_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@resetpw_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@resetpw_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class ResetPW(Resource):
    '''
    Author: 邵佳泓
    msg: 修改密码
    '''
    decorators = [
        limiter.limit('3/minute'),
        limiter.limit('50/day')
    ]

    @resetpw_ns.expect(parser)
    @resetpw_ns.marshal_with(model)
    @jwt_required()
    def post(self):
        request_data = parser.parse_args()
        requestid = request_data.get('requestid')
        try:
            password = decrypt(requestid, request_data.get('password'))
        except Exception as e:
            return {
                'code': 1,
                'message': '密码不符合要求',
                'success': False
            }
        mode = request_data.get('mode')
        if mode == 'email':
            account = request_data.get('account')
            emailcode = request_data.get('verify')
            captcha = request_data.get('captcha')
            redisemail = redis.get('/'.join(["email", requestid, account]))
            code = redis.get("captcha/" + requestid)
            if code is None:
                return {
                    'code': 2,
                    'message': '验证码已失效',
                    'success': False
                }
            elif code.decode('utf-8').lower() != captcha.lower():
                return {
                    'code': 3,
                    'message': '验证码错误',
                    'success': False
                }
            elif redisemail is None:
                return {
                    'code': 4,
                    'message': '邮件验证码已失效',
                    'success': False
                }
            elif redisemail.decode('utf-8') != emailcode:
                return {
                    'code': 5,
                    'message': '邮件验证码错误',
                    'success': False
                }
            else:
                user = Users.query.filter_by(userid=get_jwt_identity()).first()
                if Users.query.filter_by(email=account).first().userid != user.userid:
                    return {
                        'code': 6,
                        'message': '用户不匹配',
                        'success': False
                    }
                else:
                    user.set_password(password)
                    db.session.commit()
                    return {
                        'code': 0,
                        'message': '修改密码成功',
                        'success': True,
                    }
        else:
            account = request_data.get('account')
            try:
                cucpassword = decrypt(requestid, request_data.get('verify'))
            except Exception as e:
                return {
                    'code': 2,
                    'message': '密码不符合要求',
                    'success': False
                }
            captcha = request_data.get('captcha')
            code = redis.get("captcha/" + requestid)
            if code is None:
                return {
                    'code': 3,
                    'message': '验证码已失效',
                    'success': False
                }
            elif code.decode('utf-8').lower() != captcha.lower():
                return {
                    'code': 4,
                    'message': '验证码错误',
                    'success': False
                }
            elif not loginsso(account, cucpassword):
                return {
                    'code': 5,
                    'message': '中传SSO登录失败',
                    'success': False
                }
            else:
                user = Users.query.filter_by(userid=get_jwt_identity()).first()
                if Users.query.filter_by(cucaccount=account).first().userid != user.userid:
                    return {
                        'code': 6,
                        'message': '用户不匹配',
                        'success': False
                    }
                else:
                    user.set_password(password)
                    db.session.commit()
                    return {
                        'code': 0,
                        'message': '修改密码成功',
                        'success': True,
                    }
