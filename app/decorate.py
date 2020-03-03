# 装饰器部分


import functools
import json

from flask import request, jsonify

from app.response import custom


def check_params(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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
        if param["required-msg"]:
            return False, param["required"], ""
        else:
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
        if param["check-msg"]:
            return False, param["check-msg"], req
        else:
            return False, "%s应该为%s格式" % (param["name"], param["check"]), req
    return status, "", req
