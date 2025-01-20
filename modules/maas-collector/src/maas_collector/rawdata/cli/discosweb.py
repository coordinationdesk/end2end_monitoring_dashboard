"""Entry point for Discosweb collection"""

import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    http_common_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.discoswebcollector import (
    DiscoswebCollector,
    DiscoswebConfiguration,
)


def discosweb_collector_main(args):
    """Entry point for DiscoswebCollector"""
    parser = argparse.ArgumentParser(parents=[common_parser(), http_common_parser()])

    namespace = parser.parse_args(args)

    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    discosweb_config = DiscoswebConfiguration(
        namespace.http_common_timeout, namespace.http_common_keep_files
    )

    collector = DiscoswebCollector(args, discosweb_config)

    collector.setup()

    try:
        collector.run(("Discosweb",))
    except KeyboardInterrupt:
        print("Exited by keyboard interruption")


if __name__ == "__main__":
    discosweb_collector_main(sys.argv[1:])
