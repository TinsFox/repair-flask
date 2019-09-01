"""
    Created by TinsFox on 2019-08-26.
"""
from flask import jsonify, g

from app.libs.error_code import Success, Return, NotFound
from app.libs.exceptions.base import ViewSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.order import Order
from app.validators.forms import OrderForm, AcceptForm
from app.libs.helper import generate_id, getOpenID, get_order_code

__author__ = 'TinsFox'

api = Redprint('order')


@api.route('/add', methods=['POST'])
def add():
    form = OrderForm().validate_for_api()
    content = form.content.data
    id = generate_id(content[0:10])
    t = get_order_code()
    code = form.code.data
    res = getOpenID(code)
    openid = res['openid']
    with db.auto_commit():
        order = Order()
        order.id = id
        order.roomid = form.roomid.data  # 课室 A1-201
        order.content = form.content.data  # 故障描述
        order.equipment = form.equipment.data  # 设备类型
        order.phone = form.phone.data  # 电话
        order.openid = openid
        db.session.add(order)
    return Success(msg=u'报修成功')


# 未接订单
@api.route('/list', methods=['GET'])
@auth.login_required
def dislist():
    order = Order().query.filter_by(status=1).all()
    return ViewSuccess(msg=u'获取成功', data=order)


# status: 1 未接
# status: 3 已接
# status: 4 已完成

@api.route('/accept', methods=['patch'])
@auth.login_required
def accept():
    # 传入订单号 修改status、写入接单人id
    form = AcceptForm().validate_for_api()
    orderID = form.id.data
    uid = g.user.uid
    with db.auto_commit():
        order = Order().query.filter_by(id=orderID, status=1).first()
        if order:
            order.uuid = uid
            order.status = 3
            db.session.add(order)
    # return jsonify(uid)
    return Success(msg=u'接单成功')


@api.route('/finsh', methods=['patch'])
@auth.login_required
def finsh():
    # 传入订单号 修改status
    form = AcceptForm().validate_for_api()
    orderID = form.id.data
    uid = g.user.uid
    with db.auto_commit():
        order = Order().query.filter_by(id=orderID, status=3, uuid=uid).first()
        if order:
            order.status = 4
            db.session.add(order)
    # return jsonify(uid)
    return Success(msg=u'订单完成')


# 我的未完成订单
@api.route('/mylist', methods=['GET'])
@auth.login_required
def mylist():
    uid = g.user.uid
    order = Order().query.filter_by(status=3, uuid=uid).all()
    return ViewSuccess(msg=u'未完成订单列表', data=order)


# 已完成订单列表
@api.route('/myfinsh', methods=['GET'])
@auth.login_required
def myfinsh():
    uid = g.user.uid
    order = Order().query.filter_by(status=4, uuid=uid).all()
    return ViewSuccess(msg=u'已完成订单列表', data=order)


# 他人订单
@api.route('/other', methods=['GET'])
@auth.login_required
def other():
    uid = g.user.uid
    order = Order().query.filter(Order.uuid != uid).all()
    return ViewSuccess(msg=u'他人订单', data=order)
