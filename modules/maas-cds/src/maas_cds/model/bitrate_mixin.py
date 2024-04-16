"""
Mixin to calculate bitrate
"""
import logging

LOGGER = logging.getLogger("BitrateCalculationMixin")


class BitrateCalculationMixin:
    """
    A mixin for entities having several date field which can be
    used to calculate a bitrate
    """

    def calculate_bitrate(
        self,
        key: str,
    ) -> int:
        """Calculate bitrate

        Args:
            key (str): id of the consolidated document
        Returns:
            int: bitrate in microseconds
        """

        if not (
            getattr(self, self._BITRATE_VOLUME)
            and getattr(self, self._BITRATE_DURATION)
        ):
            LOGGER.warning(
                "%s or %s is None:"
                "cannot calculate bitrate for publication key= %s",
                self._BITRATE_VOLUME,
                self._BITRATE_DURATION,
                key,
            )
            return None
        # bits / seconds
        return getattr(self, self._BITRATE_VOLUME) / (getattr(self, self._BITRATE_DURATION) / 1000000)
