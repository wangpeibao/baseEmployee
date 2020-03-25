# 记录sql查询时间和接口访问时间
from datetime import datetime
from flask import request, current_app
from flask_sqlalchemy import get_debug_queries


class ApiDuration(object):
    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db

    def init_app(self, app, db):  # 初始化，根据需求到是否
        self.app = app
        self.db = db

        # API接口响应时间
        class ApiTime(db.Model):

            __table_args__ = {"extend_existing": True}

            object_id = db.Column(db.Integer, primary_key=True)
            create_time = db.Column(db.DateTime, default=datetime.now)
            path = db.Column(db.String(100))
            duration = db.Column(db.Integer)
            sql_count = db.Column(db.Integer, default=0)

        @self.app.before_request
        def insert_start_time():
            request.start_time = datetime.now().timestamp()

        @self.app.after_request
        def get_request_time(response):
            if current_app.config["DEBUG"]:
                length = datetime.now().timestamp() - request.start_time
                api = ApiTime(path=request.path, duration=int(length * 1000), sql_count=len(get_debug_queries()))
                db.session.add(api)
                db.session.commit()
            return response