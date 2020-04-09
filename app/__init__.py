# app初始化

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from config import config
from extend.api_duration import ApiDuration
from extend.mq import Rmq
from extend.op_logs import OperationLogs

db = SQLAlchemy()
redis = FlaskRedis()
api_duration = ApiDuration()
mq = Rmq()
op_logs = OperationLogs()

# 创建app
def create_app(env="default"):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    db.app = app
    redis.init_app(app)
    api_duration.init_app(app, db)
    mq.init_app(app)
    op_logs.init_app(app, db)

    # 注册蓝图
    from .app_api import api as blue_app_api
    app.register_blueprint(blue_app_api, url_prefix="/app_api")
    app.register_blueprint(blue_app_api, url_prefix="/%s/app_api" % app.config["PROJECT_NAME"])

    return app
