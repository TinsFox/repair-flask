"""
 Created by 七月 on 2018/5/26.
"""
from sqlalchemy import Column, String, Integer, orm, VARCHAR, TEXT

from app.models.base import Base, db

__author__ = '七月'


class Order(Base):
    id = Column(VARCHAR(200), primary_key=True)
    roomid = Column(VARCHAR(100))
    phone = Column(VARCHAR(100))
    content = Column(TEXT)
    equipment = Column(VARCHAR(100))
    openid = Column(VARCHAR(100))
    uuid = Column(VARCHAR(100))

    def keys(self):
        return ['id', 'roomid', 'phone', 'content', 'equipment', 'uuid', 'status', 'create_time']

    @staticmethod
    def insert(data):
        """ 向数据库写入"""
        with db.auto_commit():
            order = Order()
            order.id = data['id']
            order.roomid = data['roomid']
            order.phone = data['phone']
            order.content = data['content']
            order.equipment = data['equipment']
            order.openid = data['openid']
        db.session.add(order)
