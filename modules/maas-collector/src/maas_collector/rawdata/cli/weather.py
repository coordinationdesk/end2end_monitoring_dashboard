"""Entry point for filesystem collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    weather_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.weathercollector import (
    WeatherCollector,
    WeatherConfiguration,
)


def weather_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(parents=[common_parser(), weather_parser()])

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    weather_config = WeatherConfiguration(
        namespace.weather_timeout,
        namespace.weather_keep_files,
    )

    collector = WeatherCollector(args, weather_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("Weather",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    weather_collector_main(sys.argv[1:])
