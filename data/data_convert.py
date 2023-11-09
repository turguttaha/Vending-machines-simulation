from datetime import datetime


def convert_date_str_to_timestamp(date_str):
    assert isinstance(date_str, str), f"Expected a string but got {type(date_str)} with value {date_str}"
    date_datetime = datetime.strptime(date_str, "%Y/%m/%d")
    return date_datetime.timestamp()

