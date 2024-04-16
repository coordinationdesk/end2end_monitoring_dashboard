"""Entry point for filesystem collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    mpip_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.mpipcollector import (
    MpipCollector,
    MpipConfiguration,
)


def mpip_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), mpip_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    mpip_config = MpipConfiguration(
        namespace.mpip_timeout,
        namespace.mpip_keep_files,
    )

    collector = MpipCollector(args, mpip_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("Mpip",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    mpip_collector_main(sys.argv[1:])
