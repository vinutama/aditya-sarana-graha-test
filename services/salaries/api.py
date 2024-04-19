# services/salaries/api.py
# services/users/api.py

from flask import request

from app.db import db
from models import Salaries
from services import check_keys
from services.salaries import salary_bp
from utils import logger
from utils.auth import authenticate
from utils.db import fetch_data, fetch_first
from utils.exceptions import DatabaseError, NotFoundError
from utils.http import success


@salary_bp.route("/api/salary/create", methods=["POST"])
@authenticate()
def add_salary():
    req_body = request.get_json()
    req_keys = ("salary", "emp_id", "from_date", "to_date")
    check_keys(req_keys, req_body)

    reqs = {
        "salary": req_body["salary"],
        "emp_id": req_body["emp_id"],
        "from_date": req_body["from_date"],
        "to_date": req_body["to_date"],
    }
    try:
        salary = Salaries(**reqs)
        db.session.add(salary)
        db.session.commit()
        return success(salary.to_json(), "Salary created")
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(e)


# @salary_bp.route("/api/salary/update/<employee_id>", methods=["PUT"])
# @authenticate()
# def update_salary(employee_id: str):
#     req_body = request.get_json()
#     update_salary_employee = fetch_first(
#         db.session.query(
#             Salaries.id.label("salary_id"), Salaries.username, Salaries.password
#         )
#         .filter_by(username=username)
#         .first()
#     )
#     if not updated_employee:
#         raise NotFoundError(f"Employee with id : {employee_id} does not exist!")
#     try:
#         for k, v in req_body.items():
#             if hasattr(updated_employee, k):
#                 setattr(updated_employee, k, v)

#         db.session.commit()
#         return success(None, "Employee updated", status_code=204)
#     except Exception as e:
#         db.session.rollback()
#         raise DatabaseError(e)
