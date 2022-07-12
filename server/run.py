'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-13 01:06:30
FilePath: /server/run.py
'''
import datetime
import pandas as pd
from flask_script import Manager
from sqlalchemy import create_engine
from instance.config import SQLALCHEMY_DATABASE_URI
from app import create_app
from app.utils.mysqldb import db
from app.model import Users, Roles

app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    '''
    Author: 邵佳泓
    msg: 创建数据库
    '''
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    db.drop_all()
    db.create_all()
    standard = Roles(name='standard', description='只拥有主页可视化大屏的权限')
    vip = Roles(name='vip',
                description='拥有新闻管理的权限',
                authedroutes="['/personal','/news','/security','/log']")
    admin = Roles(name='admin',
                  description='拥有系统的全部权限',
                  authedroutes="['/personal','/news','/security','/log','/dashboard']")
    Roles.add(vip)
    Roles.add(admin)
    Roles.add(standard)
    user = Users(name="shaojh",
                 email="1746104160@qq.com",
                 role=[vip],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="vip用户")
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="normal",
                 email="s2019302120001@cuc.edu.cn",
                 role=[standard],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="standard用户")
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="administrator",
                 email="sjh1746104160@gmail.com",
                 role=[admin],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="admin用户")
    user.set_password("Aa123456")
    Users.add(user)
    for i in range(1, 10):
        test = Roles(name=f'test{i}', description=f'测试{i}')
        Roles.add(test)
        user = Users(name=f"testuser{i}",
                     email=f"test{i}@cuc.edu.cn",
                     role=[test],
                     cucaccount="2019302120001",
                     created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     last_login_ip='127.0.0.1',
                     description=f"test{i}用户" if i < 5 else None)
        user.set_password("Aa123456")
        Users.add(user)
    pd.read_csv('spider.csv').dropna().to_sql('news',engine,if_exists='append',index=False)
    print('db create ok!')


@manager.command
def update_db():
    '''
    Author: 邵佳泓
    msg: 更新数据库
    '''
    db.create_all()
    standard = Roles(name='standard', description='只拥有主页可视化大屏的权限')
    vip = Roles(name='vip',
                description='拥有新闻管理的权限',
                authedroutes="['/personal','/news','/security','/log']")
    admin = Roles(name='admin',
                  description='拥有系统的全部权限',
                  authedroutes="['/personal','/news','/security','/log','/dashboard']")
    Roles.add(vip)
    Roles.add(admin)
    Roles.add(standard)
    user = Users(name="shaojh",
                 email="1746104160@qq.com",
                 role=[vip],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="vip用户")
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="normal",
                 email="s2019302120001@cuc.edu.cn",
                 role=[standard],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="standard用户")
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="administrator",
                 email="sjh1746104160@gmail.com",
                 role=[admin],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login_ip='127.0.0.1',
                 description="admin用户")
    user.set_password("Aa123456")
    Users.add(user)
    for i in range(1, 10):
        test = Roles(name=f'test{i}', description=f'测试{i}')
        Roles.add(test)
        user = Users(name=f"testuser{i}",
                     email=f"test{i}@cuc.edu.cn",
                     role=[test],
                     cucaccount="2019302120001",
                     created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     last_login_ip='127.0.0.1',
                     description=f"test{i}用户" if i < 5 else None)
        user.set_password("Aa123456")
        Users.add(user)

if __name__ == '__main__':
    manager.run()
