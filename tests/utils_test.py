from datetime import datetime, timezone
from typing import Optional

import pytest
from flask import Flask

from app import utils
from app.exceptions.exceptions import MissingPayloadException


def test_get_utc_time_returns_datetime():
    result: datetime = utils.get_utc_time()

    assert isinstance(result, datetime)
    assert result.tzinfo == timezone.utc


def test_str_to_bool_or_none_accepts_none():
    result: Optional[bool] = utils.str_to_bool_or_none(None)

    assert result is None


@pytest.mark.parametrize(
    "input_string",
    [
        "true",
        "TRUE",
        "trUE",
        "TRue"
    ]
)
def test_str_to_bool_or_none_accepts_valid_true_string(input_string: str):
    result: Optional[bool] = utils.str_to_bool_or_none(input_string)

    assert result


@pytest.mark.parametrize(
    "input_string",
    [
        "false",
        "FALSE",
        "False",
        "fALSE",
        "falsE"
    ]
)
def test_str_to_bool_or_none_accepts_valid_false_string(input_string: str):
    result: Optional[bool] = utils.str_to_bool_or_none(input_string)

    assert not result


def test_str_to_bool_or_none_raises_exception_on_invalid_string():
    with pytest.raises(ValueError):
        utils.str_to_bool_or_none("asdbkhujab")


def test_str_to_int_or_none_accepts_none():
    result: Optional[int] = utils.str_to_int_or_none(None)

    assert result is None


@pytest.mark.parametrize(
    "input_string",
    [
        "0",
        "-100",
        "100",
        "123",
        "9" * 100
    ]
)
def test_str_to_int_or_none_accepts_valid_int(input_string: str):
    result: Optional[int] = utils.str_to_int_or_none(input_string)

    assert isinstance(result, int)
    assert int(input_string) == result


def test_str_to_int_or_none_raises_exception_on_invalid_string():
    with pytest.raises(ValueError):
        utils.str_to_int_or_none("zero")


def test_str_to_datetime_or_none_accepts_none():
    result: Optional[datetime] = utils.str_to_datetime_or_none(None)

    assert result is None


@pytest.mark.parametrize(
    "input_string",
    [
        "2020-01-01 00:00:00",
        "2021-06-16 12:12:12",
        "2022-01-01 00:00:00",
        "1992-09-21 12:34:56",
    ]
)
def test_str_to_datetime_or_none_accepts_valid_datatime(input_string: str):
    result: Optional[datetime] = utils.str_to_datetime_or_none(input_string)

    assert isinstance(result, datetime)


@pytest.mark.parametrize(
    "input_string",
    [
        "20-01-01 00:00:00",
        "2020-001-16 12:12:12",
        "2022-01-001 00:00:00",
        "0000-01-01 00:00:00",
        "2022-13-01 00:00:00",
        "2022-01-50 00:00:00",
        "1992-09-21 24:34:56",
        "1992-09-21 11:60:56",
        "1992-09-21 14:34:60",
    ]
)
def test_str_to_datetime_or_none_raises_exception_on_invalid_data(input_string: str):
    with pytest.raises(ValueError):
        utils.str_to_datetime_or_none(input_string)


def test_get_payload_with_json():
    app = Flask(__name__)

    test_data = {"key": "value"}

    with app.test_request_context("/", json=test_data):
        payload: dict = utils.get_payload()

        assert payload == test_data


def test_get_payload_without_json():
    app = Flask(__name__)

    with app.test_request_context("/", json=None):
        with pytest.raises(MissingPayloadException):
            utils.get_payload()
