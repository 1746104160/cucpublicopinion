'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-14 13:24:07
FilePath: /server/app/model.py
'''
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.default_avatar import blob
from app.utils.mysqldb import db


class User2Role(db.Model):
    '''
    Author: 邵佳泓
    msg: 用户角色关系表
    '''
    __tablename__ = 'user2role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userid'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.roleid'))

    @classmethod
    def add(cls, user2role):
        '''
        Author: 邵佳泓
        msg: 添加用户角色关系
        param {*} cls
        param {*} user
        '''
        db.session.add(user2role)
        db.session.commit()


class Users(db.Model):
    '''
    Author: 邵佳泓
    msg: 用户信息表
    '''

    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    password = db.Column(
        db.String(200),
        nullable=False,
    )
    email = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )
    cucaccount = db.Column(db.String(15), )
    created_on = db.Column(
        db.DateTime,
        nullable=False,
    )
    last_login = db.Column(
        db.DateTime,
        nullable=False,
    )
    valid = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )
    avatar = db.Column(
        db.LargeBinary(length=(2**24)-1),
        default=blob,
        nullable=False,
    )
    last_login_ip = db.Column(
        db.String(50),
        nullable=True,
    )
    description = db.Column(db.String(255))
    role = db.relationship('Roles',
                           secondary='user2role',
                           backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password: str):
        '''
        Author: 邵佳泓
        msg: 设置用户密码
        param {*} self
        param {str} password
        '''
        self.password = generate_password_hash(password, method='sha512')

    def check_password(self, password: str):
        '''
        Author: 邵佳泓
        msg: 检查用户密码
        param {*} self
        param {str} password
        '''
        return check_password_hash(self.password, password)

    @classmethod
    def add(cls, user):
        '''
        Author: 邵佳泓
        msg: 添加用户
        param {*} cls
        param {*} user
        '''
        db.session.add(user)
        db.session.commit()


class Roles(db.Model):
    '''
    Author: 邵佳泓
    msg: 角色信息表
    '''
    __tablename__ = 'role'
    roleid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    authedroutes = db.Column(db.String(255), nullable=False, default="['/personal','/version']")
    description = db.Column(db.String(255))
    valid = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    @classmethod
    def add(cls, role):
        '''
        Author: 邵佳泓
        msg: 添加角色
        param {*} cls
        param {*} user
        '''
        db.session.add(role)
        db.session.commit()


class News(db.Model):
    '''
    Author: 邵佳泓
    msg: 新闻信息表
    '''
    __tablename__ = 'news'
    newsid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    publish_time = db.Column(
        db.DateTime,
        nullable=False,
    )
    spider_time = db.Column(
        db.DateTime,
        nullable=False,
    )
    author = db.Column(db.String(50), nullable=False)
    articleSource = db.Column(db.String(50), nullable=False)
    article_url = db.Column(db.String(255), nullable=False)

    @classmethod
    def add(cls, news):
        '''
        Author: 邵佳泓
        msg: 添加新闻
        param {*} cls
        param {*} news
        '''
        db.session.add(news)
        db.session.commit()

class SenAna(db.Model):
    '''
    Author: 赵润泽
    msg: 新闻情感分析表
    '''
    __tablename__ = "sen_ana"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    newsid = db.Column(db.Integer(),db.ForeignKey('news.newsid'),nullable=False)
    attitude = db.Column(db.String(10), nullable=False)
    news = db.relationship("News",backref=db.backref("sen_ana",uselist=False),uselist=False)

    @classmethod
    def add(cls, sen_ana):
        '''
        Author: 赵润泽
        msg: 新闻情感表
        param {*} cls
        param {*} news
        '''
        db.session.add(sen_ana)
        db.session.commit()

class HotWord(db.Model):
    '''
    Author: 令狐晓玉
    msg: 热词表
    '''
    __tablename__ = 'hot_word'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    hot_word = db.Column(db.String(25),nullable=False)
    hot = db.Column(db.Float(), nullable=False)

    @classmethod
    def add(cls, hot_word):
        '''
        Author: 令狐晓玉
        msg: 热词表
        param {*} cls
        param {*} news
        '''
        db.session.add(hot_word)
        db.session.commit()

class NewsCluster(db.Model):
    '''
    Author: 邬语丝
    msg: 新闻聚类表
    '''
    __tablename__ = "news_cluster"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    newsid = db.Column(db.Integer(),db.ForeignKey('news.newsid'),nullable=False)
    category = db.Column(db.Integer(), nullable = False) # 簇标号
    topic_words = db.Column(db.String(100),nullable=False)
    news = db.relationship("News",backref=db.backref("news_cluster",uselist=False),uselist=False)


    @classmethod
    def add(cls, news_cluster):
        '''
        Author: 邬语丝
        msg: 聚类表
        param {*} cls
        param {*} news
        '''
        db.session.add(news_cluster)
        db.session.commit()

class NewsClass(db.Model):
    '''
    Author: 朱俊杰
    msg: 新闻分类表
    '''
    __tablename__ = "news_class"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    newsid = db.Column(db.Integer(),db.ForeignKey('news.newsid'),nullable=False)
    category = db.Column(db.String(20), nullable = False)
    news = db.relationship("News",backref=db.backref("news_class",uselist=False),uselist=False)

    @classmethod
    def add(cls, news_class):
        '''
        Author: 朱俊杰
        msg: 新闻分类表
        param {*} cls
        param {*} ews_class
        '''
        db.session.add(news_class)
        db.session.commit()

class PostNum(db.Model):
    '''
    Author: 朱俊杰
    msg: 发布数量表
    '''
    __tablename__ = "post_num"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    articleSource = db.Column(db.String(50), nullable=False)
    num = db.Column(db.Integer(), nullable = False)

    @classmethod
    def add(cls, post_num):
        '''
        Author: 朱俊杰
        msg: 发布数量表
        param {*} cls
        param {*} post_num
        '''
        db.session.add(post_num)
        db.session.commit()
