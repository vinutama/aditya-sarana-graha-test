# services/users/api.py

from flask import request

from app.db import db
from models import Employees, Salaries
from services import check_keys
from services.employees import employees_bp
from utils import logger
from utils.auth import authenticate
from utils.db import fetch_data, fetch_first
from utils.exceptions import DatabaseError, NotFoundError
from utils.http import success


@employees_bp.route("/api/employees/create", methods=["POST"])
@authenticate()
def add_employee():
    req_body = request.get_json()
    req_keys = ("firstname", "lastname", "birthdate")
    check_keys(req_keys, req_body)

    reqs = {
        "firstname": req_body["firstname"],
        "lastname": req_body["lastname"],
        "birthdate": req_body["birthdate"],
    }
    try:
        employee = Employees(**reqs)
        db.session.add(employee)
        db.session.commit()
        return success(employee.to_json(), "Employee created")
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(e)


@employees_bp.route("/api/employees/get", methods=["GET"])
@authenticate()
def get_employees():
    employees = fetch_data(db.session.query(Employees).all())
    return success(employees, "Employee retieved")


@employees_bp.route("/api/employees/get/<employee_id>", methods=["GET"])
@authenticate()
def get_employee_detail(employee_id: str):
    query = (
        db.session.query(
            Employees.firstname,
            Employees.lastname,
            Employees.birthdate,
            Salaries.salary,
            Salaries.from_date,
            Salaries.to_date,
        )
        .join(Salaries, Employees.id == Salaries.emp_id)
        .filter(Salaries.emp_id == employee_id)
        .first()
    )
    employee = fetch_first(query)
    logger.info(f"GET Employees: {employee}")

    return success(employee, "Employee retieved")


@employees_bp.route("/api/employees/update/<employee_id>", methods=["PUT"])
@authenticate()
def update_employee(employee_id: str):
    req_body = request.get_json()
    updated_employee = Employees.query.get(employee_id)
    if not updated_employee:
        raise NotFoundError(f"Employee with id : {employee_id} does not exist!")
    try:
        for k, v in req_body.items():
            if hasattr(updated_employee, k):
                setattr(updated_employee, k, v)

        db.session.commit()
        return success(None, "Employee updated", status_code=204)
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(e)


@employees_bp.route("/api/employees/delete/<employee_id>", methods=["DELETE"])
@authenticate()
def delete_employee(employee_id: str):
    deleted_employee = Employees.query.get(employee_id)
    if not deleted_employee:
        raise NotFoundError(f"Employee with id : {employee_id} does not exist!")
    try:
        db.session.delete(deleted_employee)
        db.session.commit()
        return success(None, "Employee deleted")
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(e)
