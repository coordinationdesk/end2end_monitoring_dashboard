""" Custom CDS model definition """
from maas_cds.model import generated, DisseminationMixin

__all__ = ["DasProduct"]


class DasProduct(DisseminationMixin, generated.DasProduct):
    """

    Override to store business logic
    """

    @property
    def start_date(self):
        """Retrieve start sensing date to keep LTA/PRIP interface

        Returns:
            datetime: the start sensing date (start)
        """
        return self.start

    @start_date.setter
    def start_date(self, value):
        """Retrieve start sensing date to keep LTA/PRIP interface

        Returns:
            datetime: the start sensing date (start)
        """
        self.start = value
