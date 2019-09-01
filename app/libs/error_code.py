"""
    Created by TinsFox on 2019-08-19.
"""
from http.client import HTTPException

from app.libs.error import APIException
from flask import json

__author__ = 'TinsFox'


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ClientTypeError(APIException):
    # 400 401 403 404
    # 500
    # 200 201 204
    # 301 302
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'


class DuplicateTypeName(APIException):
    code = 400
    error_code = 2001
    msg = '分类已存在'


class EmptyError(APIException):
    code = 400
    error_code = 2001
    msg = '表单为空'


class DuplicateMini(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in mini'


class FileError(APIException):
    code = 400
    errcode = 4007
    msg = '文件格式不符合'


class ApiSuccess(APIException):
    @property
    def generate_body(self):
        t = {
            'code': self.errcode,
            'msg': self.message,
            'data':
                {
                    'list': []
                }
        }

        if self.data:
            t = dict(t, **{'data': {'list': self.data if isinstance(self.data, list) else [self.data]}})
        if self.others is not None and isinstance(self.others, dict):
            t['data'].update(self.others)
        return t


class Return(APIException):
    code = 200
    error_code = 0
    msg = "获取成功"
