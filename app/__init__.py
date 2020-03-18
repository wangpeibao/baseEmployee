# app初始化

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from extend.api_duration import ApiDuration

db = SQLAlchemy()
redis = FlaskRedis()
api_duration = ApiDuration()


# 创建app
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    db.app = app
    redis.init_app(app)
    api_duration.init_app(app, db)

    # 注册蓝图
    from .app_api import api as blue_app_api
    app.register_blueprint(blue_app_api, url_prefix="/app_api")

    return app
