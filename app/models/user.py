"""
 Created by 七月 on 2018/5/11.
"""
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm, TEXT, VARCHAR
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

__author__ = '七月'


class User(Base):
    # 数据表字段
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(100), unique=True)
    studentID = Column(VARCHAR(100), unique=True)
    openid = Column(VARCHAR(100), unique=True)
    nickname = Column(VARCHAR(100))
    auth = Column(SmallInteger, default=1)
    avatarUrl = Column(TEXT)
    gender = Column(SmallInteger)
    phone = Column(VARCHAR(100))
    _password = Column('password', String(100))

    # 序列化返回字段
    def keys(self):
        return ['id', 'email', 'nickname', 'auth', 'avatarUrl', 'studentID', 'phone']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    # 邮箱注册
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    # 小程序注册
    def register_by_mini(openid, nickname, avatarUrl, gender):
        with db.auto_commit():
            user = User()
            user.openid = openid
            user.nickname = nickname
            user.avatarUrl = avatarUrl
            user.gender = gender
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']
