""" Custom CDS dataflow type spec definition"""

from opensearchpy import Keyword
from maas_cds.model import generated

__all__ = ["CdsDataflow"]


class CdsDataflow(generated.CdsDataflow):
    """
    Sentinel products type spec
    """

    lta = Keyword(multi=True)

    groups = Keyword(multi=True)

    published_by = Keyword(multi=True)

    consumed_by = Keyword(multi=True)
