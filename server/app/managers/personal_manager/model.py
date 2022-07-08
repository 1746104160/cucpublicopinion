'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-07 01:11:45
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-07 01:11:52
@FilePath: /server/app/managers/personal_manager/model.py
'''
from flask_restx import Model,fields
model = Model('standardresponse', {
    'code': fields.Integer(required=True, description='状态码'),
    'message': fields.String(required=True, description='状态信息'),
    'success': fields.Boolean(required=True, description='是否成功'),
})
