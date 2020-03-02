# 数据库基础类型
# 2019-11-29
# wangpeibao
from datetime import datetime

from sqlalchemy.ext.declarative import AbstractConcreteBase

from app import db


# 虚拟基础类
class Base(AbstractConcreteBase, db.Model):
    __no_table__ = True
    object_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, comment="")
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, index=True)
    is_valid = db.Column(db.Boolean, default=True, index=True)

    # 返回相应的数据映射
    def to_json(self):
        print(self)