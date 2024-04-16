"""Entry point for read only sftp collection"""
import sys

from maas_collector.rawdata.cli.lib.args import (
    get_collector_args,
    common_parser,
)
import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.rosftpcollector import ReadOnlySFTPCollector


def readonly_sftp_collector_main(args):
    """entry point"""
    parser = common_parser()

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    collector = ReadOnlySFTPCollector(get_collector_args(CollectorArgs, namespace))

    collector.setup()

    try:
        collector.run(("",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    readonly_sftp_collector_main(sys.argv[1:])
