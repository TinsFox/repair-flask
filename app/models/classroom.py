"""
    Created by TinsFox on 2019-08-21.
"""
from app.models.base import Base, db
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, VARCHAR, Text

__author__ = 'TinsFox'


class Room(Base):
    id = Column(VARCHAR(100), primary_key=True)
    bNum = Column(VARCHAR(10), unique=True)
    lBum = Column(VARCHAR(10), unique=True)
    rNum = Column(VARCHAR(10), unique=True)
    classRoomId = Column(VARCHAR(10), unique=True)

    def keys(self):
        return ['id', 'bNum', 'lBum', 'classRoomId']

    @staticmethod
    def insert(id, data):
        """ 向数据库写入"""
        with db.auto_commit():
            fault = Room()
            fault.id = id
            fault.typeName = data
            db.session.add(fault)
