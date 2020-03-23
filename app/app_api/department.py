# 部门相关接口
from sqlalchemy.orm import joinedload

from app.app_api import api
from app.decorate import check_params, verify_employee, current_enterprise
from app.models import Department, db, Employee, DepartmentMem
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


# 获取部门树
@api.route("/department/get_department_tree")
@check_params
@verify_employee
def department_get_department_tree():
    departments = Department.get_department_tree(current_enterprise.object_id)
    return success(data=[dep.to_json() for dep in departments])


# 获取子部门信息列表
@api.route("/department/get_sub_department_list")
@check_params
@verify_employee
def department_get_department_list(department_id, get_employee_info, sub_department_count, sub_employee_count,
                                   all_sub_department_count, all_sub_employee_count):
    '''
    [
        {"name": "department_id", "required": 1, "check": "int", "description": "父部门ID"},
        {"name": "get_employee_info", "required": 0, "check": "bool", "description": "是否包含当前部门员工信息"},
        {"name": "sub_department_count", "required": 0, "check": "bool", "description": "部门信息包含一级子部门数"},
        {"name": "sub_employee_count", "required": 0, "check": "bool", "description": "部门信息包含一级子员工数"},
        {"name": "all_sub_department_count", "required": 0, "check": "bool", "description": "部门信息包含所有子部门数"},
        {"name": "all_sub_employee_count", "required": 0, "check": "bool", "description": "部门信息包含所有子员工数"}
    ]
    '''
    if department_id == -1:
        department = Department.get_root_department()
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
    department_info = []
    for department in departments:
        res = department.to_json()
        if sub_department_count:
            res["sub_department_count"] = department.get_sub_department_query().count()
        if sub_employee_count:
            res["employee_count"] = department.get_current_employees_query().count()
        if all_sub_department_count:
            res["all_sub_department_count"] = department.get_all_sub_department_query().count()
        if all_sub_employee_count:
            res["all_employee_count"] = department.get_all_employees_query().count()
        department_info.append(res)
    employee_info = []
    if get_employee_info:
        depmems = DepartmentMem.query.options(joinedload(DepartmentMem.employee).joinedload(Employee.account)).filter(
            DepartmentMem.department_id == department.object_id
        ).all()
        for depmem in depmems:
            employee_info.append(depmem.to_json())
    return success(data={"department_info": department_info, "employee_info": employee_info})


# 删除部门
@api.route("/department/delete_department", methods=["POST"])
@check_params
@verify_employee
def department_delete_department(department_id, force):
    '''
    [
        {"name": "department_id", "required": 1, "check": "int", "description": "部门ID"},
        {"name": "force", "required": 0, "check": "bool", "description": "是否强制删除"}
    ]
    '''
    pass


