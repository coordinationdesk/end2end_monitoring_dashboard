""" Custom CDS model definition """
from maas_cds.model import generated, DisseminationMixin

__all__ = ["DdProduct"]


class DdProduct(DisseminationMixin, generated.DdProduct):
    """

    Override to store business logic
    """

    @property
    def publication_date(self):
        """Retrieve publication date depending on class

        Returns:
            datetime: the publication date (creation_date)
        """
        return self.creation_date

    @publication_date.setter
    def publication_date(self, value):
        """Retrieve publication date depending on class

        Returns:
            datetime: the publication date (creation_date)
        """
        self.creation_date = value

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
