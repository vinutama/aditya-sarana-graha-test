# utils/http.py

import json
from typing import Dict, List, Union

from flask.json import dumps


def success(
    data=Union[Dict, List], message: str = "", header: dict = {}, status_code: int = 200
):
    return (
        dumps(
            {"data": data, "message": message}, cls=json.JSONEncoder, sort_keys=False
        ),
        status_code,
        {**header, "Content-Type": "application/json; charset=utf-8"},
    )


def fail(e: Exception):
    error_dict = {"error": e.incident_number, "message": e.message}
    if e.data:
        error_dict["data"] = e.data
    return (
        dumps(error_dict, cls=json.JSONEncoder, sort_keys=False),
        e.status_code,
        {"Content-Type": "application/json; charset=utf-8"},
    )
