from app.app_api import api
from app.decorate import check_params
from app.response import success, commit_callback
from app.models import Account, db


# 注册账号
@api.route("/auth/register", methods=["POST"])
@check_params
def auth_register(**data):
    '''
    [
        {"name": "phone", "required": 1, "required-msg": "", "check": "string", "check-msg": "", "description": "手机号"},
        {"name": "passwd", "required": 1, "required-msg": "", "check": "string", "check-msg": "", "description": "密码"},
        {"name": "name", "required": 1, "required-msg": "", "check": "string", "check-msg": "", "description": "姓名"}
    ]
    '''
    # 是否注册过

    account = Account(
        phone=data["phone"],
        passwd=data["passwd"],
        name=data["name"]
    )
    db.session.add(account)

    def callback(account):
        return account.to_json()

    return commit_callback(callback=callback, param=(account, ))


@api.route("/auth/login")
@check_params
def auth_login(**data):
    '''
    [
        {}
    ]
    '''
    print(data.get('phone'))
    return success()
