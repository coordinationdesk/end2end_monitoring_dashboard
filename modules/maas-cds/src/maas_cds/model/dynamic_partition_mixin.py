"""
This file contain all mixin to be used for dynamic partitionning ES indexes
"""
import logging
import re

from maas_model import datestr_to_utc_datetime

__all__ = ["DynamicPartitionMixin"]

LOGGER = logging.getLogger("DynamicPartitionMixin")


class DynamicPartitionMixin:
    """
    Mixin to be used on a dynamic partitionned index that contain products or publications
    """

    # Should be define in class that use the mixin
    _PARTITION_FIELDS = []

    PRODUCT_LEVEL_THAT_MAKE_SENSE = ["L0_", "L1_", "L2_", "A"]

    def get_non_sensing_partition_field_value(self):
        """select the date of publication to use as partition field

        Returns:
            date: publication date
        """
        for partition_field in self._PARTITION_FIELDS:
            for field in dir(self):
                if re.match(partition_field, field):
                    date = getattr(self, field)
                    if date:
                        if isinstance(date, str):
                            date = datestr_to_utc_datetime(date)
                        return date

        raise ValueError(
            "Unable to determine partition field value for the document : ",
            self.to_dict(),
        )

    @classmethod
    def product_level_use_sensing_partitionned(cls, product_level):
        return product_level in DynamicPartitionMixin.PRODUCT_LEVEL_THAT_MAKE_SENSE

    def shall_use_non_sensing_partition_field(self) -> bool:
        """
        Tell if the product/publication shall use another attribute than sensing for
        partitionning

        Returns:
            bool: True if sensing is not used for partitioning
        """
        return not self.product_level_use_sensing_partitionned(self.product_level)

    @property
    def partition_field_value(self):
        """return dynamically the date of sensing for sensing

        products or the date of publication for auxiliary data

        Returns:
            date: return the date to use as partition field
        """
        if self.shall_use_non_sensing_partition_field():
            return self.get_non_sensing_partition_field_value()

        return super().partition_field_value

    @property
    def has_partition_field_value(self):
        """Override tell if partition field has a value
            This can be dynamic regarding the nominal usage of the _PARTITION_FIELD
        Returns:
            bool: flag
        """

        if self.partition_field_value is not None:
            return True

        return super().has_partition_field_value
