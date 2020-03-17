import uuid

from app.app_api import api
from app.decorate import check_params
from app.response import commit_callback, custom
from app.models import Account, db


# 注册账号
@api.route("/auth/register", methods=["POST"])
@check_params
def auth_register(phone, passwd, name):
    '''
    [
        {"name": "phone", "required": 1, "check": "string", "description": "手机号"},
        {"name": "passwd", "required": 1, "check": "string", "description": "密码"},
        {"name": "name", "required": 1, "check": "string", "description": "姓名"}
    ]
    '''
    # 是否注册过
    account = Account.query.filter_by(phone=phone).first()
    if account:
        return custom(-1, "该账号已注册")
    account = Account(
        phone=phone,
        passwd=Account.md5_passwd(passwd),
        name=name
    )
    db.session.add(account)

    def callback(param):
        return param.to_json()

    return commit_callback(callback=callback, param=(account, ))


# 账号登录
@api.route("/auth/login")
@check_params
def auth_login(phone, passwd):
    '''
    [
        {"name": "phone", "required": 1, "check": "string", "description": "手机号"},
        {"name": "passwd", "required": 1, "check": "string", "description": "密码"}
    ]
    '''
    account = Account.query.filter_by(phone=phone, passwd=Account.md5_passwd(passwd)).first()
    if not account:
        return custom(-1, "账户名或密码错误")
    account.api_token = uuid.uuid4().hex

    def callback(param):
        return param.to_json()

    return commit_callback(callback=callback, param=(account, ))


