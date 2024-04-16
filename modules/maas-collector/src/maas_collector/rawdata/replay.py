"""

Replay related stuff
"""

import dataclasses
import datetime

from maas_model import datestr_to_utc_datetime


@dataclasses.dataclass
class ReplayArgs:
    """store backup parameters"""

    interface_name: str = ""

    start_date_arg: str = None

    end_date_arg: str = None

    suffix: str = None

    retry: int = 1024

    @property
    def start_date(self) -> datetime.datetime:
        """return start_date_arg as datetime object

        Returns:
            datetime.datetime: start date
        """
        return datestr_to_utc_datetime(self.start_date_arg)

    @property
    def end_date(self) -> datetime.datetime:
        """return end_date_arg as datetime object

        Returns:
            datetime.datetime: end date
        """
        return datestr_to_utc_datetime(self.end_date_arg)
