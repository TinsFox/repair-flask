"""
    Created by TinsFox on 2019-08-20.
"""
import hashlib
import random
import string

__author__ = 'TinsFox'


def randomID():
    id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return id


def generate_id(data):
    md = hashlib.md5()
    md.update(data.encode('utf8'))
    return md.hexdigest()
