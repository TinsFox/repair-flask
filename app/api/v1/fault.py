"""
    Created by TinsFox on 2019-08-19.
"""
import csv
import random
import string

import xlrd as xlrd
from flask import jsonify, g, request

from app.libs.error_code import DeleteSuccess, AuthFailed, DuplicateGift, Success, DuplicateTypeName, FileError, \
    EmptyError
from app.libs.helper import randomID, generate_id
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from app.models.fault import FaultType, FaultList, Solution
from app.validators.forms import typeForm, FaultListForm, IDForm, SolutionForm

__author__ = 'TinsFox'

api = Redprint('fault')


# 添加故障总类别
@api.route('/typeadd', methods=['POST'])
def typeadd():
    data = request.json
    if not data:
        raise EmptyError()
    for value in data.values():
        # print(value)
        # name = data['name']
        id = generate_id(value)
        if FaultType.query.filter_by(typeName=value).first():
            raise DuplicateTypeName()
        FaultType().insert(id, value)
    return Success(u'添加')


# 列出故障类别列表
@api.route('/typeshow', methods=['GET'])
def typeshow():
    fault = FaultType.query.filter().all()
    return jsonify(fault)


# 添加故障类型名称 such as 电脑没有声音
# 传入电脑类别id
# 故障类型名称
@api.route('/faultadd', methods=['POST'])
def faultadd():
    cout = 0
    data = request.json
    if not data:
        raise EmptyError()
    for val in data:
        id = val['id']  # 总分类
        newName = val['faultTypeName']
        fid = generate_id(newName)  # 随机生成的问题名称id
        is_had = FaultType.query.filter_by(id=id).first()  # 查询分类是否存在
        if not is_had:
            raise DuplicateTypeName(u'该分类不存在')
        fault = FaultList.query.filter_by(fid=fid, faultTypeName=newName).first()
        if fault:
            raise DuplicateTypeName()
        FaultList().insert(id, fid, newName)
        cout += 1
    print(cout)
    return Success(u'添加故障类型名称成功')


# 按照总分类传入的id返回
@api.route('/faultshow', methods=['GET'])
def faultshow():
    data = IDForm().validate_for_api()
    id = data.id.data
    faultListlt = FaultList.query.filter_by(id=id).all()
    return jsonify(faultListlt)


@api.route('/solutionadd', methods=['POST'])
def show1():
    data = SolutionForm().validate_for_api()
    id = data.id.data  # 问题的id
    solutionBody = data.solutionBody.data
    nameID = solutionBody[0:10]
    print(nameID)
    with db.auto_commit():
        FaultList().query.filter_by(id=id).first_or_404()
        solution = Solution.query.filter_by(solutionBody=solutionBody).first()
        if solution:
            raise DuplicateTypeName()
        s = Solution()
        s.id = generate_id(nameID)
        s.sid = id
        s.solutionBody = solutionBody
        db.session.add(s)
    return Success()


@api.route('/solution')
def solution():
    data = IDForm().validate_for_api()
    id = data.id.data
    s = Solution.query.filter_by(sid=id).all()
    return jsonify(s)


@api.route('/upload', methods=['POST'])
def file_upload():
    """
    # 文件上传
    # status: OVER
    :return:
    """
    # TODO文件上传
    success_count = 0
    file = request.files['file']
    if file and allowed_file(file.filename):
        data = xlrd.open_workbook(file_contents=file.read())
        print('sheet_names:', data.sheet_names())  # 获取所有sheet名字
        # print('sheet_number:', data.nsheets)  # 获取sheet数量
        # print('sheet_object:', data.sheets())  # 获取所有sheet对象
        # print('By_name:', data.sheet_by_name("test"))  # 通过sheet名查找
        # print('By_index:', data.sheet_by_index(3))  # 通过索引查找
    #     if data.sheet_loaded(data.sheet_names()[-1]):
    #         table = data.sheets()[0]
    #         if not isinstance(table.cell_value(0, 1), str):
    #             raise FileError()
    #         if '分类' not in table.cell_value(0, 1):
    #             raise FileError()
    #         for num in range(1, table.nrows):
    #             count = 1  # 第一列
    #             for row in table.row_values(num):
    #                 # id = None
    #                 if count == 1:
    #                     pass  # 序号列
    #                 elif count == 2:  # 社团列
    #                     id = randomID()
    #                     if not FaultType.query.filter_by(typeName=row).first():
    #                         FaultType.insert(row)
    #                 else:
    #                     if not row:
    #                         continue
    #                     society = FaultType.query.get(id)
    #                     if not FaultType.query.filter_by(typeName=row).first():
    #                         FaultType.insert(society, row)
    #                         success_count += 1
    #                 count += 1
    # else:
    #     raise FileError()
    # return Success()


def allowed_file(filename):
    """
    :param filename: 文件名
    :return: True or False
    """
    return '.' in filename and filename.split('.')[-1] in ['xls', 'csv']
