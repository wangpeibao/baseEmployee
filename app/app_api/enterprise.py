from app import db
from app.app_api import api
from app.decorate import check_params, verify_login
from app.models import Enterprise, Employee, DepartmentMem
from app.response import commit_callback
from app.decorate import current_account


@api.route("/enterprise/create_enterprise", methods=["POST"])
@check_params
@verify_login
def enterprise_create_enterprise(name):
    '''
    [
        {"name": "name", "required": 1, "check": "string", "description": "企业名"}
    ]
    '''
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

