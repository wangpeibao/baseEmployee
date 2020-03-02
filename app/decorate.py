# 装饰器部分


import functools
import json

from flask import request, jsonify

from app.response import custom


def check_params(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params = json.loads(func.__doc__)["params"]
        if request.method == "GET":
            for param in params:
                status, msg, data = check_required_and_type(param, request.args.get(param["n"]))
                if not status:
                    return custom(-1, msg)
                kwargs[param["n"]] = data
        else:
            for param in params:
                status, msg, data = check_required_and_type(param, request.form.get(param["n"]))
                if not status:
                    return custom(-1, msg)
                kwargs[param["n"]] = data
        return func(*args, **kwargs)
    return wrapper


# 验证必要参数和类型
def check_required_and_type(param, req):
    if param['r'] and not req:
        if param["rm"]:
            return False, param["rm"], ""
        else:
            return False, "%s为必要参数" % param["n"], ""
    data = None
    if req is not None:
        return check_type(param, req)
    return True, "", data


# 验证类型
def check_type(param, req):
    status = True  # 默认状态是不通过
    if param["c"] == "int":
        try:
            req = int(req)
        except Exception as e:
            print(e)
            status = False
    if param["c"] == "float":
        try:
            req = float(req)
        except Exception as e:
            print(e)
            status = False
    if param["c"] == "json":
        try:
            req = json.loads(req)
        except Exception as e:
            print(e)
            status = False
    if not status:
        if param["cm"]:
            return False, param["cm"], req
        else:
            return False, "%s应该为%s格式" % (param["n"], param["c"]), req
    return status, "", req
