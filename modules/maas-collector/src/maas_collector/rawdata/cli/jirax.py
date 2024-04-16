"""Entry point for filesystem collection"""

import sys

import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
)

from maas_collector.rawdata.collector.filecollector import CollectorArgs

from maas_collector.rawdata.collector.jiraxcollector import JIRAExtendedCollector


def jirax_collector_main(args):
    """entry point"""
    parser = common_parser()
    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    collector = JIRAExtendedCollector(get_collector_args(CollectorArgs, namespace))

    collector.setup()

    try:
        # no path provided, passing endpoint for logging readability
        collector.run(("Jira",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    jirax_collector_main(sys.argv[1:])
