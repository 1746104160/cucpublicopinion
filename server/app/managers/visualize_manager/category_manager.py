'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-13 13:00:59
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 23:03:47
FilePath: /server/app/managers/visualize_manager/category_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.model import NewsClass
from app.managers.model import standardmodel
from app.utils.limiter import limiter

category_ns = Namespace('category', description='类别管理')
category_ns.models[standardmodel.name] = standardmodel
category_model = category_ns.model(
    'categorymodel', {
        'name': fields.String(required=True, description='类型'),
        'value': fields.Float(required=True, description='数量'),
    })
model = category_ns.model(
    'categoryinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.Nested(category_model)),
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@category_ns.route('')
@category_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@category_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                      standardmodel)
@category_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class CategoryInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 新闻类型
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @category_ns.expect(parser)
    @category_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 新闻类型
        param {*} self
        '''
        categories = NewsClass.query.with_entities(NewsClass.category).distinct().all()
        data = sorted([{
            'name': category[0],
            'value': NewsClass.query.filter_by(category=category[0]).count()
        } for category in categories],key=lambda x:x['value'],reverse=True)
        return {'code': 0, 'message': '类别数据查询成功', 'success': True, 'data': data}
