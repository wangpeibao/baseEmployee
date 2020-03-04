from flask import jsonify

from app import db


def success(msg="", data=""):
    response = jsonify({'code': 200, 'msg': msg, 'data': data})
    response.status_code = 200
    return response


def custom(code=-1, msg="", data=""):
    response = jsonify({'code': code, 'msg': msg, 'data': data})
    response.status_code = 200
    db.session.rollback()
    return response


def commit(msg="", data=""):
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return custom(-999, "系统异常")
    return success(msg=msg, data=data)


def commit_callback(msg="", callback=None, param=()):
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return custom(-999, "系统异常")
    return success(msg, callback(*param))
