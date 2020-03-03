# 登录账户
from sqlalchemy import event

from app import db
from app.models.base import Base
from xpinyin import Pinyin

pinyin = Pinyin()


# 账户
class Account(Base):
    phone = db.Column(db.String(11), index=True, comment="用户手机号，登录账号", unique=True)
    passwd = db.Column(db.String(32), comment="用户名密码")
    name = db.Column(db.String(32), comment="用户账号名")
    pinyin = db.Column(db.String(100), comment="拼音名")

    def to_json(self, exclude_list=()):
        res = super(Account, self).to_json(exclude_list=["passwd"])
        return res


@event.listens_for(Account.name, "set")
def update_pinyin_name(*args):
    if args[1] != args[2]:
        print(args[1])
        try:
            args[0].pinyin = pinyin.get_pinyin(args[1], splitter="")
        except Exception as e:
            print(e)
            args[0].pinyin = ""
