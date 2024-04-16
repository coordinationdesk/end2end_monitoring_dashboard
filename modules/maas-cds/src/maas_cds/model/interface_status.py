"""Custom CdsInterfaceStatus DAO"""
from maas_cds.model import generated


__all__ = ["CdsInterfaceStatus"]


class CdsInterfaceStatus(generated.CdsInterfaceStatus):
    """

    Custom CdsInterfaceStatus model to add business logic to calculate duration
    """

    def calculate_duration(self):
        """Calculate and set status duration"""
        self.status_duration = (
            self.status_time_stop - self.status_time_start
        ).total_seconds()
