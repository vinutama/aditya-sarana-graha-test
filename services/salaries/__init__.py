from flask import Blueprint

salary_bp = Blueprint("salaries", __name__)

from services.salaries import api
