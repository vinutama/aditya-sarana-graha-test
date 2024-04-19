# utils/auth.py

from functools import wraps
from os import environ

import bcrypt
import jwt
from flask import request as flask_request

from services import check_keys
from utils import logger
from utils.exceptions import AuthenticationError

# required keys to be encoded/decoded for login and check_token
AUTH_FIELDS = ("user_id", "username", "exp")


def hash_password(password: str) -> str:
    password = password.encode()
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pw.decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    """Checks if the password is right.

    Args:
        password {[type]} -- [description]
        hashed {[type]} -- [description]
    """
    if type(password) is str:
        password = password.encode()
    if type(hashed) is str:
        hashed = hashed.encode()

    return bcrypt.checkpw(password, hashed)


# using [] instead of get so it auto raises if no secret is set
JWT_SECRET = environ["JWT_SECRET"]


def parse_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        logger.info(f"DECODED: {decoded}")
        return {key: decoded.get(key) for key in AUTH_FIELDS}
    except jwt.exceptions.InvalidTokenError as e:
        raise AuthenticationError(f"Your session has expired, please re-login: {e}")


def get_jwt(payload: dict) -> str:
    try:
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    except Exception as e:
        raise AuthenticationError(f"Can't encode payload: {e}")


def decode_token(token: str) -> dict:
    """Decodes token from request and returns user info.

    Args:
        token: JWT token from login

    Returns:
        A dict containing user information
        {
            "user_id": current user ID,
            "username": username of the current user
        }

    Raises:
        APIError: Error related to Flask request.
        AuthenticationError: Error related to user authentication.
    """

    user_info = parse_jwt(token)
    logger.info(f"USER INFO: {user_info}")
    check_keys(AUTH_FIELDS, user_info, exc=AuthenticationError)

    user_info.pop("exp")

    return user_info


def get_token(request=None) -> dict:
    """Returns the authorization from a given Flask request.

    If the request is not given, it fetches the current one via flask.request.
    """
    if not request:
        request = flask_request
    header = request.headers
    if not header:
        raise AuthenticationError("Header is empty")
    return header.get("Authorization")


def authenticate():
    """Decorator to authenticate endpoint methods.

    Must be used within application context as we are using Flask's
    current_app functionality.
    """

    def wrap_f(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            decode_token(get_token())

            return f(*args, **kwargs)

        return wrapper

    return wrap_f
