from app.app_api import api
from app.decorate import check_params
from app.response import success


# 注册账号
@api.route("/auth/register", methods=["POST"])
@check_params
def auth_register(**data):
    print(data)
    return success()


@api.route("/auth/login")
@check_params
def auth_login(**data):
    '''
    '''
    print(data.get('phone'))
    return success()
