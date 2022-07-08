'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 13:00:34
FilePath: /server/app/managers/personal_manager/updateinfo_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.redisdb import redis
from app.utils.limiter import limiter
from app.model import Users
from app.managers.personal_manager.model import model

update_ns = Namespace('update', description='用户信息')
update_ns.models[model.name] = model
parser = reqparse.RequestParser()
parser.add_argument('description',
                    type=str,
                    location='json',
                    nullable=False,
                    required=True,
                    help='个人简介不能为空')


@update_ns.route('')
@update_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@update_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@update_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 50/day.")
class Update(Resource):
    '''
    Author: 邵佳泓
    msg: 更新个人信息
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('50/day')]

    @update_ns.marshal_with(model)
    @update_ns.expect(parser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 更新个人信息
        param {*} self
        '''
        request_data = parser.parse_args()
        description = request_data.get('description')
        userid = get_jwt_identity()
        [redis.delete(key) for key in redis.keys() if key.decode('utf-8').startswith('userinfo')]
        Users.query.filter_by(id=userid).update({'description': description})
        return {'code': 200, 'message': '更新个人信息成功', 'success': True}
