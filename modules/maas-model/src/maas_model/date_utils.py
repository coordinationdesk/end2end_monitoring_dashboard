"""Functions about ZULU date management """

import datetime

import dateutil.parser

__all__ = ["datetime_to_zulu", "datestr_to_zulu", "datestr_to_utc_datetime"]


def datetime_to_zulu(datetime_object: datetime.datetime | None) -> str | None:
    """Format a dateime object to ZULU format

    Args:
        datetime_object (datetime.datetime): datetime to format

    Returns:
        str: zulu formatted string or None if datetime_object is None
    """
    if datetime_object is None:
        return None
    return datetime_object.strftime("%04Y-%02m-%02dT%02H:%02M:%02S.%f")[:-3] + "Z"


def datestr_to_zulu(date_str: str | None) -> str | None:
    """Convert a iso datetime string to ZULU format compatible with MAAS

    Args:
        date_str (str): an iso string

    Returns:
        str: zulu formatted string or None if date_str is None
    """
    if date_str is None:
        return None
    return datetime_to_zulu(datestr_to_utc_datetime(date_str))


def datestr_to_utc_datetime(date_str: str | None) -> datetime.datetime | None:
    """Convert a iso datetime string to utc datetime object

    Args:
        date_str (str): an iso string

    Returns:
        datetime.datetime: utc datetime object or None if date_str is None
    """
    if date_str is None:
        return None
    return dateutil.parser.isoparse(date_str).astimezone(dateutil.tz.UTC)
