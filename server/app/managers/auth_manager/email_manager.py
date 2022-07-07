'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 00:31:45
@FilePath: /server/app/managers/auth_manager/email_manager.py
'''
from http import HTTPStatus
from app.utils.redisdb import redis
from flask_restx import Namespace, Resource, fields, reqparse
import re
from flask_mail import Message
from app.utils.mail import mail
from app.utils.limiter import limiter
import random
import time
CHAR_SET = [chr(ord('A')+i) for i in range(26)] +\
	[chr(ord('a')+i) for i in range(26)] +\
	[chr(ord('0')+i) for i in range(10)]
email_ns = Namespace('email', description='邮件验证码')
model = email_ns.model('email', {
	'code': fields.Integer(required=True, description='状态码'),
	'message': fields.String(required=True, description='状态信息'),
	'success': fields.Boolean(required=True, description='是否成功'),
})
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('email', type=str, location='json', nullable=False, required=True, help='邮箱不能为空')
parser.add_argument('requestid', type=str, location='cookies', nullable=False, required=True, help='会话开始id')
parser.add_argument('X-CSRFToken', type=str, location='headers', nullable=False, required=True, help='csrf_token不能为空')


@email_ns.route('')
@email_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@email_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@email_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 1/minute, 10/day.")
class Email(Resource):
	'''
	@Author: 邵佳泓
	@msg: 发送邮件验证码
	'''
	decorators = [
		limiter.limit('1/minute'),
		limiter.limit('10/day')
	]

	@email_ns.expect(parser)
	@email_ns.marshal_with(model)
	def post(self):
		request_data = parser.parse_args()
		email = request_data.get('email')
		requestid = request_data.get('requestid')
		if not re.match(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
			return {'code': 1, 'message': '邮箱格式不正确', 'success': False}
		else:
			code = ''.join(random.sample(CHAR_SET, 6))
			message = Message('邮箱验证码',
							recipients=[email],
							html=f'''<p>您好！</p>
			<p>您的验证码是：<strong style="color:orangered;">{code}</strong></p>
			<p>如果不是您本人操作，请无视此邮件</p>''')
			try:
				mail.send(message)
				value = str(code).encode('utf-8')
				expire_time = int(time.time()) + 300
				key = '/'.join(["email", requestid, email])
				p = redis.pipeline()
				p.set(key, value)
				p.expireat(key, expire_time)
				p.execute()
				return {
					"code": 0,
					"success": True,
					"message": f'邮件验证码已发送到{email}'
				}
			except:
				return {
					"code": 2,
					"success": False,
					"message": f'邮件验证码发送失败，请使用中国大陆邮箱'
				}