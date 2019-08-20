"""
    Created by TinsFox on 2019-08-19.
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

__author__ = 'TinsFox'


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class MiniForm(Form):
    code = StringField(validators=[DataRequired(message='not null')])


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


class CodeForm(Form):
    code = StringField(validators=[DataRequired(message='别问，你就是错了')])
    nickName = StringField()
    avatarUrl = StringField()
    gender = IntegerField()


class typeForm(Form):
    typeName = StringField(validators=[DataRequired(message='分类名称')])


class FaultListForm(Form):
    id = StringField(validators=[DataRequired(message='总类id')])
    faultTypeName = StringField(validators=[DataRequired(message='问题名称')])


class IDForm(Form):
    id = StringField(validators=[DataRequired(message="请输入ID")])


class SolutionForm(Form):
    id = StringField(validators=[DataRequired(message="请输入ID")])
    solutionBody = StringField(validators=[DataRequired(message="方案内容")])
