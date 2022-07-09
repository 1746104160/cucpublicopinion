'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-10 01:02:02
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
        db.LargeBinary(length=2048),
        default=blob,
        nullable=False,
    )
    last_login_ip = db.Column(
        db.String(50),
        nullable=True,
    )
    description = db.Column(db.String(255))
    # favorites = db.relationship('Favorites', backref='user', lazy='dynamic')
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
    authedroutes = db.Column(db.String(255), nullable=False, default="['/personal']")
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
    # fav = db.relationship('Favorites', uselist=False, back_populates="news")
    # comments = db.relationship('Comments', backref='news', lazy='dynamic')

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

# class Favorites(db.Model):
#     '''
#     Author: 邵佳泓
#     msg: 喜好信息表
#     '''
#     __tablename__ = 'favorite'
#     favid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     userid = db.Column(db.Integer(), db.ForeignKey('user.userid'), nullable=False)
#     newsid = db.Column(db.Integer(), db.ForeignKey('news.newsid'), nullable=False)
#     news = db.relationship('News', uselist=False, back_populates="fav")

#     @classmethod
#     def add(cls, fav):
#         '''
#         Author: 邵佳泓
#         msg: 添加收藏
#         param {*} cls
#         param {*} user
#         '''
#         db.session.add(fav)
#         db.session.commit()


# class Comments(db.Model):
#     '''
#     Author: 邵佳泓
#     msg: 评论信息表
#     '''
#     __tablename__ = 'comment'
#     commentid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     userid = db.Column(db.Integer(), db.ForeignKey('user.userid'), nullable=False)
#     newsid = db.Column(db.Integer(), db.ForeignKey('news.newsid'), nullable=False)
#     content = db.Column(db.String(255), nullable=False)
#     comment_time = db.Column(db.DateTime, nullable=False)
#     replies = db.relationship('Replies', backref='comment', lazy='dynamic')

#     @classmethod
#     def add(cls, comment):
#         '''
#         Author: 邵佳泓
#         msg: 添加评论
#         param {*} cls
#         param {*} user
#         '''
#         db.session.add(comment)
#         db.session.commit()


# class Replies(db.Model):
#     '''
#     Author: 邵佳泓
#     msg: 回复信息表
#     '''
#     __tablename__ = 'reply'
#     replyid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     responder_id = db.Column(db.Integer(), db.ForeignKey('user.userid'), nullable=False)
#     reviewer_id = db.Column(db.Integer(), db.ForeignKey('user.userid'), nullable=False)
#     commentid = db.Column(db.Integer(), db.ForeignKey('comment.commentid'), nullable=False)
#     content = db.Column(db.String(255), nullable=False)
#     reply_time = db.Column(db.DateTime, nullable=False)

#     @classmethod
#     def add(cls, reply):
#         '''
#         Author: 邵佳泓
#         msg: 添加回复
#         param {*} cls
#         param {*} user
#         '''
#         db.session.add(reply)
#         db.session.commit()
