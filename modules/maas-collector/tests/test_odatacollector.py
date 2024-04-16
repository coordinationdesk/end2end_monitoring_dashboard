# """odata collector testing"""
# import datetime
# import os
# import logging
# import sys
# from requests import Session

# import pytest
# from unittest.mock import patch
# import unittest

# from maas_collector.rawdata.collector.filecollector import CollectorArgs, FileCollector
# from maas_collector.rawdata.collector.odatacollector import (
#     ODataConfiguration,
#     ODataCollector,
# )


# from conftest import (
#     mock_client,
#     mocked_requests_post,
#     mocked_requests_get,
#     mocked_requests_work_and_fail,
#     mocked_requests_post_short_token,
#     mocked_requests_post_short_token_failed_refresh,
#     mocked_requests_get_no_response,
#     mocked_requests_get_work_then_no_response,
# )

# DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# TEST_NO_AUTH_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-no-auth.json"
# )

# TEST_BASIC_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-basic.json"
# )

# TEST_OAUTH_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-oauth.json"
# )

# TEST_BAD_PRODUCT_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-bad-product.json"
# )

# TEST_BAD_AUTH_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-bad-auth.json"
# )

# TEST_PAGINATION_CONF = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-pagination.json"
# )

# TEST_CREDENTIAL_FILE = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-credentials.json"
# )

# TEST_REFRESH_TOKEN_FILE = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-oauth-pagination.json"
# )

# TEST_WRONG_INTERFACE_FILE = os.path.join(
#     os.path.dirname(__file__), "conf", "test-maas-collector-odata-wrong-interface.json"
# )


# class TestODataCollector(unittest.TestCase):
#     @patch.object(FileCollector, "setup")
#     def test_odatacollector_config(self, mock_super_setup):

#         args = CollectorArgs(rawdata_config=TEST_NO_AUTH_CONF, healthcheck_port=8123)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()
#         collector.load_config()

#         assert collector.token == None

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_basic_auth(self, mock_super_setup, mock_session_get, mock_file_collector):
#         args = CollectorArgs(rawdata_config=TEST_BASIC_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()
#         collector.ingest()

#         assert collector.token == "Basic bXlfc3VwZXJfdXNlcjpteV9zdXBlcl9wYXNzd29yZA=="

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "post", side_effect=mocked_requests_post)
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_oauth(
#         self, mock_super_setup, mock_session_get, mock_session_post, mock_file_collector
#     ):

#         args = CollectorArgs(rawdata_config=TEST_OAUTH_CONF, healthcheck_port=8123)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()
#         collector.ingest()
#         assert collector.token == "my_super_token_oauth"

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "post", side_effect=mocked_requests_post)
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_bad_auth_request(
#         self, mock_super_setup, mock_session_get, mock_session_post, mock_file_collector
#     ):
#         args = CollectorArgs(rawdata_config=TEST_BAD_AUTH_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         with self.assertRaises(ValueError) as context:
#             collector.ingest()

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_no_auth_request(
#         self, mock_super_setup, mock_session_get, mock_file_collector
#     ):
#         args = args = CollectorArgs(rawdata_config=TEST_NO_AUTH_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         collector.ingest()

#         assert collector.token == ""

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_pagination(self, mock_super_setup, mock_session_get, mock_file_collector):
#         args = CollectorArgs(rawdata_config=TEST_PAGINATION_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         collector.ingest()
#         #  One for count on for product
#         assert mock_session_get.call_count == 3

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "get", side_effect=mocked_requests_work_and_fail)
#     @patch.object(FileCollector, "setup")
#     def test_get_count_work_then_product_fail(
#         self, mock_super_setup, mock_session_get, mock_file_collector
#     ):
#         args = args = CollectorArgs(rawdata_config=TEST_PAGINATION_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         with self.assertRaises(ValueError):
#             collector.ingest()

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_bad_product_url(
#         self, mock_super_setup, mock_session_get, mock_file_collector
#     ):
#         args = args = CollectorArgs(rawdata_config=TEST_BAD_PRODUCT_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         with self.assertRaises(ValueError):
#             collector.ingest()

#     @patch.object(Session, "get", side_effect=mocked_requests_get_no_response)
#     @patch.object(FileCollector, "setup")
#     def test_except_no_response_from_api_count(
#         self, mock_super_setup, mock_session_get
#     ):
#         args = CollectorArgs(rawdata_config=TEST_NO_AUTH_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         collector.ingest()

#         assert mock_session_get.call_count == 1

#     @patch.object(Session, "get", side_effect=mocked_requests_get_work_then_no_response)
#     @patch.object(FileCollector, "setup")
#     def test_except_no_response_from_api_product(
#         self, mock_super_setup, mock_session_get
#     ):
#         args = CollectorArgs(rawdata_config=TEST_PAGINATION_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         collector.ingest()

#         assert mock_session_get.call_count == 2

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(
#         Session, "post", side_effect=mocked_requests_post_short_token_failed_refresh
#     )
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_oauth_refresh_failed(
#         self, mock_super_setup, mock_session_get, mock_session_post, mock_file_collector
#     ):

#         args = CollectorArgs(rawdata_config=TEST_REFRESH_TOKEN_FILE)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()

#         with self.assertRaises(ValueError):
#             collector.ingest()
#             assert mock_session_post.call_count == 2

#     @patch.object(FileCollector, "extract_from_file")
#     @patch.object(Session, "post", side_effect=mocked_requests_post_short_token)
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_oauth_refresh(
#         self, mock_super_setup, mock_session_get, mock_session_post, mock_file_collector
#     ):

#         args = CollectorArgs(rawdata_config=TEST_REFRESH_TOKEN_FILE)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         collector.load_config()
#         collector.ingest()

#         assert collector.token == "my_super_token_oauth"
#         assert collector.refresh_token == "my_super_refresh_token_oauth"

#         assert mock_session_post.call_count >= 2

#     @patch.object(ODataCollector, "ingest_odata")
#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_should_stop_ingest(
#         self, mock_super_setup, mock_session_get, mock_ingest_odata
#     ):
#         args = CollectorArgs(rawdata_config=TEST_PAGINATION_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)
#         collector.setup()
#         collector.load_config()

#         collector.should_stop_loop = True
#         collector.ingest()

#         assert mock_ingest_odata.call_count == 0

#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_should_stop_ingest_odata(self, mock_super_setup, mock_session_get):
#         args = CollectorArgs(rawdata_config=TEST_PAGINATION_CONF)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)
#         collector.setup()
#         collector.load_config()

#         collector.should_stop_loop = True
#         collector.ingest_odata(collector.configs[0])

#         # first call for count is made
#         assert mock_session_get.call_count == 1

#     @patch.object(Session, "get", side_effect=mocked_requests_get)
#     @patch.object(FileCollector, "setup")
#     def test_except_wrong_interface(self, mock_super_setup, mock_session_get):
#         args = CollectorArgs(rawdata_config=TEST_WRONG_INTERFACE_FILE)

#         logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#         odata_config = ODataConfiguration(
#             timeout=60, credential_file=TEST_CREDENTIAL_FILE
#         )
#         collector = ODataCollector(args, odata_config)

#         collector.setup()

#         with self.assertRaises(KeyError):
#             collector.load_config()
