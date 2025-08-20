from datetime import datetime, timezone
from typing import Optional

from flask import request

from app.exceptions.exceptions import MissingPayloadException


def get_utc_time() -> datetime:
    return datetime.now(timezone.utc)


def str_to_bool_or_none(string: Optional[str]) -> Optional[bool]:
    if string is None:
        return None

    string_lower: str = string.lower()

    if string_lower == "true":
        return True
    elif string_lower == "false":
        return False
    else:
        raise ValueError(f"Cannot convert {string_lower} to bool")


def str_to_int_or_none(string: Optional[str]) -> Optional[int]:
    if string is None:
        return None

    return int(string)


def str_to_datetime_or_none(string: Optional[str]) -> Optional[datetime]:
    if string is None:
        return None

    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def get_payload() -> dict:
    payload: Optional[dict] = request.get_json()

    if payload is None:
        raise MissingPayloadException()

    return payload