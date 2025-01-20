""" This file test monitoring configuration """

import os
import logging
import sys
from unittest.mock import patch

from maas_collector.rawdata.collector.monitorcollector import (
    InterfaceMonitorConfiguration,
    InterfaceMonitor,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs

TEST_CONF = os.path.join(
    os.path.dirname(__file__), "conf", "maas-collector-interface-monitoring.json"
)

CREDENTIAL_FILE = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-collector-credentials.json"
)

CONF_WITH_PROBE = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-collector-odata-basic.json"
)

CONF_WITHOUT_PROBE = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-collector-odata-no-auth.json"
)

CONFS = os.path.join(os.path.dirname(__file__), "conf")


@patch("maas_collector.rawdata.collector.monitorcollector.find_configurations")
@patch(
    "opensearchpy.connection.connections.Connections.create_connection",
    return_value=True,
)
@patch("maas_collector.rawdata.messenger.Messenger.setup", return_value=True)
def test_monitoring_disable(amqp_mock, es_mock, find_conf_mock):
    """this test load configuration for 2 interface monitoring with :
        basic_test interface is probed
        no_auth interface is not probed

    Args:
        amqp_mock (_type_): rabbitmq mock
        es_mock (_type_): database mock
        find_conf_mock (_type_): find_configuration mock
    """

    find_conf_mock.return_value = [CONF_WITH_PROBE, CONF_WITHOUT_PROBE]

    args = CollectorArgs(
        rawdata_config=TEST_CONF,
        credential_file=CREDENTIAL_FILE,
    )
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    monitoring = InterfaceMonitor(
        args,
        InterfaceMonitorConfiguration(**{"interface_name": "OMCS_Monitoring"}),
    )

    monitoring.setup()

    assert len(monitoring.meta_dict) == 1
    assert list(monitoring.meta_dict.values())[0].name == "basic_test"

    monitoring.exit_gracefully(9, "")
