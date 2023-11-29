"""Entry point for filesystem collection"""
import sys

from maas_collector.rawdata.cli.lib.args import (
    get_collector_args,
    common_parser,
)
import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.ftpcollector import (
    FTPCollector,
    FTPConfiguration,
)


def ftp_collector_main(args):
    """entry point"""
    parser = common_parser()

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    config = FTPConfiguration(
        namespace.credential_file,
    )

    collector = FTPCollector(args, config)

    collector.setup()

    try:
        collector.run(("",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    ftp_collector_main(sys.argv[1:])
