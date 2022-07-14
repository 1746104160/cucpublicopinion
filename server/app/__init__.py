'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 14:54:37
FilePath: /server/app/__init__.py
'''
import datetime
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_jwt_extended import JWTManager

from app.model import Users
from .utils import db, redis, limiter, requestid, mail
from .managers import auth, personal, admin, visualize, apk


def create_app():
    '''
    Author: 邵佳泓
    msg: 创建web后端服务
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    CORS(app, supports_credentials=True, resources=r"*")
    CSRFProtect(app)
    jwt = JWTManager(app)

    db.init_app(app)
    redis.init_app(app)
    limiter.init_app(app)
    requestid.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(personal)
    app.register_blueprint(admin)
    app.register_blueprint(visualize)
    app.register_blueprint(apk)

    @app.route('/', methods=['GET'])
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/assets/<string:filename>', methods=['GET'])
    def assets(filename):
        return send_from_directory('static/assets', filename)

    @app.route('/apk/<string:version>', methods=['GET'])
    def apkfile(version):
        return send_from_directory('resource', 'SEMS_'+version+'.apk')

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.after_request
    def after_request(response):
        response.set_cookie('csrf_token', generate_csrf())
        return response

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(_jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        exp = jwt_payload["exp"]
        token_in_redis = redis.get(jti)
        return token_in_redis is not None or exp < datetime.datetime.now().timestamp()

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.userid

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Users.query.filter_by(userid=identity).one_or_none()

    return app
