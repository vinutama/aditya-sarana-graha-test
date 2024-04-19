from flask import Blueprint

user_bp = Blueprint("users", __name__)

from services.users import api
