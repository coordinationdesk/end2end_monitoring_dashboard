"""Contains ZuluDate class field"""

__all__ = ["ZuluDate"]

import datetime

import dateutil.parser
import dateutil.tz
from opensearchpy import Date


class ZuluDate(Date):
    """Custom field to serialize / serialize date in ZULU format"""

    name = "zuludate"

    _coerce = True

    def _serialize(self, data):
        """convert data to ZULU format"""

        # common case
        if isinstance(data, datetime.datetime):
            return data.strftime("%04Y-%02m-%02dT%02H:%02M:%S.%f")[:-3] + "Z"

        # less common
        if isinstance(data, str) and data[-1] != "Z":
            data = dateutil.parser.parse(data).astimezone(dateutil.tz.UTC)
            return data.strftime("%04Y-%2m-%2dT%H:%M:%S.%f")[:-3] + "Z"

        return data

    def _deserialize(self, data):
        if isinstance(data, str) and data[-1] == "Z":
            # optimization: fromisoformat is said to be fatest than other means
            # (strptime, etc)
            try:
                return datetime.datetime.fromisoformat(data[:-1] + "+00:00")
            except ValueError:
                # will try other strategy below
                pass

        data = super()._deserialize(data)
        # normalize UTC
        if data.tzinfo != datetime.timezone.utc:
            data = data.astimezone(datetime.timezone.utc)
        return data
