'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 23:11:28
@FilePath: /server/app/managers/personal_manager/uploadavatar_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, reqparse
from app.utils.limiter import limiter
from app.utils.redisdb import redis
from app.model import Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from app.managers.personal_manager.model import model
upload_ns = Namespace('upload', description='用户信息')
upload_ns.models[model.name] = model
parser = reqparse.RequestParser()
parser.add_argument('avatar', type=FileStorage, nullable=False, required=True, help='头像不能为空')

@upload_ns.route('')
@upload_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@upload_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@upload_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 1/minute, 5/day.")
class Upload(Resource):
    '''
    Author: 邵佳泓
    msg: 上传头像
    '''
    decorators = [
        limiter.limit('1/minute'),
        limiter.limit('5/day')
    ]

    @upload_ns.marshal_with(model)
    @upload_ns.expect(parser)
    @jwt_required()
    def post(self):
        request_data = parser.parse_args()
        avatar = request_data.get('avatar')
        userid = get_jwt_identity()
        [redis.delete(key) for key in redis.keys() if key.decode('utf-8').startswith('userinfo')]
        Users.query.filter_by(id=userid).update({'avatar': avatar.stream.read()})
        return {
            'code': 200,
            'message': '更新个人信息成功',
            'success': True
        }
        