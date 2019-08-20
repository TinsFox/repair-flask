"""
    Created by TinsFox on 2019-08-19.
"""
from enum import Enum

__author__ = 'TinsFox'


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201
