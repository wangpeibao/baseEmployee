# 装饰器部分


import functools
import json

from flask import request
from sqlalchemy.orm import joinedload
from werkzeug.local import LocalStack, LocalProxy

from app.models import Account, Employee
from app.response import custom

account_stack = LocalStack()
employee_stack = LocalStack()
enterprise_stack = LocalStack()

current_account = LocalProxy(lambda: account_stack.top)
current_employee = LocalProxy(lambda: employee_stack.top)
current_enterprise = LocalProxy(lambda: enterprise_stack.top)


def check_params(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func.__doc__:
            params = json.loads(func.__doc__)
            if request.method == "GET":
                for param in params:
                    status, msg, data = check_required_and_type(param, request.args.get(param["name"]))
                    if not status:
                        return custom(-1, msg)
                    kwargs[param["name"]] = data
            else:
                for param in params:
                    status, msg, data = check_required_and_type(param, request.form.get(param["name"]))
                    if not status:
                        return custom(-1, msg)
                    kwargs[param["name"]] = data
        return func(*args, **kwargs)
    return wrapper


# 验证必要参数和类型
def check_required_and_type(param, req):
    if param['required'] and not req:
        return False, "%s为必要参数" % param["name"], ""
    data = None
    if req is not None:
        return check_type(param, req)
    return True, "", data


# 验证类型
def check_type(param, req):
    status = True  # 默认状态是不通过
    if param["check"] == "int":
        try:
            req = int(req)
        except Exception as e:
            print(e)
            status = False
    if param["check"] == "float":
        try:
            req = float(req)
        except Exception as e:
            print(e)
            status = False
    if param["check"] == "json":
        try:
            req = json.loads(req)
        except Exception as e:
            print(e)
            status = False
    if not status:
        return False, "%s应该为%s格式" % (param["name"], param["check"]), req
    return status, "", req


# 验证登录状态
def verify_account(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        account_id = request.headers.get("AccountID", default=int)
        token = request.headers.get("Token")
        account = Account.query.filter_by(object_id=account_id, app_token=token).first()
        if not account:
            return custom(-99, "登录失效，请重新登录")
        account_stack.push(account)
        return func(*args, **kwargs)
    return wrapper


# 验证员工状态
def verify_employee(func):
    @verify_account
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        enterprise_id = request.headers.get("EnterpriseID", defualt=int)
        employee = Employee.query.options(
            joinedload(Employee.enterprise),
            joinedload(Employee.account)
        ).filter_by(
            enterprise_id=enterprise_id, account_id=current_account.object_id).first()
        if not employee:
            return custom(-100, "您不在该企业中")
        employee_stack.push(employee)
        enterprise_stack.push(employee.enterprise)
        return func(*args, **kwargs)
    return wrapper
