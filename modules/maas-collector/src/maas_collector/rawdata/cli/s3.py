"""Entry point for filesystem collection"""

import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    s3_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.s3collector import (
    S3Collector,
    S3Configuration,
)


def s3_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), s3_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    s3_config = S3Configuration(
        namespace.s3_timeout,
        namespace.s3_keep_files,
    )

    collector = S3Collector(args, s3_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("S3",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    s3_collector_main(sys.argv[1:])
