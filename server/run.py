'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 19:43:25
FilePath: /server/run.py
'''
from flask_script import Manager
from app import create_app
from app.utils.mysqldb import db

app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    '''
    Author: 邵佳泓
    msg: 创建数据库
    '''
    # db.drop_all()
    db.create_all()
    print('db create ok!')

if __name__ == '__main__':
    manager.run()
