import uuid
from datetime import datetime

from flask import current_app
from sqlalchemy.ext.declarative import AbstractConcreteBase, declared_attr

from app import db, redis


def gen_id():  # 根据redis+snowflake生成自增分布式ID
    ms = int(datetime.now().timestamp() * 1000)
    seq_id = redis.incr(ms)
    redis.expire(ms, 2)
    seq_id = seq_id % 4096
    ms = ms << 17
    work_id = current_app.config["WORK_ID"]  # 只有容纳0-31台服务
    work_id = work_id << 12
    # 合并成long字长的整数
    ms += ms + work_id + seq_id
    return ms


def gen_uuid():  # 生成uuid主键
    return uuid.uuid4().hex

# 数据库自增主键


# 虚拟基础类
class Base(AbstractConcreteBase, db.Model):
    __abstract__ = True

    object_id = db.Column(db.BigInteger, primary_key=True, nullable=False, default=gen_id, comment="主键")
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, index=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

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
