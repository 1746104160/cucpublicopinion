'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-05 19:51:10
@FilePath: /server/app/managers/auth_manager/captcha_manager.py
'''
from http import HTTPStatus
import random
from flask_restx import Namespace,Resource,fields
from app.utils.requestid import requestid
from app.utils.redisdb import redis
from app.utils.limiter import limiter
import time
from captcha.image import ImageCaptcha
import io
import base64
CHAR_SET = [chr(ord('A')+i) for i in range(26)]+\
    [chr(ord('a')+i) for i in range(26)]+\
    [chr(ord('0')+i) for i in range(10)]
captcha_ns = Namespace('captcha', description='验证码')
data_model = captcha_ns.model('captchadata',{
    'captcha':fields.String(required=True,description='验证码')
})
model = captcha_ns.model('captcha',{
    'code': fields.Integer(required=True,description='状态码'),
    'message': fields.String(required=True,description='状态信息'),
    'success': fields.Boolean(required=True,description='是否成功'),
    'data':fields.Nested(model=data_model,required=True,description='数据')
})
@captcha_ns.route('/<float:id>')
@captcha_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@captcha_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@captcha_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast: 20/minute, 500/day.")
class Captcha(Resource):
    '''
    Author: 邵佳泓
    msg: 返回图片验证码
    '''
    decorators = [
        limiter.limit('20/minute'),
        limiter.limit('500/day')
    ]
    @captcha_ns.doc(params={'id': '避免浏览器缓存'})
    @captcha_ns.marshal_with(model)
    def get(self,id: float):
        random.seed(id)
        code = ''.join(random.sample(CHAR_SET, 4))
        image = ImageCaptcha().generate_image(code)
        image_byte = io.BytesIO()
        image.save(image_byte, format='png')
        value = code.encode('utf-8')
        expire_time = int(time.time()) + 300
        key = "captcha/" + str(requestid.id)
        p = redis.pipeline()
        p.set(key, value)
        p.expireat(key, expire_time)
        p.execute()
        return {
            "code": 0,
            "data": {
                "captcha": "data:image/png;base64," + base64.b64encode(image_byte.getvalue()).decode('ascii')
            },
            "success": True,
            "message": '获取图片验证码成功'
        }