"""Entry point for filesystem collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    odata_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.odatacollector import (
    ODataCollector,
    ODataConfiguration,
)


def odata_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), odata_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    odata_config = ODataConfiguration(
        namespace.odata_timeout,
        namespace.odata_keep_files,
    )

    collector = ODataCollector(args, odata_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("OData",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    odata_collector_main(sys.argv[1:])
