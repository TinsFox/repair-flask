"""
 Created by TinsFox on 2019-08-19.
"""
import requests
from flask import request, jsonify, json, current_app
from app.libs.error_code import ClientTypeError, Success, AuthFailed, DuplicateMini
from app.libs.helper import getOpenID
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


"""
    小程序登录


    Args:
        code
        userinfo

    Returns:
        data:{
            error_code: 0
            msg: "ok"
            request: "POST /v1/client/mini"
            }
    """


@api.route('/mini', methods=['POST'])
def mini_creat():
    form = CodeForm().validate_for_api()
    res = getOpenID(form.code.data)
    openid = res['openid']
    userinfo = User.query.filter_by(openid=openid).first()
    if userinfo:
        return DuplicateMini()
    User.register_by_mini(openid, form.nickName.data, form.avatarUrl.data, form.gender.data)
    return Success()
