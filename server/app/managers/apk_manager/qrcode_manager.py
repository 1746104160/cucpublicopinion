'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-14 14:45:04
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 14:58:08
FilePath: /server/app/managers/apk_manager/qrcode_manager.py
'''
import base64
from http import HTTPStatus
import io
import qrcode
from flask_restx import Namespace, Resource, fields
from app.managers.model import standardmodel

qrcode_ns = Namespace('qrcode', description='获取APK二维码')
qrcode_ns.models[standardmodel.name] = standardmodel
data_model = qrcode_ns.model('qrcodedata',
                             {'qrcode': fields.String(required=True, description='验证码')})
model = qrcode_ns.model(
    'qrcode', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(model=data_model, required=True, description='数据')
    })


@qrcode_ns.route('/<string:version>')
@qrcode_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@qrcode_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@qrcode_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class Qrcode(Resource):
    '''
    Author: 邵佳泓
    msg: 获取最新的二维码
    '''
    @qrcode_ns.doc('getqrcode')
    @qrcode_ns.marshal_with(model)
    def get(self, version):
        '''
        Author: 邵佳泓
        msg: 获取最新的二维码
        '''
        code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        code.add_data(f'https://software.mcl913.top/apk/{version}')
        code.make(fit=True)
        img = code.make_image()
        image_byte = io.BytesIO()
        img.save(image_byte, format='png')
        image_byte.seek(0)
        return {
            'code': 0,
            'message': '获取APK二维码成功',
            'success': True,
            'data': {
                'qrcode':
                "data:image/png;base64," +  base64.b64encode(image_byte.getvalue()).decode('ascii')
            }
        }
