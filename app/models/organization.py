# 登录账户
import hashlib

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

    @staticmethod
    def md5_passwd(passwd):
        passwd += "wangpeibao"
        m = hashlib.md5()
        m.update(passwd.encode("iso-8859-1"))
        return m.hexdigest()


@event.listens_for(Account.name, "set")
def update_pinyin_name(*args):
    if args[1] != args[2]:
        print(args[1])
        try:
            args[0].pinyin = pinyin.get_pinyin(args[1], splitter="")
        except Exception as e:
            print(e)
            args[0].pinyin = ""


# 企业
class Enterprise(Base):
    name = db.Column(db.String(32), index=True, unique=True, comment="企业名称")


# 员工(账号-企业的关系表)
class Employee(Base):
    account_id = db.Column(db.String(32), db.ForeignKey("account.object_id"))
    enterprise_id = db.Column(db.String(32), db.ForeignKey("enterprise.object_id"))


Employee.enterprise = db.relationship("Enterprise", backref="employees", foreign_keys="Enterprise.object_id")
Employee.account = db.relationship("Account", backref="employees", foreign_keys="Account.object_id")