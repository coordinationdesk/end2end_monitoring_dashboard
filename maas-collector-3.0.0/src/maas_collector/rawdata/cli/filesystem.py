"""Entry point for filesystem collection"""
import argparse
import dataclasses
import sys
import typing

from maas_collector.rawdata.cli.lib.args import get_collector_args, common_parser
import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.collector.filecollector import FileCollector, CollectorArgs


@dataclasses.dataclass
class FileCollectorArgs(CollectorArgs):
    """store arguments"""

    path_list: typing.List[str] = None


def filesystem_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser()])
    parser.add_argument("PATH", help="Files or directories, space separated", nargs="+")
    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(FileCollectorArgs, namespace, path_list=namespace.PATH)

    collector = FileCollector(args)

    collector.setup()

    try:
        collector.run(args.path_list)
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    filesystem_collector_main(sys.argv[1:])
