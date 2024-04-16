"""Entry point for filesystem collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    loki_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.lokicollector import (
    LokiCollector,
    LokiConfiguration,
)


def loki_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), loki_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    loki_config = LokiConfiguration(
        namespace.loki_timeout,
        namespace.loki_keep_files,
    )

    collector = LokiCollector(args, loki_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("Loki",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    loki_collector_main(sys.argv[1:])
