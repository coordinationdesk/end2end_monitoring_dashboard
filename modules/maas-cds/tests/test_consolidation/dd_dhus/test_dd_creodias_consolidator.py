from unittest.mock import patch

import pytest

from maas_engine.engine.base import EngineSession

import maas_cds.model as model


from maas_cds.engines.reports.dd_product import DDProductConsolidatorEngine
from maas_cds.engines.reports import PublicationConsolidatorEngine

from maas_cds.model.datatake import CdsDatatake


def test_dd_das_publication_consolidation(s2_creodias_product_1):
    engine = PublicationConsolidatorEngine()
    engine.session = EngineSession()

    publication = engine.consolidate_from_CreodiasProduct(
        s2_creodias_product_1, model.CdsPublication()
    )

    engine.consolidated_documents = [publication]

    publication.full_clean()

    assert publication.to_dict() == {
        "content_length": 485359842,
        "from_sensing_timeliness": 15409338646000,
        "key": "c43d34bf843b455cdb83505fb49714f2",
        "mission": "S2",
        "name": "S2A_MSIL2A_20220710T170936_N0204_R112_T23XMG_20220710T170937.SAFE",
        "product_uuid": "9874d06d-f2de-5f46-bb21-b9dac8c95d6c",
        "product_type": "MSI_L2A___",
        "product_level": "L2_",
        "publication_date": "2023-01-05T01:31:54.673Z",
        "satellite_unit": "S2A",
        "sensing_start_date": "2022-07-10T17:09:36.027Z",
        "sensing_end_date": "2022-07-10T17:09:36.027Z",
        "sensing_duration": 0,
        "product_discriminator_date": "2022-07-10T17:09:37.000Z",  # temp solution decalage horaire (+2h)
        "service_type": "DD",
        "timeliness": "_",
        "datatake_id": "______",
        "tile_number": "23XMG",
        "service_id": "CREODIAS",
    }


# @patch("maas_cds.model.CdsDatatake.get_by_id", return_value=None)
# def test_action(mock_get_by_id, s1_ddas_product_1):
#     engine = DDProductConsolidatorEngine()

#     product = engine.consolidate_from_DasProduct(s1_ddas_product_1, model.CdsProduct())

#     assert engine.get_report_action("created", product) == "new.cds-product-s1"


# @patch("maas_cds.lib.queryutils.find_datatake_from_sensing.find_datatake_from_sensing")
# @patch("maas_cds.model.CdsPublication.get_by_id", return_value=None)
# def test_ddas_product_consolidation(
#     mock_get_by_id, mock_find_datatake_from_sensing, s2_raw_product_l1c_container_das
# ):
#     engine = PublicationConsolidatorEngine()
#     # TODO
#     product = engine.consolidate_from_DasProduct(
#         s2_raw_product_l1c_container_das, model.CdsPublication()
#     )

#     assert product.product_level == "L1_"
