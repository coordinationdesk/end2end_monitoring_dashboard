"""
Mixin to calculate timeliness
"""

import logging

from maas_cds.lib.dateutils import get_microseconds_delta

LOGGER = logging.getLogger("TimelinessCalculationMixin")


class TimelinessCalculationMixin:
    """
    A mixin for entities having several date field which can be
    used to calculate a timeliness
    """

    def calculate_timeliness(
        self,
    ) -> int:
        """Calculate timeliness

        Args:
            key (str): id of the consolidated document
        Returns:
            int: timeliness in microseconds
        """

        if not (
            getattr(self, self._TIMELINESS_START_FIELD)
            and getattr(self, self._TIMELINESS_END_FIELD)
        ):
            LOGGER.warning(
                "%s or %s is None:"
                "cannot calculate timeliness for publication key= %s",
                self._TIMELINESS_START_FIELD,
                self._TIMELINESS_END_FIELD,
                self,
            )
            return None

        return get_microseconds_delta(
            getattr(self, self._TIMELINESS_START_FIELD),
            getattr(self, self._TIMELINESS_END_FIELD),
        )
