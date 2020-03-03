import uuid
from datetime import datetime

from sqlalchemy.ext.declarative import AbstractConcreteBase, declared_attr

from app import db


def gen_id():
    return uuid.uuid4().hex


# 返回数据库映射
class JSONBaseMixin(object):
    def to_json(self, exclude_list=()):
        d = dict()
        d['object_name'] = self.__class__.__name__
        for col in self.__table__.columns:
            col_name = col.name
            if col_name in exclude_list:
                continue
            value = getattr(self, col_name)
            if value is None:
                pass
            else:
                if isinstance(col.type, db.DateTime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(col.type, db.Date):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(col.type, db.Time):
                    value = value.strftime('%H:%M:%S')
                elif isinstance(col.type, db.DECIMAL):
                    value = float(value)
            d[col_name] = value
        return d


# 虚拟基础类
class Base(AbstractConcreteBase, db.Model, JSONBaseMixin):
    __abstract__ = True

    object_id = db.Column(db.String(32), primary_key=True, nullable=False, default=gen_id, comment="主键")
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, index=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
