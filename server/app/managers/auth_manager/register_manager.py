'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 23:11:41
@FilePath: /server/app/managers/auth_manager/register_manager.py
'''
import datetime
from http import HTTPStatus

from app.utils.redisdb import redis
from flask_restx import Namespace, Resource, fields, reqparse
import re
from app.model import Users, Roles
from app.utils.limiter import limiter
from app.utils.aes import decrypt
from app.utils.ssoauth import loginsso
register_ns = Namespace('register', description='注册')
model = register_ns.model('register', {
	'code': fields.Integer(required=True, description='状态码'),
	'message': fields.String(required=True, description='状态信息'),
	'success': fields.Boolean(required=True, description='是否成功'),
})
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, location='json', nullable=False, required=True, help='用户名不能为空')
parser.add_argument('password', type=str, location='json', nullable=False, required=True, help='密码不能为空')
parser.add_argument('email', type=str, location='json', nullable=False, required=True, help='邮箱不能为空')
parser.add_argument('emailcode', type=str, location='json', nullable=False, required=True, help='邮件验证码不能为空')
parser.add_argument('captcha', type=str, location='json', nullable=False, required=True, help='验证码不能为空')
parser.add_argument('requestid', type=str, location='cookies', nullable=False, help='会话开始id')
parser.add_argument('X-CSRFToken', type=str, location='headers', nullable=False, required=True, help='csrf_token不能为空')


@register_ns.route('/systemaccount')
@register_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@register_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@register_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class registerSystem(Resource):
	'''
	@Author: 邵佳泓
	@msg: 注册系统账号
	'''
	decorators = [
		limiter.limit('3/minute'),
		limiter.limit('50/day')
	]

	@register_ns.expect(parser)
	@register_ns.marshal_with(model)
	def post(self):
		request_data = parser.parse_args()
		requestid = request_data.get('requestid')
		try:
			password = decrypt(requestid, request_data.get('password'))
		except:
			return {
				'code': 1,
				'message': '密码不符合要求',
				'success': False
			}
		username = request_data.get('username')
		captcha = request_data.get('captcha')
		email = request_data.get('email')
		emailcode = request_data.get('emailcode')
		code = redis.get("captcha/" + requestid)
		redisemail = redis.get('/'.join(["email", requestid, email]))
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
		elif len(username) < 6 or len(username) > 16:
			return {
				'code': 6,
				'message': '用户名需要在6-16位之间',
				'success': False
			}
		elif not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{5,15}$", username):
			return {
				'code': 7,
				'message': '用户名需要以字母开头，只能包含字母、数字和下划线',
				'success': False
			}
		else:
			if Users.query.filter_by(name=username).first():
				return {
					'code': 8,
					'message': '用户名已注册',
					'success': False
				}
			else:
				standard = Roles.query.filter_by(name='standard').first()
				user = Users(name=username,
									email=email,
									role=[standard],
									created_on=datetime.datetime.now().strftime(
										"%Y-%m-%d %H:%M:%S"),
									last_login=datetime.datetime.now().strftime(
										"%Y-%m-%d %H:%M:%S"))
				user.set_password(password)
				[redis.delete(key) for key in redis.keys() if key.decode('utf-8').startswith('userinfo/desc')]
				Users.add(user)
				return {
					'code': 0,
					'message': '注册成功',
					'success': True
				}


ssoparser = reqparse.RequestParser(bundle_errors=True)
ssoparser.add_argument('username', type=str, location='json', nullable=False, required=True, help='用户名不能为空')
ssoparser.add_argument('password', type=str, location='json', nullable=False, required=True, help='密码不能为空')
ssoparser.add_argument('captcha', type=str, location='json', nullable=False, required=True, help='验证码不能为空')
ssoparser.add_argument('requestid', type=str, location='cookies', nullable=False, required=True, help='requestid不能为空')
ssoparser.add_argument('X-CSRFToken', type=str, location='headers', nullable=False, required=True, help='csrf_token不能为空')


@register_ns.route('/cucaccount')
@register_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@register_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@register_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class RegisterSSO(Resource):
	'''
	@Author: 邵佳泓
	@msg: 登录系统账号
	'''
	decorators = [
		limiter.limit('3/minute'),
		limiter.limit('50/day')
	]

	@register_ns.expect(ssoparser)
	@register_ns.marshal_with(model)
	def post(self):
		request_data = ssoparser.parse_args()
		requestid = request_data.get('requestid')
		try:
			password = decrypt(requestid, request_data.get('password'))
		except:
			return {
				'code': 1,
				'message': '用户名或密码错误',
				'success': False
			}
		username = request_data.get('username')
		captcha = request_data.get('captcha')
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
		elif not re.match(r"^\d{4,}$", username):
			return {
				'code': 4,
				'message': '用户名或密码错误',
				'success': False
			}
		elif not loginsso(username, password):
			return {
				'code': 5,
				'message': '用户名或密码错误',
				'success': False
			}
		elif Users.query.filter_by(name=username).first():
			return {
				'code': 6,
				'message': '用户已注册',
				'success': False
			}
		else:
			standard = Roles.query.filter_by(name='standard').first()
			user = Users(name=username,
							email=username+'@cuc.edu.cn',
							cucaccount=username,
							role=[standard],
							created_on=datetime.datetime.now().strftime(
								"%Y-%m-%d %H:%M:%S"),
							last_login=datetime.datetime.now().strftime(
								"%Y-%m-%d %H:%M:%S"))
			user.set_password(password)
			[redis.delete(key) for key in redis.keys() if key.decode('utf-8').startswith('userinfo/desc')]
			Users.add(user)
			return {
				'code': 0,
				'message': '注册成功',
				'success': True
			}