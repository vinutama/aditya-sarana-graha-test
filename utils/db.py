from typing import List

from sqlalchemy import Row


def fetch_first(row: Row) -> dict:
    if not row:
        return None
    return row._asdict()


def fetch_data(rows: List[Row]) -> List:
    if not rows:
        return []
    return [row._asdict() for row in rows]
