# 组织架构信息
from sqlalchemy import event
from sqlalchemy.ext.declarative.base import declared_attr

from app import db
from .base import Base

class Account(Base):
    phone = db.Column(db.String(11), index=True, comment="用户手机号，登录账号")
    passwd = db.Column(db.String(32), comment="用户名密码")
    name = db.Column(db.String(32), comment="用户账号名")
    pinyin = db.Column(db.String(100), comment="拼音名")


# @event.listens_for()
