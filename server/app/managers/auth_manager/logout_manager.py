'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 00:25:47
FilePath: /server/app/managers/auth_manager/logout_manager.py
'''
import datetime
from http import HTTPStatus
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, reqparse
from app.utils.redisdb import redis
from app.utils.limiter import limiter
from app.managers.model import standardmodel as model

logout_ns = Namespace('logout', description='注销')
logout_ns.models[model.name] = model
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@logout_ns.route('')
@logout_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", model)
@logout_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", model)
@logout_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                   model)
class LogoutSystem(Resource):
    '''
    Author: 邵佳泓
    msg: 注销系统账号
    '''
    decorators = [jwt_required(), limiter.limit('3/minute'), limiter.limit('50/day')]

    @logout_ns.expect(parser)
    @logout_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 注销系统账号
        param {*} self
        '''
        jti = get_jwt()["jti"]
        redis.set(jti, "", ex=datetime.timedelta(hours=1))
        return {'code': 0, 'message': '注销成功', 'success': True}
