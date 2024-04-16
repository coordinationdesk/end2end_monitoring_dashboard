"""Monitoring collector endpoint"""
import sys

import maas_collector.rawdata.cli.lib.log as maas_log

from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    EnvDefault,
)

from maas_collector.rawdata.collector.filecollector import CollectorArgs

from maas_collector.rawdata.collector.monitorcollector import (
    InterfaceMonitor,
    InterfaceMonitorConfiguration,
)


def interface_monitor_main(args):
    """entry point"""
    parser = common_parser()

    parser.add_argument(
        "--monitoring-interface-name",
        dest="monitoring_interface_name",
        help="Monitoring interface name (default: %(default)s)",
        action=EnvDefault,
        envvar="MONITORING_INTERFACE_NAME",
        required=False,
        type=str,
    )

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    monitor_config = InterfaceMonitorConfiguration(
        interface_name=namespace.monitoring_interface_name,
    )

    collector = InterfaceMonitor(args, monitor_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    interface_monitor_main(sys.argv[1:])
