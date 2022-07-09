'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-09 21:43:33
FilePath: /server/app/managers/admin_manager/role_manager.py
'''
from http import HTTPStatus
import time
from flask_restx import Namespace, Resource, fields, reqparse
from flask_restx.inputs import positive, regex
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app.utils.limiter import limiter
from app.utils.redisdb import redis
from app.model import Users, Roles
from app.managers.model import standardmodel

role_ns = Namespace('role', description='角色管理')
role_ns.models[standardmodel.name] = standardmodel
role_model = role_ns.model(
    'rolemodel', {
        'roleid': fields.Integer(required=True, description='角色id'),
        'name': fields.String(required=True, description='角色名'),
        'description': fields.String(required=True, description='个人简介'),
        'routes': fields.List(fields.String(required=True, description='路由')),
        'valid': fields.Boolean(required=True, description='是否有效')
    })
data_model = role_ns.model(
    'roledatamodel', {
        'roles': fields.List(fields.Nested(role_model)),
        'total': fields.Integer(required=True, description='总数')
    })
model = role_ns.model(
    'roleinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(data_model, description='数据')
    })
routesmodel = role_ns.model(
    'allroles', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.String, required=True, description='路由'),
    })

pagination_reqparser = reqparse.RequestParser(bundle_errors=True)
pagination_reqparser.add_argument('page', location='args', type=positive, default=1, help='页码')
pagination_reqparser.add_argument('size',
                                  location='args',
                                  type=positive,
                                  default=10,
                                  choices=[5, 10, 20],
                                  help='每页数量')
pagination_reqparser.add_argument('order',
                                  location='args',
                                  type=regex(pattern='^((ascending)|(descending)){1}$'),
                                  default='ascending',
                                  choices=['ascending', 'descending'],
                                  help='排序方式')
pagination_reqparser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')

@role_ns.route('/roleinfo')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class RoleInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 发送角色信息
    '''
    decorators = [limiter.limit('20/minute'), limiter.limit('1000/day')]

    @role_ns.expect(pagination_reqparser)
    @role_ns.marshal_with(model)
    @jwt_required()
    def get(self):
        '''
        Author: 邵佳泓
        msg: 发送角色信息
        param {*} self
        '''
        request_data = pagination_reqparser.parse_args()
        page = request_data.get('page')
        size = request_data.get('size')
        order = request_data.get('order')
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        expire_time = int(time.time()) + 86400
        key = '/'.join(['roleinfo', order, str(page), str(size)])
        length = Roles.query.count()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        elif (bytedata := redis.get(key)) and page != length // size + 1:
            data = eval(bytedata.decode('utf-8'))
            return {
                'code': 0,
                'message': '获取角色信息成功',
                'success': True,
                'data': {
                    'roles': data,
                    'total': length
                }
            }
        else:
            roles = Roles.query.order_by(Roles.roleid.asc() if order ==
                                         'ascending' else Roles.roleid.desc()).paginate(
                                             page, size, False).items
            data = [{
                'roleid': role.roleid,
                'name': role.name,
                'description': role.description,
                'valid': role.valid,
                'routes': eval(role.authedroutes)
            } for role in roles if role.name != 'admin']
            pipe = redis.pipeline()
            pipe.set(key, str(data).encode('utf-8'))
            pipe.expireat(key, expire_time)
            pipe.execute()
            return {
                'code': 0,
                'message': '获取角色信息成功',
                'success': True,
                'data': {
                    'roles':data,
                    'total': length
                }
            }
roleinfoparser = reqparse.RequestParser(bundle_errors=True)
roleinfoparser.add_argument('Authorization',
                            type=str,
                            location='headers',
                            nullable=False,
                            required=True,
                            help='Authorization不能为空')
@role_ns.route('/routes')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class AllRoutesInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 返回全部路由
    '''
    decorators = [limiter.limit('20/minute'), limiter.limit('1000/day')]
    @role_ns.marshal_with(routesmodel)
    @role_ns.expect(roleinfoparser)
    @jwt_required()
    def get(self):
        '''
        Author: 邵佳泓
        msg: 返回全部路由
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            routes = user.role[0].authedroutes
            return {
                'code': 0,
                'message': '获取角色信息成功',
                'success': True,
                'data': [route for route in eval(routes) if route != '/dashboard']
            }

updateparser = reqparse.RequestParser(bundle_errors=True)
updateparser.add_argument('roleid', type=positive, nullable=False, required=True, help='角色ID不能为空')
updateparser.add_argument('routes',
                          type=regex(pattern=r'^/\w+$'),
                          nullable=False,
                          required=True,
                          help='角色路由不能为空',
                          action='append')
updateparser.add_argument('X-CSRFToken',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='csrf_token不能为空')
updateparser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')

@role_ns.route('/update')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class UpdateRole(Resource):
    '''
    Author: 邵佳泓
    msg: 更新角色权限
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @role_ns.marshal_with(standardmodel)
    @role_ns.expect(updateparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 更新角色权限
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = updateparser.parse_args()
            roleid = request_data.get('roleid')
            routes = request_data.get('routes')
            Roles.query.filter_by(roleid=roleid).update({'authedroutes': str(routes)})
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('roleinfo')
            ]
            return {'code': 0, 'message': '变更角色权限成功', 'success': True}


createparser = reqparse.RequestParser(bundle_errors=True)
createparser.add_argument('name',
                          type=regex(pattern=r'\S{2,}'),
                          nullable=False,
                          required=True,
                          help='角色名不能为空')
createparser.add_argument('description',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='角色简介不能为空')
createparser.add_argument('X-CSRFToken',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='csrf_token不能为空')
createparser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')


@role_ns.route('/create')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class CreateRole(Resource):
    '''
    Author: 邵佳泓
    msg: 添加角色
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @role_ns.marshal_with(standardmodel)
    @role_ns.expect(createparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 添加角色
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = createparser.parse_args()
            name = request_data.get('name')
            if Roles.query.filter_by(name=name).first():
                return {'code': 1, 'message': '角色名已存在', 'success': False}
            else:
                description = request_data.get('description')
                Roles.add(Roles(name=name, description=description))
                [
                    redis.delete(key) for key in redis.keys()
                    if key.decode('utf-8').startswith('roleinfo/desc')
                ]
                return {'code': 0, 'message': '创建角色成功', 'success': True}


deleteparser = reqparse.RequestParser(bundle_errors=True)
deleteparser.add_argument('roleid', type=positive, nullable=False, required=True, help='角色ID不能为空')
deleteparser.add_argument('X-CSRFToken',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='csrf_token不能为空')
deleteparser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    nullable=False,
                    required=True,
                    help='Authorization不能为空')

@role_ns.route('/delete')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class DeleteRole(Resource):
    '''
    Author: 邵佳泓
    msg: 删除角色
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @role_ns.marshal_with(standardmodel)
    @role_ns.expect(deleteparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 删除角色
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = deleteparser.parse_args()
            roleid = request_data.get('roleid')
            try:
                Roles.query.filter_by(roleid=roleid).delete()
                [
                    redis.delete(key) for key in redis.keys()
                    if key.decode('utf-8').startswith('roleinfo')
                ]
                return {'code': 0, 'message': '删除角色成功', 'success': True}
            except SQLAlchemyError:
                return {'code': 2, 'message': '系统中有用户属于当前角色，不可删除', 'success': False}


banparser = reqparse.RequestParser(bundle_errors=True)
banparser.add_argument('roleid', type=positive, nullable=False, required=True, help='角色ID不能为空')
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

@role_ns.route('/ban')
@role_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@role_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.",
                  standardmodel)
class BanRole(Resource):
    '''
    Author: 邵佳泓
    msg: 角色限制管理
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @role_ns.marshal_with(standardmodel)
    @role_ns.expect(banparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 角色限制管理
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' != user.role[0].name:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = deleteparser.parse_args()
            roleid = request_data.get('roleid')
            role = Roles.query.filter_by(roleid=roleid)
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('roleinfo')
            ]
            if role.first().valid:
                role.update({'valid': False})
                return {'code': 0, 'message': '封禁角色成功', 'success': True}
            else:
                role.update({'valid': True})
                return {'code': 0, 'message': '解封角色成功', 'success': True}
