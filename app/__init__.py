# app/__init__.py
import inspect
import os

from flask import Flask

import utils.exceptions as exc
from app.db import db
from config import DevelopmentConfig, ProductionConfig
from services.auth import auth_bp
from services.employees import employees_bp
from services.salaries import salary_bp
from services.users import user_bp
from utils import logger
from utils.http import fail

_blueprints = (auth_bp, employees_bp, salary_bp, user_bp)

KNOWN_EXCEPTIONS = [e for _, e in inspect.getmembers(exc, inspect.isclass)]


def initiate_tables(db):
    db.create_all()


def create_app(config_class: str = None):
    app = Flask(__name__)
    config_class_mapper = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
    }
    if config_class is None:
        config_class = config_class_mapper[os.environ.get("DEPLOYMENT_TYPE", "dev")]
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        initiate_tables(db)

        for blueprint in _blueprints:
            try:
                app.register_blueprint(blueprint)
            except AssertionError:
                logger.warning(f"API {blueprint} already registered")

    @app.errorhandler(Exception)
    def handle_error(e: Exception):
        # rollback the session on catching Exception
        if type(e) in KNOWN_EXCEPTIONS:
            return fail(e)
        return fail(exc.UnhandledError(f"Unknown error: {e}"))

    return app
