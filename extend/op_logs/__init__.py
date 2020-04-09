# 操作日志扩展模块
# 期望实现两个方面，一个基于数据的方法，一个是基于ElasticSearch实现的查询
from datetime import datetime


class OperationLogs(object):
    def __init__(self):
        self.app = None
        self.db = None
        self.store_type = None  # 目前只支持本地数据库模式和ElasticSearch模式

    def init_app(self, app, db=None):
        self.app = app
        self.db = db

        class OpLogs(db.Model):  # 定义的操作日志model
            __table_args__ = {"extend_existing": True}

            object_id = db.Column(db.Integer, primary_key=True)
            create_time = db.Column(db.DateTime, default=datetime.now)
            platform = db.Column(db.Integer, default=0, comment="操作平台")
            module = db.Column(db.Integer, default=0, comment="所在模块")
            title = db.Column(db.String(32), nullable=False, comment="操作名")
            conent = db.Column(db.Text, nullable=False, comment="具体的操作内容")

