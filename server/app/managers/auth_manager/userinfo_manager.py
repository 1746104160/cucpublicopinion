'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 23:57:30
@FilePath: /server/app/managers/auth_manager/userinfo_manager.py
'''
import base64
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from app.utils.limiter import limiter
from app.model import Users
from flask_jwt_extended import jwt_required, get_jwt_identity
userinfo_ns = Namespace('userinfo', description='用户信息')
user_model = userinfo_ns.model('usermodel',{
    'userid':fields.Integer(required=True,description='验证码'),
    'name':fields.String(required=True,description='用户名'),
    'email':fields.String(required=True,description='邮箱'),
    'created_on':fields.DateTime(required=True,description='创建时间'),
    'last_login':fields.DateTime(required=True,description='最后登录时间'),
    'valid':fields.Boolean(required=True,description='账号是否有效'),
    'last_login_ip':fields.String(required=True,description='最后登录ip'),
    'role':fields.List(fields.String,required=True,description='角色'),
    'avatar':fields.String(required=True,description='头像'),
    'cucaccount':fields.String(required=True,description='中传学号'),
})
data_model = userinfo_ns.model('userinfodata', {
    'Routes': fields.List(fields.String(description='路由')),
    'userinfo': fields.Nested(user_model,description='用户信息')
})
model = userinfo_ns.model('userinfo', {
    'code': fields.Integer(required=True, description='状态码'),
    'message': fields.String(required=True, description='状态信息'),
    'success': fields.Boolean(required=True, description='是否成功'),
    'data'    : fields.Nested(data_model, description='数据')
})


@userinfo_ns.route('')
@userinfo_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@userinfo_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@userinfo_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 10/minute, 500/day.")
class UserIno(Resource):
    '''
    Author: 邵佳泓
    msg: 发送用户信息
    '''
    decorators = [
        limiter.limit('10/minute'),
        limiter.limit('500/day')
    ]

    @userinfo_ns.marshal_with(model)
    @jwt_required()
    def get(self):
        userid = get_jwt_identity()
        user = Users.query.filter_by(userid=userid).first()
        return {
            'code': 0,
            'message': '发送成功',
            'data':{
                'Routes':list(set([route for role in user.role if role.valid for route in eval(role.authedroutes)])),
                'userinfo':{
                    'userid':user.userid,
                    'name':user.name,
                    'email':user.email,
                    'cucaccount':user.cucaccount,
                    'created_on':user.created_on,
                    'last_login':user.last_login,
                    'valid':user.valid,
                    'last_login_ip':user.last_login_ip,
                    'avatar': "data:image/png;base64," + base64.b64encode(user.avatar).decode('ascii'),
                    'role':[role.name for role in user.role if role.valid]
                },
            },
            'success': True
        }