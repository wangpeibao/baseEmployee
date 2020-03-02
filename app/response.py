from flask import jsonify


def success(msg="", data=""):
    response = jsonify({'code': 200, 'msg': msg, 'data': data})
    response.status_code = 200
    return response


def custom(code=-1, msg="", data=""):
    response = jsonify({'code': code, 'msg': msg, 'data': data})
    response.status_code = 200
    return response


