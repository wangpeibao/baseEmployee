from app import db
from app.app_api import api
from app.decorate import check_params, verify_account, verify_employee, current_enterprise
from app.models import Enterprise, Employee, DepartmentMem
from app.response import commit_callback, custom, commit
from app.decorate import current_account


@api.route("/enterprise/create_enterprise", methods=["POST"])
@check_params
@verify_account
def enterprise_create_enterprise(name):
    '''
    [
        {"name": "name", "required": 1, "check": "string", "description": "企业名"}
    ]
    '''
    # 名字不可重复
    enterprise = Enterprise.query.filter_by(name=name).first()
    if enterprise:
        return custom(-1, "该名字已存在")

    enterprise = Enterprise(name=name)
    db.session.add(enterprise)
    employee = Employee(account_id=current_account.object_id, is_owner=True)
    employee.enterprise = enterprise
    # 员工与根部门的关系
    dep_mem = DepartmentMem()
    dep_mem.employee = employee
    dep_mem.department = enterprise.departments[0]
    db.session.add(dep_mem)

    def callback(eme):
        return eme.to_json()

    return commit_callback(callback=callback, param=(employee, ))


# 更新企业信息
@api.route("/enterprise/update_enterprise_info", methods=["POST"])
@check_params
@verify_employee
def enterprise_update_enterprise_info(name):
    '''
        [
            {"name": "name", "required": 1, "check": "string", "description": "企业名"}
        ]
    '''
    if name != current_enterprise.name:  # 修改名字
        has_enterprise = Enterprise.query.filter_by(name=name).first()
        if has_enterprise:
            return custom(-1, "企业名已经被占用")
        current_enterprise.name = name
    return commit()


# 退出企业
@api.route("/enterprise/quit_enterprise", methods=["POST"])
@verify_employee
def enterprise_quit_enterprise():
    pass