'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-13 13:00:59
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 00:15:56
FilePath: /server/app/managers/visualize_manager/cluster_manager.py
'''
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.model import NewsCluster
from app.managers.model import standardmodel
from app.utils.limiter import limiter

cluster_ns = Namespace('cluster', description='聚类管理')
cluster_ns.models[standardmodel.name] = standardmodel
cluster_model = cluster_ns.model(
    'clustermodel', {
        'name': fields.String(required=True, description='聚类名称'),
        'value': fields.Float(required=True, description='数量'),
    })
model = cluster_ns.model(
    'clusterinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.Nested(cluster_model)),
    })
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')

@cluster_ns.route('')
@cluster_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@cluster_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                     standardmodel)
@cluster_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class ClusterInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 新闻聚类
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @cluster_ns.expect(parser)
    @cluster_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 新闻聚类
        param {*} self
        '''
        clusters = NewsCluster.query.with_entities(NewsCluster.topic_words).distinct().all()
        data = sorted([{
            'name': cluster[0],
            'value': NewsCluster.query.filter(NewsCluster.topic_words == cluster[0]).count()
        } for cluster in clusters],key=lambda x:x['value'],reverse=True)
        return {'code': 0, 'message': '类别数据查询成功', 'success': True, 'data': data}
