'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-12 21:41:22
FilePath: /server/app/managers/admin_manager/log_manager.py
'''
from datetime import datetime
from http import HTTPStatus
import re
from flask_restx import Namespace, Resource, fields, reqparse
from flask_restx.inputs import positive, regex, date_from_iso8601
from flask_jwt_extended import jwt_required, get_current_user
from app.managers.model import standardmodel
from app.utils.limiter import limiter

log_ns = Namespace('log', description='日志管理')
log_ns.models[standardmodel.name] = standardmodel
log_model = log_ns.model(
    'logmodel', {
        'remote_addr': fields.String(required=True, description='请求源IP地址'),
        'visit_time': fields.DateTime(required=True, description='访问时间'),
        'request_method': fields.String(required=True, description='请求方法'),
        'request_path': fields.String(required=True, description='请求路径'),
        'request_protocol': fields.String(required=True, description='请求协议'),
        'status': fields.Integer(required=True, description='返回状态码'),
        'http_referer': fields.String(required=True, description='HTTP来源'),
        'http_user_agent': fields.String(required=True, description='HTTP用户代理'),
    })
data_model = log_ns.model(
    'datamodel', {
        'logs': fields.List(fields.Nested(log_model)),
        'total': fields.Integer(required=True, description='总数'),
        'ips': fields.List(fields.String(required=True, description='全部IP地址'))
    })
model = log_ns.model(
    'loginfo', {
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
pagination_reqparser.add_argument('date',
                                  location='args',
                                  type=date_from_iso8601,
                                  default=datetime.today().strftime('%Y-%m-%d'),
                                  help='日期')
pagination_reqparser.add_argument('Authorization',
                                  type=str,
                                  location='headers',
                                  nullable=False,
                                  required=True,
                                  help='Authorization不能为空')


@log_ns.route('/loginfo')
@log_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@log_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@log_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class LogInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 发送nginx日志信息
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]
    @log_ns.expect(pagination_reqparser)
    @log_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 发送nginx日志信息
        param {*} self
        '''
        user = get_current_user()
        if '/log' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理nginx日志的权限', 'success': False}
        else:
            request_data = pagination_reqparser.parse_args()
            page = request_data.get('page')
            size = request_data.get('size')
            date = request_data.get('date')
            ip_addr = request_data.get('ip_addr')
            try:
                with open(f'/var/log/nginx/{date}.access.log', 'r+', encoding='utf-8') as file:
                    txt = file.read()
            except FileNotFoundError:
                return {'code': 1, 'message': '日志文件不存在', 'success': False}
            logs = re.findall(
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} ' +
                r'- \[\S*\] \{.*\} \d{3} ".*" \(Mozilla.*\)', txt)
            ips = list(
                set([
                    tmp for ip in re.findall(
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} - ', txt)
                    if (tmp := ip.split(' ')[0])
                ]))
            data = [{
                "remote_addr": ip_addr,
                "visit_time": re.findall(r'\[.*\]', log)[0].strip('[]'),
                "request_method": re.findall(r'\{.*\}', log)[0].split(' ')[0].strip('{'),
                "request_path": re.findall(r'\{.*\}', log)[0].split(' ')[1],
                "request_protocol": "HTTP/2.0",
                "status": int(re.findall(r' \d{3} ', log)[0].strip()),
                "http_referer": re.findall(r'".*"', log)[0].strip('"'),
                "http_user_agent": re.findall(r'\(Mozilla/.*\)', log)[0].strip('"')
            } for log in logs if log.split(' ')[0] == ip_addr] if ip_addr else [
                {
                    "remote_addr": log.split(' ')[0],
                    "visit_time": re.findall(r'\[.*\]', log)[0].strip('[]'),
                    "request_method": re.findall(r'\{.*\}', log)[0].split(' ')[0].strip('{'),
                    "request_path": re.findall(r'\{.*\}', log)[0].split(' ')[1],
                    "request_protocol": "HTTP/2.0",
                    "status": int(re.findall(r' \d{3} ', log)[0].strip()),
                    "http_referer": re.findall(r'".*"', log)[0].strip('"'),
                    "http_user_agent": re.findall(r'\(Mozilla/.*\)', log)[0].strip('"')
                } for log in logs
            ]
            total = len(data)
            data = data[(page - 1) * size:page * size]
            return {
                'code': 0,
                'message': 'success',
                'success': True,
                'data': {
                    'total': total,
                    'logs': data,
                    'ips': ips
                }
            }
