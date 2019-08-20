"""
    Created by TinsFox on 2019-08-19.
"""
from app.models.base import Base, db
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, VARCHAR, Text
import datetime

__author__ = 'TinsFox'


class FaultType(Base):
    id = Column(VARCHAR(100), primary_key=True)
    typeName = Column(VARCHAR(100))

    # 序列化返回字段
    def keys(self):
        return ['id', 'typeName', 'create_time']

    @staticmethod
    def insert(id, data):
        """ 向数据库写入"""
        with db.auto_commit():
            fault = FaultType()
            fault.id = id
            fault.typeName = data
            db.session.add(fault)


class FaultList(Base):
    id = Column(VARCHAR(100))
    fid = Column(VARCHAR(100), primary_key=True)
    faultTypeName = Column(VARCHAR(100))

    @staticmethod
    def insert(id, fid, faultTypeName):
        """ 向数据库写入"""
        with db.auto_commit():
            fault = FaultList()
            fault.id = id
            fault.fid = fid
            fault.faultTypeName = faultTypeName
            db.session.add(fault)

    def keys(self):
        return ['id', 'faultTypeName', 'create_time']


class Solution(Base):
    id = Column(VARCHAR(100), primary_key=True)
    sid = Column(VARCHAR(100), unique=True)
    solutionBody = Column(Text)

    @staticmethod
    def insert(id, sid, solutionBody):
        with db.auto_commit():
            solution = Solution()
            solution.id = id
            solution.sid = sid
            solution.solutionBody = solutionBody
            db.session.add(solution)

    def keys(self):
        return ['id', 'solutionBody', 'create_time']
