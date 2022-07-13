'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-13 13:00:59
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 00:13:05
FilePath: /server/app/managers/visualize_manager/postnum_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.model import News, PostNum
from app.managers.model import standardmodel
from app.utils.limiter import limiter

postnum_ns = Namespace('postnum', description='数据来源统计管理')
postnum_ns.models[standardmodel.name] = standardmodel
postnum_model = postnum_ns.model(
    'postnummodel', {
        'name': fields.String(required=True, description='数据来源'),
        'value': fields.Float(required=True, description='数量'),
    })
data_model = postnum_ns.model(
    'postnumdata', {
        'data': fields.List(fields.Nested(postnum_model)),
        'total': fields.Integer(required=True, description='总数')
    })
model = postnum_ns.model(
    'postnuminfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(data_model),
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@postnum_ns.route('')
@postnum_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@postnum_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                     standardmodel)
@postnum_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class PostnumInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 统计信息
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @postnum_ns.expect(parser)
    @postnum_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 统计信息
        param {*} self
        '''
        total = News.query.count()
        datas = [{
            'name': result.articleSource,
            'value': result.num
        } for result in PostNum.query.order_by(PostNum.num.desc()).limit(4).all()]
        return {
            'code': 0,
            'message': '热词查询成功',
            'success': True,
            'data': {
                'data': datas,
                'total': total
            }
        }
