'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 10:52:20
FilePath: /server/app/managers/admin_manager/security_manager.py
'''
from http import HTTPStatus
import re
from flask_restx import Namespace, Resource, fields, reqparse
from flask_restx.inputs import positive, regex
from flask_jwt_extended import jwt_required, get_current_user
from app.utils.redisdb import redis
from app.managers.model import standardmodel

security_ns = Namespace('security', description='接口安全管理')
security_ns.models[standardmodel.name] = standardmodel
security_model = security_ns.model(
    'securitymodel', {
        'ip_addr': fields.String(required=True, description='IP地址'),
        'servicename': fields.String(required=True, description='服务名称'),
        'current_visit': fields.Integer(required=True, description='当日访问次数'),
        'max_visit': fields.Integer(required=True, description='当日最高访问次数'),
    })
data_model = security_ns.model(
    'datamodel', {
        'security': fields.List(fields.Nested(security_model)),
        'total': fields.Integer(required=True, description='总数'),
        'ips': fields.List(fields.String(required=True, description='全部IP地址'))
    })
model = security_ns.model(
    'securityinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(data_model, description='数据')
    })
pagination_reqparser = reqparse.RequestParser(bundle_errors=True)
pagination_reqparser.add_argument('page', location='args', type=positive, default=1, help='页码')
pagination_reqparser.add_argument('size',
                                  location='args',
                                  type=positive,
                                  default=10,
                                  choices=[5, 10, 20],
                                  help='每页数量')
pagination_reqparser.add_argument(
    'ip_addr',
    location='args',
    type=regex(
        pattern=r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'),
    help='ip地址')
pagination_reqparser.add_argument('Authorization',
                                  type=str,
                                  location='headers',
                                  nullable=False,
                                  required=True,
                                  help='Authorization不能为空')


@security_ns.route('/serviceinfo')
@security_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@security_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                      standardmodel)
@security_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class ServiceInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 发送接口安全信息
    '''
    decorators = [jwt_required()]

    @security_ns.expect(pagination_reqparser)
    @security_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 发送接口安全信息
        param {*} self
        '''
        user = get_current_user()
        if '/security' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理接口安全的权限', 'success': False}
        else:
            request_data = pagination_reqparser.parse_args()
            page = request_data.get('page')
            size = request_data.get('size')
            ip_addr = request_data.get('ip_addr')
            ips = list(
                set([key.decode('utf8').split('/')[1] for key in redis.keys('LIMITER/*/day')]))
            keys = redis.keys(f'LIMITER/{ip_addr}/*/day') if ip_addr else redis.keys(
                'LIMITER/*/day')
            total = len(keys)
            start = (page - 1) * size
            end = min(start + size, total)
            data = [{
                "ip_addr": tmp[1],
                "servicename": tmp[2],
                "current_visit": redis.get(key).decode('utf8'),
                "max_visit": tmp[3]
            } for key in keys[start:end] if (tmp := key.decode('utf8').split('/'))]
            return {
                'code': 0,
                'message': 'success',
                'success': True,
                'data': {
                    'security': data,
                    'total': total,
                    'ips': ips
                }
            }


banparser = reqparse.RequestParser(bundle_errors=True)
banparser.add_argument('data',
                       type=str,
                       required=True,
                       nullable=False,
                       location='json',
                       help="需要封禁的接口")

banparser.add_argument('X-CSRFToken',
                       type=str,
                       location='headers',
                       nullable=False,
                       required=True,
                       help='csrf_token不能为空')
banparser.add_argument('Authorization',
                       type=str,
                       location='headers',
                       nullable=False,
                       required=True,
                       help='Authorization不能为空')


@security_ns.route('/ban')
@security_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@security_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                      standardmodel)
@security_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class BanAPI(Resource):
    '''
    Author: 邵佳泓
    msg: 接口封禁管理
    '''
    decorators = [jwt_required()]

    @security_ns.marshal_with(standardmodel)
    @security_ns.expect(banparser)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 接口封禁管理
        param {*} self
        '''
        user = get_current_user()
        if '/security' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理接口安全的权限', 'success': False}
        else:
            request_data = banparser.parse_args()
            try:
                datas = eval(request_data.get('data'))
            except SyntaxError:
                return {'code': 1, 'message': '数据格式错误', 'success': False}
            for data in datas:
                ip_addr = data.get('ip_addr')
                if not ip_addr:
                    return {'code': 1, 'message': 'ip地址不能为空', 'success': False}
                elif not re.match(
                        r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})' +
                        r'(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}', ip_addr):
                    return {'code': 1, 'message': 'ip地址格式错误', 'success': False}
                servicename = data.get('servicename')
                if not servicename:
                    return {'code': 1, 'message': '服务名不能为空', 'success': False}
                max_visit = data.get('max_visit')
                if not max_visit:
                    return {'code': 1, 'message': '最大访问数不能为空', 'success': False}
                elif not isinstance(max_visit, int):
                    return {'code': 1, 'message': '最大访问数必须为整数', 'success': False}
                key = f'LIMITER/{ip_addr}/{servicename}/{max_visit}/1/day'.encode("utf8")
                redis.set(key, max_visit)
        return {'code': 0, 'message': '封禁接口操作成功', 'success': True}


@security_ns.route('/unban')
@security_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@security_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.",
                      standardmodel)
@security_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class UnBanAPI(Resource):
    '''
    Author: 邵佳泓
    msg: 接口封禁管理
    '''
    decorators = [jwt_required()]

    @security_ns.marshal_with(standardmodel)
    @security_ns.expect(banparser)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 接口封禁管理
        param {*} self
        '''
        user = get_current_user()
        if '/security' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理接口安全的权限', 'success': False}
        else:
            request_data = banparser.parse_args()
            try:
                datas = eval(request_data.get('data'))
            except SyntaxError:
                return {'code': 1, 'message': '数据格式错误', 'success': False}
            for data in datas:
                ip_addr = data.get('ip_addr')
                if not ip_addr:
                    return {'code': 1, 'message': 'ip地址不能为空', 'success': False}
                elif not re.match(
                        r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})' +
                        r'(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}', ip_addr):
                    return {'code': 1, 'message': 'ip地址格式错误', 'success': False}
                servicename = data.get('servicename')
                if not servicename:
                    return {'code': 1, 'message': '服务名不能为空', 'success': False}
                max_visit = data.get('max_visit')
                if not max_visit:
                    return {'code': 1, 'message': '最大访问数不能为空', 'success': False}
                elif not isinstance(max_visit, int):
                    return {'code': 1, 'message': '最大访问数必须为整数', 'success': False}
                key = f'LIMITER/{ip_addr}/{servicename}/{max_visit}/1/day'.encode("utf8")
                redis.set(key, 0)
        return {'code': 0, 'message': '封禁接口操作成功', 'success': True}
