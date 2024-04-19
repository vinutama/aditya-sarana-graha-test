# services/users/api.py

from flask import jsonify, request

import config
from app.db import db
from models import Users
from services import check_keys
from services.users import user_bp
from utils import logger
from utils.auth import hash_password
from utils.exceptions import APIError
from utils.http import success


@user_bp.route("/api/user/create", methods=["POST"])
def user_register():
    req_body = request.get_json()
    req_keys = ("username", "password")
    check_keys(req_keys, req_body)

    reqs = {
        "username": req_body["username"],
        "password": hash_password(req_body["password"]),
    }
    try:
        user = Users(**reqs)
        db.session.add(user)
        db.session.commit()
        return success(user.to_json(), "User created")
    except Exception as e:
        db.session.rollback()
        raise APIError(f"Database Error: {e}")
