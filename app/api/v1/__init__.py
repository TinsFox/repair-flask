"""
    Created by TinsFox on 2019-08-19.
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token, gift, fault, room, order

__author__ = 'TinsFox'


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    fault.api.register(bp_v1)
    room.api.register(bp_v1)
    order.api.register(bp_v1)
    return bp_v1
