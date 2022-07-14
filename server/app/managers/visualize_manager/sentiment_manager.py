'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-13 13:00:59
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 12:48:28
FilePath: /server/app/managers/visualize_manager/sentiment_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.model import News, SenAna
from app.managers.model import standardmodel
from app.utils.limiter import limiter

sentiment_ns = Namespace('sentiment', description='情感度管理')
sentiment_ns.models[standardmodel.name] = standardmodel
sentiment_model = sentiment_ns.model(
    'sentimentmodel', {
        'name': fields.String(required=True, description='情感倾向'),
        'value': fields.Float(required=True, description='数量'),
    })
model = sentiment_ns.model(
    'sentimentinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.List(fields.Nested(sentiment_model))),
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('articleSource',
                    type=str,
                    location='args',
                    action="split",
                    default='',
                    help='articleSource用于绘制子图')

parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@sentiment_ns.route('')
@sentiment_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@sentiment_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                       standardmodel)
@sentiment_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class SentimentInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 情感信息
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @sentiment_ns.expect(parser)
    @sentiment_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 情感信息
        param {*} self
        '''
        request_data = parser.parse_args()
        article_sources = request_data.get('articleSource')
        if article_sources == '':
            attitudes = SenAna.query.with_entities(SenAna.attitude).distinct().all()
            data = [[{
                'name': attitude[0],
                'value': SenAna.query.filter_by(attitude=attitude[0]).count()
            } for attitude in attitudes]]
            return {'code': 0, 'message': '情感数据查询成功', 'success': True, 'data': data}
        else:
            data = []
            for article_source in article_sources:
                attitudes = SenAna.query.with_entities(SenAna.attitude).distinct().all()
                data.append([{
                    'name':
                    attitude[0],
                    'value':
                    SenAna.query.join(News, SenAna.newsid == News.newsid).filter(
                        SenAna.attitude == attitude[0],
                        News.articleSource == article_source).count()
                } for attitude in attitudes])
            return {'code': 0, 'message': '情感数据查询成功', 'success': True, 'data': data}
