from utils.exceptions import APIError


def check_keys(
    req_keys, container, exc: Exception = APIError, error_msg: str = "Bad request"
):
    """Checks whether all the keys are in the container."""
    missing_keys = [key for key in req_keys if key not in container]
    if missing_keys:
        raise exc(error_msg, data={"missing_keys": missing_keys})
    _check_empty_keys(req_keys, container, exc=exc, error_msg=error_msg)


def _check_empty_keys(
    keys: tuple,
    container: dict,
    exc: Exception = APIError,
    error_msg: str = "Bad request",
):
    """Checks whether some of the values are empty."""
    empty_keys = [key for key in keys if container[key] in ("", None, [])]
    if empty_keys:
        raise exc(error_msg, data={"empty_keys": empty_keys})
