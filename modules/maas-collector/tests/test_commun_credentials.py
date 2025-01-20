""" This file test monitoring configuration """

import os
import logging
import sys
from unittest.mock import patch

from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollector,
    FileCollectorConfiguration,
)
from maas_collector.rawdata.collector.odatacollector import (
    ODataCollector,
    ODataConfiguration,
)
from maas_collector.rawdata.extractor.base import BaseExtractor

TEST_CONF = os.path.join(
    os.path.dirname(__file__),
    "conf",
    "test-maas-collector-odata-oauth-common-cred.json",
)

CREDENTIAL_FILE = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-collector-credentials.json"
)


@patch(
    "opensearchpy.connection.connections.Connections.create_connection",
    return_value=True,
)
@patch("maas_collector.rawdata.messenger.Messenger.setup", return_value=True)
def test_load_commun_credentials(amqp_mock, es_mock):

    args = CollectorArgs(
        rawdata_config=TEST_CONF,
        credential_file=CREDENTIAL_FILE,
    )
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    collector = ODataCollector(args, ODataConfiguration())

    collector.setup()

    assert collector.configs[0].token_field_header == "my_super_header"
    assert collector.configs[0].auth_method == "Basic"
    assert collector.configs[0].odata_product_url == "http://my_super_product_url"
    assert collector.configs[0].client_username == "my_super_user"
    assert collector.configs[0].client_password == "my_super_password"

    assert collector.configs[1].token_field_header == "my_super_header"
    assert collector.configs[1].auth_method == "Basic"
    assert (
        collector.configs[1].odata_product_url
        == "http://my_super_product_url/custom_for_beta"
    )
    assert collector.configs[1].client_username == "my_super_user"
    assert collector.configs[1].client_password == "my_super_password"
