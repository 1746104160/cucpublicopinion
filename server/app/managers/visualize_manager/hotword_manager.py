'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-13 13:00:59
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 18:34:56
FilePath: /server/app/managers/visualize_manager/hotword_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.model import HotWord
from app.managers.model import standardmodel
from app.utils.limiter import limiter

hotword_ns = Namespace('hotword', description='热词管理')
hotword_ns.models[standardmodel.name] = standardmodel
hotword_model = hotword_ns.model(
    'hotwordmodel', {
        'hot_word': fields.String(required=True, description='热词'),
        'hot': fields.Float(required=True, description='热度'),
    })
model = hotword_ns.model(
    'hotwordinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.Nested(hotword_model))
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@hotword_ns.route('')
@hotword_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@hotword_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                     standardmodel)
@hotword_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class HotwordInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 热词信息
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @hotword_ns.expect(parser)
    @hotword_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 热词信息
        param {*} self
        '''
        hotwords = [
            hotword.__dict__
            for hotword in HotWord.query.order_by(HotWord.hot.desc()).limit(20).all()
        ]
        return {'code': 0, 'message': '热词查询成功', 'success': True, 'data': hotwords}
