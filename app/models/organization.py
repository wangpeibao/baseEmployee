# 登录账户
import hashlib

from sqlalchemy import event
from sqlalchemy_mptt import BaseNestedSets

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
    app_token = db.Column(db.String(32), comment="app登录token")

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

    def __init__(self, *args, **kwargs):
        super(Enterprise, self).__init__(*args, **kwargs)
        # 给企业创建一个根部门
        root_department = Department(name="根部门")
        db.session.add(root_department)
        self.departments.append(root_department)


# 员工(账号-企业的关系表)
class Employee(Base):
    account_id = db.Column(db.Integer, db.ForeignKey("account.object_id"))
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprise.object_id"))
    is_owner = db.Column(db.Boolean, default=False)  # 标记位，是否是企业的创建者


Employee.enterprise = db.relationship("Enterprise", backref="employees")
Employee.account = db.relationship("Account", backref="employees")


# 部门（无限极）
class Department(Base, BaseNestedSets):
    sqlalchemy_mptt_pk_name = "object_id"

    name = db.Column(db.String(32), default="未命名")
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprise.object_id"))

    @staticmethod
    def get_root_department(enterprise_id):
        root = Department.query.filter(
            Department.enterprise_id == enterprise_id,
            Department.parent_id == None
        ).first()
        return root

Department.enterprise = db.relationship("Enterprise", backref="departments")


# 部门－员工关系
class DepartmentMem(Base):
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.object_id"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.object_id"))
    is_manager = db.Column(db.Boolean, default=0, comment="是否是部门负责人")


DepartmentMem.employee = db.relationship("Employee", backref="department_members")
DepartmentMem.department = db.relationship("Department", backref="department_members")

