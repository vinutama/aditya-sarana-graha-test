# utils/exceptions.py

from uuid import uuid4


class BaseException(Exception):
    status_code = 500
    _default_msg = "Unknown error"

    def __init__(self, message=None, data=None):
        super().__init__(message)
        self.incident_number = str(uuid4())
        if message is None:
            message = self._default_msg
        self.message = message
        self.data = data


class APIError(BaseException):
    """Raises when a request payload of an API call is incomplete/invalid.

    Possible cases:
        - empty or missing key-values
        - invalid data type
    """

    status_code = 400


class AuthenticationError(BaseException):
    """Raises when a user is not authenticated.

    Typically, user should be prompted to relog-in.
    """

    status_code = 401


class NotFoundError(BaseException):
    """Raises when a data is not found."""

    status_code = 404


class DatabaseError(BaseException):
    """Raises when error on DB-related"""

    status_code = 500


class UnhandledError(BaseException):
    """Raises unhandled cases."""
