'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 12:33:35
FilePath: /server/app/managers/admin_manager/user_manager.py
'''
import base64
from http import HTTPStatus
import time
import datetime
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.limiter import limiter
from app.utils.redisdb import redis
from app.model import Users, Roles, User2Role
from app.managers.admin_manager.model import standardmodel

datetime.datetime.now()
user_ns = Namespace('user', description='用户管理')
user_ns.models[standardmodel.name] = standardmodel
user_model = user_ns.model(
    'usermodel', {
        'userid': fields.Integer(required=True, description='用户id'),
        'name': fields.String(required=True, description='用户名'),
        'email': fields.String(required=True, description='邮箱'),
        'created_on': fields.DateTime(required=True, description='创建时间'),
        'last_login': fields.DateTime(required=True, description='最后登录时间'),
        'valid': fields.Boolean(required=True, description='账号是否有效'),
        'last_login_ip': fields.String(required=True, description='最后登录ip'),
        'role': fields.List(fields.String, required=True, description='角色'),
        'avatar': fields.String(required=True, description='头像'),
        'cucaccount': fields.String(required=True, description='中传学号'),
        'description': fields.String(required=True, description='个人简介')
    })
model = user_ns.model(
    'userinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.List(fields.Nested(user_model, description='数据')),
        'total': fields.Integer(required=True, description='总数')
    })


@user_ns.route('/userinfo/<int:page>/<int:size>/<string:order>')
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 20/minute, 1000/day.")
class UserIno(Resource):
    '''
    Author: 邵佳泓
    msg: 发送用户信息
    '''
    decorators = [limiter.limit('20/minute'), limiter.limit('1000/day')]

    @user_ns.doc(params={'page': '页码', 'size': '每页数量', 'order': '排序'})
    @user_ns.marshal_with(model)
    @jwt_required()
    def get(self, page: int, size: int, order: str):
        '''
        Author: 邵佳泓
        msg: 发送用户信息
        param {*} self
        param {int} page
        param {int} size
        param {str} order
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        expire_time = int(time.time()) + 86400
        key = '/'.join(['userinfo', order, str(page), str(size)])
        length = Users.query.count()
        if 'admin' not in [role.name for role in user.role]:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        elif (bytedata := redis.get(key)) and page != length // size + 1:
            data = eval(bytedata.decode('utf-8'))
            return {
                'code': 0,
                'message': '获取用户信息成功',
                'success': True,
                'data': data,
                'total': length
            }
        else:
            users = Users.query.order_by(Users.userid.asc() if order ==
                                         'ascending' else Users.userid.desc()).paginate(
                                             page, size, False).items
            data = [{
                'userid':
                user.userid,
                'name':
                user.name,
                'email':
                user.email,
                'cucaccount':
                user.cucaccount,
                'created_on':
                user.created_on,
                'last_login':
                user.last_login,
                'valid':
                user.valid,
                'description':
                user.description,
                'last_login_ip':
                user.last_login_ip,
                'avatar':
                "data:image/png;base64," + base64.b64encode(user.avatar).decode('ascii'),
                'role': [role.name for role in user.role]
            } for user in users if 'admin' not in [role.name for role in user.role]]
            pipe = redis.pipeline()
            pipe.set(key, str(data).encode('utf-8'))
            pipe.expireat(key, expire_time)
            pipe.execute()
            return {
                'code': 0,
                'message': '获取用户信息成功',
                'success': True,
                'data': data,
                'total': length
            }


updateparser = reqparse.RequestParser()
updateparser.add_argument('userid', type=int, nullable=False, required=True, help='用户ID不能为空')
updateparser.add_argument('role',
                          type=str,
                          nullable=False,
                          required=True,
                          help='角色不能为空',
                          action='append')


@user_ns.route('/update')
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 100/day.")
class Update(Resource):
    '''
    Author: 邵佳泓
    msg: 更新角色
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @user_ns.marshal_with(standardmodel)
    @user_ns.expect(updateparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 更新角色
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' not in [role.name for role in user.role]:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = updateparser.parse_args()
            userid = request_data.get('userid')
            User2Role.query.filter_by(user_id=userid).delete()
            for role in request_data.get('role'):
                roleid = Roles.query.filter_by(name=role).first().roleid
                User2Role.add(User2Role(user_id=userid, role_id=roleid))
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('userinfo')
            ]
            return {'code': 0, 'message': '变更角色成功', 'success': True}


deleteparser = reqparse.RequestParser()
deleteparser.add_argument('userid', type=int, nullable=False, required=True, help='用户ID不能为空')


@user_ns.route('/delete')
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 100/day.")
class Delete(Resource):
    '''
    Author: 邵佳泓
    msg: 删除用户
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @user_ns.marshal_with(standardmodel)
    @user_ns.expect(deleteparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 删除用户
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' not in [role.name for role in user.role]:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = deleteparser.parse_args()
            userid = request_data.get('userid')
            User2Role.query.filter_by(user_id=userid).delete()
            Users.query.filter_by(userid=userid).delete()
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('userinfo')
            ]
            return {'code': 0, 'message': '删除用户成功', 'success': True}


banparser = reqparse.RequestParser()
banparser.add_argument('userid', type=int, nullable=False, required=True, help='用户ID不能为空')


@user_ns.route('/ban')
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 3/minute, 100/day.")
class Ban(Resource):
    '''
    Author: 邵佳泓
    msg: 用户封禁管理
    '''
    decorators = [limiter.limit('3/minute'), limiter.limit('100/day')]

    @user_ns.marshal_with(standardmodel)
    @user_ns.expect(banparser)
    @jwt_required()
    def post(self):
        '''
        Author: 邵佳泓
        msg: 用户封禁管理
        param {*} self
        '''
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        if 'admin' not in [role.name for role in user.role]:
            return {'code': 1, 'message': '非管理员用户', 'success': False}
        else:
            request_data = deleteparser.parse_args()
            userid = request_data.get('userid')
            user = Users.query.filter_by(userid=userid)
            [
                redis.delete(key) for key in redis.keys()
                if key.decode('utf-8').startswith('userinfo')
            ]
            if user.first().valid:
                user.update({'valid': False})
                return {'code': 0, 'message': '封禁用户成功', 'success': True}
            else:
                user.update({'valid': True})
                return {'code': 0, 'message': '解封用户成功', 'success': True}
                