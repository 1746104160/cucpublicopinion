'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-04 16:00:03
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 01:49:05
@FilePath: /server/app/__init__.py
'''
from flask import Flask, send_from_directory, make_response
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect,generate_csrf
from flask_jwt_extended import JWTManager

from .utils import db, redis, limiter, requestid, mail
from .managers import auth,personal,admin

def create_app():
	'''
	@Author: 邵佳泓
	@msg: 创建web后端服务
	'''
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile('config.py')
	CORS(app, supports_credentials=True, resources=r"*")
	jwt = JWTManager(app)
	CSRFProtect(app)
	db.init_app(app)
	redis.init_app(app)
	limiter.init_app(app)
	requestid.init_app(app)
	mail.init_app(app)
	app.register_blueprint(auth)
	app.register_blueprint(personal)
	app.register_blueprint(admin)
	@app.route('/', methods=['GET'])
	def index():
		return send_from_directory('static', 'index.html')

	@app.route('/favicon.ico', methods=['GET'])
	def favicon():
		return send_from_directory('static',
								   'favicon.ico',
								   mimetype='image/vnd.microsoft.icon')
	@app.after_request
	def after_request(response):
		response.set_cookie('csrf_token', generate_csrf())
		return response

	@jwt.expired_token_loader
	def expired_token_callback():
		return make_response("token expired", 403)

	@jwt.unauthorized_loader
	def unauthorized_callback():
		return make_response("unauthorized", 403)

	return app
