""" Custom CDS model definition for product"""

import logging
import typing

from opensearchpy import Keyword
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.dynamic_partition_mixin import DynamicPartitionMixin
from maas_cds.model.product_datatake_mixin import ProductDatatakeMixin
from maas_cds.model import generated
import maas_cds.lib.parsing_name.utils as utils


from maas_cds.lib.dateutils import get_microseconds_delta

__all__ = ["CdsProduct"]

LOGGER = logging.getLogger("CdsProduct")


class CdsProduct(
    DynamicPartitionMixin, AnomalyMixin, ProductDatatakeMixin, generated.CdsProduct
):
    """CdsProduct custom"""

    cams_tickets = Keyword(multi=True)

    _PARTITION_FIELDS = [
        "PRIP_.*_publication_date",
        "prip_publication_date",
        "AUXIP_.*_publication_date",
        "auxip_publication_date",
        "DD_.*_publication_date",
        "ddip_publication_date",
        "dddas_publication_date",
        "ddcreodias_publication_date",
        "MPCIP_.*_publication_date",
        "LTA_.*_publication_date",
    ]

    def datatake_id_is_missing(self) -> bool:
        """Returns true if datatake id is missing or None

        Returns:
            boolean: datatake is missing
        """
        return (
            self.datatake_id is None
            or self.datatake_id == utils.DATATAKE_ID_MISSING_VALUE
        )

    def get_datatake_id(self) -> str | None:
        """Return the associate datatake id of the product

        Returns:
            str: associate cds-datatake id
        """

        return (
            f"{self.satellite_unit}-{self.datatake_id}"
            if not self.datatake_id_is_missing()
            else None
        )

    def get_compute_key(self):
        """Return the compute key of the product

        The key is unique for a calcul

        If the product is not associate with calcul the method should return None

        """

        LOGGER.warning(
            "get_compute_key - Must be surcharged in sub class specific for each mission : %s",
            self.name,
        )
        return None

    def data_for_datatake(self):
        """When a datatake is not already create from the mp
        this method allow to create the associate datatake from the product

        Returns:
            dict: data for create the datatake. Default None
        """
        return None

    def calculate_dd_timeliness(self, dd_service_name, dd_attrs):
        """Calculate from PRIP to DD timeliness"""

        dd_attr_config = dd_attrs.get(dd_service_name)

        if dd_attr_config is None:
            LOGGER.error(
                "Unknown dd service name : %s. Cannot calculate dd timeliness for product : %s.",
                dd_service_name,
                self.name,
            )
            return

        dd_publication_date = getattr(self, dd_attr_config["publication_date"])

        if self.prip_publication_date and dd_publication_date:
            setattr(
                self,
                dd_attr_config["from_prip_timeliness"],
                get_microseconds_delta(dd_publication_date, self.prip_publication_date),
            )

    def mark_as_deleted(self, issue: "DeletionIssue", service_ids: typing.List[str]):
        """Populate attributes to reflect deletion from interfaces.

        Args:
            issue (DeletionIssue): issue
            interface_name_dict (dict, optional): interface name dict. Defaults to None.
        """
        for service_id in service_ids:
            prefix = f"{issue.interface_type}_{service_id}"

            setattr(self, f"{prefix}_is_deleted", True)

            setattr(self, f"{prefix}_deletion_issue", issue.key)

            setattr(
                self,
                f"{prefix}_deletion_date",
                issue.deletion_date,
            )

            setattr(
                self,
                f"{prefix}_deletion_cause",
                issue.deletion_cause,
            )

        # Count deleted per service type
        nb_deleted_attrname = f"nb_{issue.interface_type.lower()}_deleted"

        nb_deleted_value = sum(
            1 if getattr(self, field) else 0
            for field in dir(self)
            if field.startswith(f"{issue.interface_type}_")
            and field.endswith("_is_deleted")
        )

        setattr(self, nb_deleted_attrname, nb_deleted_value)
