# """Tests for LTA Werum consolidation into products and publications"""
# import datetime
# from unittest.mock import patch
# from maas_cds.engines.reports.lta_deletion import (
#     LTADeletionConsolidatorEngine,
#     LTADeletionProductConsolidatorEngine,
# )


# import maas_model
# import pytest

# from maas_cds.engines.reports.product import ProductConsolidatorEngine
# from maas_cds.engines.reports.publication import PublicationConsolidatorEngine
# from maas_cds.model import (
#     CdsDatatake,
#     LtaDeletionProduct,
#     CdsLtaDeletionProduct,
#     LtaProduct,
#     CdsProduct,
#     LtaDeletionIssue,
#     CdsPublication,
# )


# @pytest.fixture
# def lta_deletion_issue_1():
#     "LtaDeletionIssue test object"
#     data_dict = {
#         "key": "OMCS-1664",
#         "deletion_date": "2022-01-12T07:12:53.994Z",
#         "deletion_cause": "The dog ate the products",
#         "deletion_ltas": ["Exprivia"],
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#         "reportName": "OMCS-1664",
#     }
#     raw_document = LtaDeletionIssue(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def lta_deletion_issue_no_lta_given():
#     "LtaDeletionIssue test object"
#     data_dict = {
#         "key": "OMCS-1664",
#         "deletion_date": "2022-01-12T07:12:53.994Z",
#         "deletion_cause": "The dog ate the products",
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#         "reportName": "OMCS-1664",
#     }
#     raw_document = LtaDeletionIssue(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def lta_deletion_products_1():
#     "LtaDeletionProduct test object"
#     data_dict = {
#         # "jira_issue": "OMCS-1664",
#         "products_list": [
#             "S2B_OPER_MSI_L0__DS_2BPS_20220830T122617_S20220830T003155_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003206_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003224_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003155_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003202_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003155_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003227_D10_N04.00.tar",
#         ],
#         "reportName": "OMCS-1664_REPORTNAME",
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#     }
#     raw_document = LtaDeletionProduct(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def cds_lta_deletion_products_1():
#     "CdsLtaDeletionProduct test object"
#     data_dict = {
#         # "jira_issue": "OMCS-1664",
#         "products_list": [
#             "S2B_OPER_MSI_L0__DS_2BPS_20220830T122617_S20220830T003155_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003206_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003224_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003155_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003202_D12_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003155_D11_N04.00.tar",
#             "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003227_D10_N04.00.tar",
#         ],
#         "reportName": "OMCS-1664_REPORTNAME",
#         "jira_issue": "OMCS-1664",
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#     }
#     raw_document = CdsLtaDeletionProduct(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def lta_product_1():
#     "LtaProduct test object"

#     data_dict = {
#         "reportName": "LTA_Werum_20220111T150336_20220112T103044_1000_P103.json",
#         "product_id": "9484cbcc-c1d0-48d8-0de6-0104621c7d82",
#         "product_name": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#         "content_length": 2519,
#         "publication_date": "2022-01-12T07:11:53.994Z",
#         "start_date": "2020-05-11T22:26:03.000Z",
#         "end_date": "2020-05-12T01:47:27.000Z",
#         "origin_date": "2020-05-11T00:00:00.000Z",
#         "modification_date": "2022-01-12T07:11:53.994Z",
#         "interface_name": "LTA_Werum",
#         "production_service_type": "LTA",
#         "production_service_name": "Werum",
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#     }
#     raw_document = LtaProduct(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def cds_product_1():
#     "CdsProduct test object"

#     data_dict = {
#         "key": "68f5fc840ea626bafb05c34ff5a364f7",
#         "mission": "S2",
#         "name": "S2A_OPER_MSI_L0__GR_ATOS_20220622T224339_S20220622T175008_D03_N04.00.tar",
#         "product_level": "L0_",
#         "product_type": "MSI_L0__GR",
#         "satellite_unit": "S2A",
#         "site_center": "ATOS",
#         "sensing_start_date": "2022-06-22T17:50:08.468Z",
#         "sensing_end_date": "2022-06-22T17:50:08.468Z",
#         "sensing_duration": 0,
#         "timeliness": "_",
#         "detector_id": "03",
#         "expected_lta_number": 4,
#         "LTA_Exprivia_S2_is_published": True,
#         "LTA_Exprivia_S2_publication_date": "2022-06-22T23:35:44.526000+00:00",
#         "nb_lta_served": 1,
#         "updateTime": "2022-10-26T07:27:30.271Z",
#     }
#     raw_document = CdsProduct(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# @pytest.fixture
# def cds_publication_1():
#     "CdsPublication test object"

#     data_dict = {
#         "key": "e441aed124660ff7f5fc1ae8b3f4de60",
#         "mission": "S2",
#         "name": "S2B_OPER_MSI_L0__GR_2BPS_20220622T222302_S20220622T220011_D02_N04.00.tar",
#         "product_level": "L0_",
#         "product_type": "MSI_L0__GR",
#         "satellite_unit": "S2B",
#         "site_center": "2BPS",
#         "sensing_start_date": "2022-06-22T22:00:11.259Z",
#         "sensing_end_date": "2022-06-22T22:00:11.259Z",
#         "sensing_duration": 0,
#         "timeliness": "_",
#         "content_length": 18390528,
#         "service_id": "Exprivia",
#         "service_type": "LTA",
#         "product_uuid": "0951a3a6-f284-11ec-8e94-bc97e19feb4c",
#         "modification_date": "2022-06-22T23:35:44.723Z",
#         "origin_date": "2022-06-22T23:17:54.122Z",
#         "publication_date": "2022-06-22T23:35:44.723Z",
#         "transfer_timeliness": 1070601000,
#         "from_sensing_timeliness": 5733464000,
#         "updateTime": "2022-10-26T07:27:19.864Z",
#     }
#     raw_document = CdsPublication(**data_dict)
#     raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
#     raw_document.full_clean()
#     return raw_document


# def test_LTADeletionProductConsolidatorEngine(
#     lta_deletion_products_1,
# ):
#     "product consolidation test"

#     engine = LTADeletionProductConsolidatorEngine()

#     document = CdsLtaDeletionProduct()

#     product = engine.consolidate_from_LtaDeletionProduct(
#         # raw_document: LtaDeletionProduct, document: CdsLtaDeletionProduct
#         lta_deletion_products_1,
#         document,
#     )

#     assert product.to_dict() == {
#         "ingestionTime": "2022-02-12T14:25:46.396Z",
#         "jira_issue": "OMCS-1664",
#         "reportName": "OMCS-1664_REPORTNAME",
#     }


# # pylint: disable=W2901
# def test_get_published_lta_name(
#     cds_product_1,
# ):
#     "get_published_lta_name test"

#     result = CdsLtaDeletionProduct.get_published_lta_name(cds_product_1, "exprivia")
#     assert result == "Exprivia_S2"


# # pylint: disable=W2901
# @patch("maas_cds.model.CdsLtaDeletionProduct.get_products_names")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_publications")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_products")
# def test_lta_product_consolidation_from_issue(
#     mock_get_products,
#     mock_get_publications,
#     mock_get_products_names,
#     cds_product_1,
#     lta_deletion_issue_1,
#     cds_publication_1,
# ):
#     "lta-deletion consolidation test"

#     mock_get_products_names.return_value = [
#         "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#     ]
#     mock_get_publications.return_value = [cds_publication_1]
#     mock_get_products.return_value = [cds_product_1]

#     engine = LTADeletionConsolidatorEngine()
#     engine.payload = maas_model.MAASMessage(document_class="LtaDeletionIssue")
#     engine.input_documents = [lta_deletion_issue_1]

#     results = list(engine.action_iterator())

#     for r in results:
#         del r["_source"]["updateTime"]
#         try:
#             r["_source"]["LTA_Exprivia_S2_deletion_date"] = r["_source"][
#                 "LTA_Exprivia_S2_deletion_date"
#             ].isoformat(sep="T", timespec="auto")
#         except KeyError:
#             pass

#     assert results == [
#         {
#             "_id": "ce44721a4ab1ccaff42b945850019ff7",
#             "_index": "cds-product-2022-06",
#             "_source": {
#                 "key": "68f5fc840ea626bafb05c34ff5a364f7",
#                 "mission": "S2",
#                 "name": "S2A_OPER_MSI_L0__GR_ATOS_20220622T224339_S20220622T175008_D03_N04.00.tar",
#                 "product_level": "L0_",
#                 "product_type": "MSI_L0__GR",
#                 "satellite_unit": "S2A",
#                 "site_center": "ATOS",
#                 "sensing_start_date": "2022-06-22T17:50:08.468Z",
#                 "sensing_end_date": "2022-06-22T17:50:08.468Z",
#                 "sensing_duration": 0,
#                 "timeliness": "_",
#                 "detector_id": "03",
#                 "expected_lta_number": 4,
#                 "LTA_Exprivia_S2_is_published": True,
#                 "LTA_Exprivia_S2_is_deleted": True,
#                 "LTA_Exprivia_S2_publication_date": "2022-06-22T23:35:44.526000+00:00",
#                 "LTA_Exprivia_S2_deletion_cause": "The dog ate the products",
#                 "LTA_Exprivia_S2_deletion_date": "2022-01-12T07:12:53.994000+00:00",
#                 "LTA_Exprivia_S2_deletion_issue": "OMCS-1664",
#                 "nb_lta_served": 1,
#                 "nb_lta_deleted": 1,
#             },
#             "_op_type": "create",
#         },
#         {
#             "_id": "ce44721a4ab1ccaff42b945850019ff7",
#             "_index": "cds-publication-2022-06",
#             "_source": {
#                 "key": "e441aed124660ff7f5fc1ae8b3f4de60",
#                 "mission": "S2",
#                 "name": "S2B_OPER_MSI_L0__GR_2BPS_20220622T222302_S20220622T220011_D02_N04.00.tar",
#                 "product_level": "L0_",
#                 "product_type": "MSI_L0__GR",
#                 "satellite_unit": "S2B",
#                 "site_center": "2BPS",
#                 "sensing_start_date": "2022-06-22T22:00:11.259Z",
#                 "sensing_end_date": "2022-06-22T22:00:11.259Z",
#                 "sensing_duration": 0,
#                 "timeliness": "_",
#                 "content_length": 18390528,
#                 "service_id": "Exprivia",
#                 "service_type": "LTA",
#                 "product_uuid": "0951a3a6-f284-11ec-8e94-bc97e19feb4c",
#                 "modification_date": "2022-06-22T23:35:44.723Z",
#                 "origin_date": "2022-06-22T23:17:54.122Z",
#                 "publication_date": "2022-06-22T23:35:44.723Z",
#                 "transfer_timeliness": 1070601000,
#                 "from_sensing_timeliness": 5733464000,
#                 "deletion_date": "2022-01-12T07:12:53.994Z",
#                 "deletion_cause": "The dog ate the products",
#                 "deletion_issue": "OMCS-1664",
#             },
#             "_op_type": "create",
#         },
#     ]


# # pylint: disable=W2901
# @patch("maas_cds.model.CdsLtaDeletionProduct.get_products_names")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_related_issues")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_publications")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_products")
# def test_lta_product_consolidation_from_product(
#     mock_get_products,
#     mock_get_publications,
#     mock_get_related_issues,
#     mock_get_products_names,
#     cds_product_1,
#     lta_deletion_issue_1,
#     cds_publication_1,
#     cds_lta_deletion_products_1,
# ):
#     "lta-deletion consolidation test"

#     mock_get_products_names.return_value = [
#         "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#     ]
#     mock_get_publications.return_value = [cds_publication_1]
#     mock_get_products.return_value = [cds_product_1]
#     mock_get_related_issues.return_value = [lta_deletion_issue_1]

#     engine = LTADeletionConsolidatorEngine()
#     engine.payload = maas_model.MAASMessage(document_class="CdsLtaDeletionProduct")
#     engine.input_documents = [cds_lta_deletion_products_1]

#     results = list(engine.action_iterator())

#     for r in results:
#         del r["_source"]["updateTime"]

#         try:
#             r["_source"]["LTA_Exprivia_S2_deletion_date"] = r["_source"][
#                 "LTA_Exprivia_S2_deletion_date"
#             ].isoformat(sep="T", timespec="auto")
#         except KeyError:
#             pass

#     assert results == [
#         {
#             "_id": "ce44721a4ab1ccaff42b945850019ff7",
#             "_index": "cds-product-2022-06",
#             "_source": {
#                 "key": "68f5fc840ea626bafb05c34ff5a364f7",
#                 "mission": "S2",
#                 "name": "S2A_OPER_MSI_L0__GR_ATOS_20220622T224339_S20220622T175008_D03_N04.00.tar",
#                 "product_level": "L0_",
#                 "product_type": "MSI_L0__GR",
#                 "satellite_unit": "S2A",
#                 "site_center": "ATOS",
#                 "sensing_start_date": "2022-06-22T17:50:08.468Z",
#                 "sensing_end_date": "2022-06-22T17:50:08.468Z",
#                 "sensing_duration": 0,
#                 "timeliness": "_",
#                 "detector_id": "03",
#                 "expected_lta_number": 4,
#                 "LTA_Exprivia_S2_is_published": True,
#                 "LTA_Exprivia_S2_is_deleted": True,
#                 "LTA_Exprivia_S2_publication_date": "2022-06-22T23:35:44.526000+00:00",
#                 "LTA_Exprivia_S2_deletion_cause": "The dog ate the products",
#                 "LTA_Exprivia_S2_deletion_date": "2022-01-12T07:12:53.994000+00:00",
#                 "LTA_Exprivia_S2_deletion_issue": "OMCS-1664",
#                 "nb_lta_served": 1,
#                 "nb_lta_deleted": 1,
#             },
#             "_op_type": "create",
#         },
#         {
#             "_id": "ce44721a4ab1ccaff42b945850019ff7",
#             "_index": "cds-publication-2022-06",
#             "_source": {
#                 "key": "e441aed124660ff7f5fc1ae8b3f4de60",
#                 "mission": "S2",
#                 "name": "S2B_OPER_MSI_L0__GR_2BPS_20220622T222302_S20220622T220011_D02_N04.00.tar",
#                 "product_level": "L0_",
#                 "product_type": "MSI_L0__GR",
#                 "satellite_unit": "S2B",
#                 "site_center": "2BPS",
#                 "sensing_start_date": "2022-06-22T22:00:11.259Z",
#                 "sensing_end_date": "2022-06-22T22:00:11.259Z",
#                 "sensing_duration": 0,
#                 "timeliness": "_",
#                 "content_length": 18390528,
#                 "service_id": "Exprivia",
#                 "service_type": "LTA",
#                 "product_uuid": "0951a3a6-f284-11ec-8e94-bc97e19feb4c",
#                 "modification_date": "2022-06-22T23:35:44.723Z",
#                 "origin_date": "2022-06-22T23:17:54.122Z",
#                 "publication_date": "2022-06-22T23:35:44.723Z",
#                 "transfer_timeliness": 1070601000,
#                 "from_sensing_timeliness": 5733464000,
#                 "deletion_date": "2022-01-12T07:12:53.994Z",
#                 "deletion_cause": "The dog ate the products",
#                 "deletion_issue": "OMCS-1664",
#             },
#             "_op_type": "create",
#         },
#     ]


# # pylint: disable=W2901
# @patch("maas_cds.model.CdsLtaDeletionProduct.get_products_names")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_related_issues")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_publications")
# @patch("maas_cds.engines.reports.LTADeletionConsolidatorEngine.get_products")
# def test_lta_product_consolidation_from_product_no_issue(
#     mock_get_products,
#     mock_get_publications,
#     mock_get_related_issues,
#     mock_get_products_names,
#     cds_product_1,
#     lta_deletion_issue_1,
#     cds_publication_1,
#     cds_lta_deletion_products_1,
# ):
#     "lta-deletion consolidation test"

#     mock_get_products_names.return_value = [
#         "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
#     ]
#     mock_get_publications.return_value = [cds_publication_1]
#     mock_get_products.return_value = [cds_product_1]
#     mock_get_related_issues.return_value = []

#     engine = LTADeletionConsolidatorEngine()
#     engine.payload = maas_model.MAASMessage(document_class="CdsLtaDeletionProduct")
#     engine.input_documents = [cds_lta_deletion_products_1]

#     results = list(engine.action_iterator())

#     for r in results:
#         del r["_source"]["updateTime"]

#     assert results == []


# def test_lta_deletion_product_missing_lta(lta_deletion_issue_no_lta_given):
#     assert len(lta_deletion_issue_no_lta_given.lta_to_remove_list) == 0
