'''
@Descripttion: 业务管理系统
@version: 1.0.0
@Author: 邵佳泓
@Date: 2022-07-05 13:02:48
@LastEditors: 邵佳泓
@LastEditTime: 2022-07-08 00:17:09
@FilePath: /server/run.py
'''
from app import create_app
from flask_script import Manager
from app.utils.mysqldb import db
from app.model import *
import datetime
app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    standard = Roles(name='standard', description='只拥有主页可视化大屏的权限')
    vip = Roles(name='vip', description='拥有新闻管理的权限', authedroutes="['/personal','/news']")
    admin = Roles(name='admin', description='拥有系统的全部权限', authedroutes="['/personal','/dashboard']")
    Roles.add(vip)
    Roles.add(admin)
    Roles.add(standard)
    user = Users(name="shaojh", email="1746104160@qq.com", role=[vip],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="normal", email="2019302120001@cuc.edu.cn", role=[standard],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user.set_password("Aa123456")
    Users.add(user)
    user = Users(name="administrator", email="sjh1746104160@gmail.com", role=[admin],
                 created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user.set_password("Aa123456")
    Users.add(user)
    for i in range(1, 10):
        test = Roles(name=f'test{i}', description=f'测试{i}')
        Roles.add(test)
        user = Users(name=f"testuser{i}", email=f"test{i}@cuc.edu.cn", role=[test], cucaccount="2019302120001",
                     created_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user.set_password("Aa123456")
        Users.add(user)
    print('db create ok!')


if __name__ == '__main__':
    manager.run()
