"""Entry point for filesystem collection"""
import argparse
import sys

from maas_collector.rawdata.cli.lib.args import (
    get_collector_args,
    common_parser,
    sftp_parser,
)
import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.sftpcollector import (
    SFTPCollector,
    SFTPConfiguration,
)


def sftp_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), sftp_parser()])

    parser.add_argument(
        "REMOTEPATH", help="Remote files or directories, space separated", nargs="+"
    )

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    config = SFTPConfiguration(
        namespace.sftp_hostname,
        namespace.sftp_port,
        namespace.sftp_username,
        namespace.sftp_password,
        namespace.sftp_process_prefix,
        namespace.sftp_inbox_root,
        namespace.sftp_ingested_dir,
        namespace.sftp_rejected_dir,
        namespace.sftp_force_suffix,
        namespace.sftp_age_limit,
    )

    collector = SFTPCollector(args, config)

    collector.setup()

    try:
        collector.run(namespace.REMOTEPATH)
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    sftp_collector_main(sys.argv[1:])
