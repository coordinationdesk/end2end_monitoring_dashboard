"""Entry point for filesystem collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    webdav_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.webdavcollector import (
    WebDAVCollector,
    WebDAVConfiguration,
)


def webdav_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), webdav_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    webdav_config = WebDAVConfiguration(
        namespace.webdav_timeout,
    )

    collector = WebDAVCollector(args, webdav_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    webdav_collector_main(sys.argv[1:])
