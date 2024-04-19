from typing import Dict, List

from sqlalchemy import Row


def fetch_first(row: Row) -> Dict:
    if not row:
        return None
    return row._asdict()


def fetch_data(rows: List[Row]) -> List:
    if not rows:
        return []
    result = []
    for row in rows:
        # convert class object to dict
        row_dict = vars(row)
        # exclude internal class atts
        row_dict = {k: v for k, v in row_dict.items() if not k.startswith("_")}
        result.append(row_dict)
    return result
