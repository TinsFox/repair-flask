"""
    Created by TinsFox on 2019-08-20.
"""
import hashlib
import random
import string
import time

import requests
from flask import current_app, json

from app.libs.error_code import AuthFailed

__author__ = 'TinsFox'


def randomID():
    id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return id


def generate_id(data):
    md = hashlib.md5()
    md.update(data.encode('utf8'))
    return md.hexdigest()


def getOpenID(code):
    appid = current_app.config['APP_ID']
    SECRET = current_app.config['APP_SECRET']
    errcode = {
        '-1': u'系统繁忙，此时请开发者稍候再试',
        '40029': u'code无效',
        '45011': u'频率限制，每个用户每分钟100次',
    }
    # 网络请求地址 Get方式 注意format里面的内容，传入了三个参数：AppID(小程序ID)、AppSecret(小程序密钥)、code
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
        appid, SECRET, code)
    r = requests.get(url)
    res = json.loads(r.text)
    if 'errcode' in res.keys() and res.get('errcode') != 0:
        raise AuthFailed(errcode[res.get('errcode')])
    return res

def get_order_code():
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    return order_no
