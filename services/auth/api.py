# services/auth/api.py

from datetime import datetime, timedelta

from flask import request

from app.db import db
from models import Users
from services import check_keys
from services.auth import auth_bp
from utils.auth import check_password, get_jwt
from utils.db import fetch_first
from utils.exceptions import AuthenticationError
from utils.http import success

TTL = 60 * 60 * 2  # 2 hours expired


@auth_bp.route("/api/login", methods=["POST"])
def login():
    req_body = request.get_json()
    req_keys = ("username", "password")
    check_keys(req_keys, req_body)

    username = req_body["username"]
    password = req_body["password"]
    user_info = fetch_first(
        db.session.query(Users.id.label("user_id"), Users.username, Users.password)
        .filter_by(username=username)
        .first()
    )
    if not user_info:
        raise AuthenticationError("User not found!")

    if not check_password(password, user_info.pop("password")):
        raise AuthenticationError("Wrong password!")

    user_info["user_id"] = str(user_info["user_id"])

    user_info["exp"] = datetime.now() + timedelta(seconds=TTL)
    token = get_jwt(user_info)
    user_info["token"] = token
    user_info.pop("exp")

    return success(
        user_info,
        "Login successfull",
        header={"Authorization": token},
        status_code=201,
    )
