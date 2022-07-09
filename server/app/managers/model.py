'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-07 01:11:45
LastEditors: 邵佳泓
LastEditTime: 2022-07-09 12:02:37
FilePath: /server/app/managers/model.py
'''
from flask_restx import Model,fields
standardmodel = Model('standardresponse', {
    'code': fields.Integer(required=True, description='状态码',default=999),
    'message': fields.String(required=True, description='状态信息'),
    'success': fields.Boolean(required=True, description='是否成功',default=False),
})
