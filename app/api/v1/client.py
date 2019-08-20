"""
 Created by TinsFox on 2019-08-19.
"""
import requests
from flask import request, jsonify, json, current_app
from app.libs.error_code import ClientTypeError, Success, AuthFailed, DuplicateMini
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm, CodeForm, MiniForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException

__author__ = '七月'

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)


@api.route('/getcode', methods=['GET', 'POST'])
def getcode():
    # 获取微信小程序传入的code
    form = CodeForm().validate_for_api()
    return form.code.data


@api.route('/mini', methods=['POST'])
def mini_creat():
    form = CodeForm().validate_for_api()
    res = gotOpenID(form.code.data)
    openid = res['openid']
    userinfo = User.query.filter_by(openid=openid).first()
    if userinfo:
        return DuplicateMini()
    User.register_by_mini(openid, form.nickName.data, form.avatarUrl.data, form.gender.data)
    return Success()


def gotOpenID(code):
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
