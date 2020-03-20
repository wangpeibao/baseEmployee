# 部门相关接口
from app.app_api import api
from app.decorate import check_params, verify_employee, current_enterprise
from app.models import Department, db
from app.response import custom, commit_callback, success


@api.route("/department/create_department", methods=["POST"])
@check_params
@verify_employee
def department_create_department(parent_id, name):
    '''
    [
        {"name": "parent_id", "required": 1, "check": "int", "description": "父部门ID"},
        {"name": "name", "required": 1, "check": "string", "description": "部门名"}
    ]
    '''
    # 规定parent_id = -1时，是根部门
    if parent_id == -1:
        parent = Department.get_root_department(current_enterprise.object_id)
    else:
        parent = Department.query.filter(
            Department.enterprise_id == current_enterprise.object_id,
            Department.object_id == parent_id
        ).first()
        if not parent:
            return custom(-1, "部门不存在")
    department = Department(name=name, parent_id=parent.object_id, enterprise_id=current_enterprise.object_id)
    db.session.add(department)

    def callback(dep):
        return dep.to_json()

    return commit_callback(callback=callback, param=(department, ))


@api.route("/department/get_sub_department_list")
@check_params
@verify_employee
def department_get_department_list(department_id):
    '''
    [
        {"name": "department_id", "required": 1, "check": "int", "description": "父部门ID"}
    ]
    '''
    if department_id == -1:
        department = Department.get_root_department(current_enterprise.object_id)
    else:
        department = Department.query.filter(
            Department.enterprise_id == current_enterprise.object_id,
            Department.object_id == department_id
        ).first()
        if not department:
            return custom(-1, "参数错误")
    departments = Department.query.filter(
        Department.enterprise_id == current_enterprise.object_id,
        Department.parent_id == department.object_id
    ).all()
    return success(data=[dep.to_json() for dep in departments])
