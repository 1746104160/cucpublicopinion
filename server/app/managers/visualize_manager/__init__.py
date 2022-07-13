'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-07 01:41:28
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 18:33:46
FilePath: /server/app/managers/visualize_manager/__init__.py
'''
from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended.exceptions import JWTExtendedException
from app.managers.visualize_manager.category_manager import category_ns
from app.managers.visualize_manager.cluster_manager import cluster_ns
from app.managers.visualize_manager.hotword_manager import hotword_ns
from app.managers.visualize_manager.postnum_manager import postnum_ns
from app.managers.visualize_manager.sentiment_manager import sentiment_ns
visualize = Blueprint("visualize", __name__, url_prefix='/visualize/news')
api = Api(visualize, version='1.0', title='Visualize API',description='Visualize',doc='/swagger/')
api.add_namespace(category_ns,path='/category')
api.add_namespace(cluster_ns,path='/cluster')
api.add_namespace(hotword_ns,path='/hotword')
api.add_namespace(postnum_ns,path='/postnum')
api.add_namespace(sentiment_ns,path='/sentiment')
@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    """
    If the error is a JWT error, return a 401 response with the error message
    :param error: The error that was raised
    """
    return {'message': str(error)}, getattr(error, 'code', 401)
