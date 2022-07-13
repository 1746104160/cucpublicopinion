'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-05 14:35:32
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 10:47:33
FilePath: /server/app/managers/admin_manager/news_manager.py
'''
from http import HTTPStatus
import time
import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Namespace, Resource, fields, reqparse
from flask_restx.inputs import positive, regex, datetime_from_iso8601, URL
from flask_jwt_extended import jwt_required, get_current_user
from app.utils.limiter import limiter
from app.utils.redisdb import redis
from app.model import News
from app.managers.model import standardmodel

datetime.datetime.now()
news_ns = Namespace('news', description='新闻管理')
news_ns.models[standardmodel.name] = standardmodel
news_model = news_ns.model(
    'newsmodel', {
        'newsid': fields.Integer(required=True, description='新闻id'),
        'title': fields.String(required=True, description='新闻标题'),
        'publish_time': fields.DateTime(required=True, description='发布时间'),
        'spider_time': fields.DateTime(required=True, description='爬取时间'),
        'author': fields.String(required=True, description='作者'),
        'articleSource': fields.String(required=True, description='新闻来源'),
        'article_url': fields.String(required=True, description='新闻链接'),
    })
data_model = news_ns.model(
    'datamodel', {
        'news': fields.List(fields.Nested(news_model)),
        'total': fields.Integer(required=True, description='总数')
    })
model = news_ns.model(
    'newsinfo', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(data_model, description='数据')
    })
content_data_model = news_ns.model('contentdatamodel',
                                   {'content': fields.String(required=True, description='新闻内容')})
content_model = news_ns.model(
    'contentmodel', {
        'code': fields.Integer(required=True, description='状态码'),
        'message': fields.String(required=True, description='状态信息'),
        'success': fields.Boolean(required=True, description='是否成功'),
        'data': fields.Nested(content_data_model, description='数据')
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
pagination_reqparser.add_argument('keyword', location='args', type=str, default='', help='关键词')
pagination_reqparser.add_argument('Authorization',
                                  type=str,
                                  location='headers',
                                  nullable=False,
                                  required=True,
                                  help='Authorization不能为空')


@news_ns.route('/newsinfo')
@news_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@news_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@news_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class NewsInfo(Resource):
    '''
    Author: 邵佳泓
    msg: 发送新闻信息
    '''
    decorators = [jwt_required(), limiter.limit('20/minute'), limiter.limit('1000/day')]

    @news_ns.expect(pagination_reqparser)
    @news_ns.marshal_with(model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 发送新闻信息
        param {*} self
        '''
        request_data = pagination_reqparser.parse_args()
        page = request_data.get('page')
        size = request_data.get('size')
        order = request_data.get('order')
        keyword = request_data.get('keyword')
        user = get_current_user()
        expire_time = int(
            time.mktime((datetime.date.today() + datetime.timedelta(days=1)).timetuple()))
        key = '/'.join(['newsinfo', order, str(page), str(size), keyword])
        length = News.query.count() if keyword == '' else News.query.filter(
            News.title.like('%' + keyword + '%')).count()
        if '/news' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理新闻的权限', 'success': False}
        elif (bytedata := redis.get(key)) and page != length // size + 1:
            data = eval(bytedata.decode('utf-8'))
            return {
                'code': 0,
                'message': '获取新闻信息成功',
                'success': True,
                'data': {
                    'news': data,
                    'total': length
                }
            }
        else:
            allnews = News.query.filter(News.title.like(f'%{keyword}%')).order_by(
                News.newsid.asc() if order == 'ascending' else News.newsid.desc()).paginate(
                    page, size, False).items
            data = [{
                'newsid': news.newsid,
                'title': news.title,
                'publish_time': news.publish_time,
                'spider_time': news.spider_time,
                'author': news.author,
                'articleSource': news.articleSource,
                'article_url': news.article_url
            } for news in allnews]
            pipe = redis.pipeline()
            pipe.set(key, str(data).encode('utf-8'))
            pipe.expireat(key, expire_time)
            pipe.execute()
            return {
                'code': 0,
                'message': '获取新闻信息成功',
                'success': True,
                'data': {
                    'news': data,
                    'total': length
                }
            }


newsdetailparser = reqparse.RequestParser(bundle_errors=True)
newsdetailparser.add_argument('newsid',
                              location='args',
                              type=positive,
                              required=True,
                              help='新闻id不能为空')
newsdetailparser.add_argument('Authorization',
                              type=str,
                              location='headers',
                              nullable=False,
                              required=True,
                              help='Authorization不能为空')


@news_ns.route('/content')
@news_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@news_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@news_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class NewsContent(Resource):
    '''
    Author: 邵佳泓
    msg: 获取新闻正文
    '''
    decorators = [jwt_required(), limiter.limit('10/minute'), limiter.limit('500/day')]

    @news_ns.expect(newsdetailparser)
    @news_ns.marshal_with(content_model)
    def get(self):
        '''
        Author: 邵佳泓
        msg: 获取新闻正文
        '''
        request_data = newsdetailparser.parse_args()
        newsid = request_data.get('newsid')
        user = get_current_user()
        if '/news' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理新闻的权限', 'success': False}
        else:
            news = News.query.filter_by(newsid=newsid).first()
            return {
                'code': 0,
                'message': '获取新闻正文成功',
                'success': True,
                'data': {
                    'content': news.content
                }
            }


updateparser = reqparse.RequestParser(bundle_errors=True)
updateparser.add_argument('newsid', type=positive, nullable=False, required=True, help='新闻ID不能为空')
updateparser.add_argument('title',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='新闻标题不能为空')
updateparser.add_argument('content',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='新闻内容不能为空')
updateparser.add_argument('publish_time',
                          type=datetime_from_iso8601,
                          nullable=False,
                          required=True,
                          help='发布时间不能为空')
updateparser.add_argument('spider_time',
                          type=datetime_from_iso8601,
                          nullable=False,
                          required=True,
                          help='爬取时间不能为空')
updateparser.add_argument('author',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='作者不能为空')
updateparser.add_argument('articleSource',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='文章来源不能为空')
updateparser.add_argument('article_url',
                          type=URL(check=True),
                          nullable=False,
                          required=True,
                          help='文章链接不能为空')
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


@news_ns.route('/update')
@news_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@news_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@news_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class UpdateNews(Resource):
    '''
    Author: 邵佳泓
    msg: 更新新闻数据
    '''
    decorators = [jwt_required(), limiter.limit('3/minute'), limiter.limit('100/day')]

    @news_ns.marshal_with(standardmodel)
    @news_ns.expect(updateparser)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 更新新闻数据
        param {*} self
        '''
        user = get_current_user()
        if '/news' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理新闻的权限', 'success': False}
        else:
            request_data = updateparser.parse_args()
            newsid = request_data.get('newsid')
            title = request_data.get('title')
            content = request_data.get('content')
            publish_time = request_data.get('publish_time')
            spider_time = request_data.get('spider_time')
            author = request_data.get('author')
            article_source = request_data.get('articleSource')
            article_url = request_data.get('article_url')
            news = News.query.filter_by(newsid=newsid)
            if news.first():
                news.update({
                    'title': title,
                    'content': content,
                    'publish_time': publish_time,
                    'spider_time': spider_time,
                    'author': author,
                    'articleSource': article_source,
                    'article_url': article_url
                })
                return {'code': 0, 'message': '更新新闻成功', 'success': True}
            else:
                return {'code': 1, 'message': '新闻不存在', 'success': False}


createparser = reqparse.RequestParser(bundle_errors=True)
createparser.add_argument('title',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='新闻标题不能为空')
createparser.add_argument('content',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='新闻内容不能为空')
createparser.add_argument('publish_time',
                          type=datetime_from_iso8601,
                          nullable=False,
                          required=True,
                          help='发布时间不能为空')
createparser.add_argument('spider_time',
                          type=datetime_from_iso8601,
                          nullable=False,
                          required=True,
                          help='爬取时间不能为空')
createparser.add_argument('author',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='作者不能为空')
createparser.add_argument('articleSource',
                          type=regex(pattern=r'\S+'),
                          nullable=False,
                          required=True,
                          help='文章来源不能为空')
createparser.add_argument('article_url',
                          type=URL(check=True),
                          nullable=False,
                          required=True,
                          help='文章链接不能为空')
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


@news_ns.route('/create')
@news_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@news_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@news_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class Createnews(Resource):
    '''
    Author: 邵佳泓
    msg: 导入新闻数据
    '''
    decorators = [jwt_required(), limiter.limit('3/minute'), limiter.limit('100/day')]

    @news_ns.marshal_with(standardmodel)
    @news_ns.expect(createparser)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 导入新闻数据
        param {*} self
        '''
        user = get_current_user()
        if '/news' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理新闻的权限', 'success': False}
        else:
            request_data = createparser.parse_args()
            title = request_data.get('title')
            if News.query.filter_by(title=title).first():
                return {'code': 1, 'message': '新闻已存在', 'success': False}
            else:
                content = request_data.get('content')
                publish_time = request_data.get('publish_time')
                spider_time = request_data.get('spider_time')
                author = request_data.get('author')
                article_source = request_data.get('articleSource')
                article_url = request_data.get('article_url')
                News.add(
                    News(title=title,
                         content=content,
                         publish_time=publish_time,
                         spider_time=spider_time,
                         author=author,
                         articleSource=article_source,
                         article_url=article_url))
                [
                    redis.delete(key) for key in redis.keys('newsinfo/desc/*')
                ]
                return {'code': 0, 'message': '导入新闻数据成功', 'success': True}


deleteparser = reqparse.RequestParser(bundle_errors=True)
deleteparser.add_argument('newsid', type=positive, nullable=False, required=True, help='新闻ID不能为空')
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


@news_ns.route('/delete')
@news_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.", standardmodel)
@news_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.", standardmodel)
@news_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), "visit too fast.", standardmodel)
class Deletenews(Resource):
    '''
    Author: 邵佳泓
    msg: 删除新闻
    '''
    decorators = [jwt_required(), limiter.limit('3/minute'), limiter.limit('100/day')]

    @news_ns.marshal_with(standardmodel)
    @news_ns.expect(deleteparser)
    def post(self):
        '''
        Author: 邵佳泓
        msg: 删除新闻
        param {*} self
        '''
        user = get_current_user()
        if '/news' not in [route for role in user.role for route in eval(role.authedroutes)]:
            return {'code': 1, 'message': '没有管理新闻的权限', 'success': False}
        else:
            request_data = deleteparser.parse_args()
            newsid = request_data.get('newsid')
            try:
                News.query.filter_by(newsid=newsid).delete()
                [
                    redis.delete(key) for key in redis.keys('newsinfo/*')
                ]
                return {'code': 0, 'message': '删除新闻成功', 'success': True}
            except SQLAlchemyError:
                return {'code': 2, 'message': '系统中有对该新闻的外键约束，不可删除', 'success': False}
