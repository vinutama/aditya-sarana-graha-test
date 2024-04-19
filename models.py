# app/models.py
import uuid

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db import db


class Base(db.Model):
    """Base class for default tables.

    This class determines ground rules that must be satisfied by all tables.
    """

    __abstract__ = True

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Users(Base):
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Employees(Base):
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(Date, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Salaries(Base):
    emp_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    salary = db.Column(Integer, nullable=False)
    from_date = db.Column(Date, nullable=False)
    to_date = db.Column(Date, nullable=False)
