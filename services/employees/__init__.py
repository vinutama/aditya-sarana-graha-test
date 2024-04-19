from flask import Blueprint

employees_bp = Blueprint("employees", __name__)

from services.employees import api
