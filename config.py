# 配置文件

import os
from datetime import timedelta

BASEDIR = os.path.abspath(os.path.dirname(__file__))


# 配置文件
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data.sqlite')
    SQLALCHEMY_ECHO = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    HOST = "127.0.0.1"
    PORT = 5000


config = {
    "dev": Config
}
