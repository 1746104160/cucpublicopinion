'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 00:47:20
@FilePath: /server/app/managers/auth_manager/resetpw_manager.py
'''
from http import HTTPStatus
from app.utils.redisdb import redis
from app.utils.mysqldb import db
from flask_restx import Namespace, Resource, fields, reqparse
from app.model import Users
from app.utils.limiter import limiter
from app.utils.aes import decrypt
resetpw_ns = Namespace('resetpw', description='重置密码')
model = resetpw_ns.model('resetpw', {
	'code': fields.Integer(required=True, description='状态码'),
	'message': fields.String(required=True, description='状态信息'),
	'success': fields.Boolean(required=True, description='是否成功'),
})
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('email', type=str, location='json', nullable=False, required=True, help='邮箱不能为空')
parser.add_argument('emailcode', type=str, location='json', nullable=False, required=True, help='邮件验证码不能为空')
parser.add_argument('password', type=str, location='json', nullable=False, required=True, help='密码不能为空')
parser.add_argument('captcha', type=str, location='json', nullable=False, required=True, help='验证码不能为空')
parser.add_argument('requestid', type=str, location='cookies', nullable=False, help='会话开始id')
parser.add_argument('X-CSRFToken', type=str, location='headers', nullable=False, required=True, help='csrf_token不能为空')


@resetpw_ns.route('')
@resetpw_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@resetpw_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@resetpw_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class ResetPW(Resource):
	'''
	@Author: 邵佳泓
	@msg: 修改密码
	'''
	decorators = [
		limiter.limit('3/minute'),
		limiter.limit('50/day')
	]

	@resetpw_ns.expect(parser)
	@resetpw_ns.marshal_with(model)
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
		email = request_data.get('email')
		emailcode = request_data.get('emailcode')
		captcha = request_data.get('captcha')
		redisemail = redis.get('/'.join(["email", requestid, email]))
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
			user = Users.query.filter_by(email=email).first()
			if user is None:
				return {
					'code': 6,
					'message': '用户未注册',
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
