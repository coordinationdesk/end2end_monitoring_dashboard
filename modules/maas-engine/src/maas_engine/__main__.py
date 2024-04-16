"""entry point"""
import sys

from maas_engine.consumer.engine_consumer import MaasEngineConsumer


def main(args):
    """entry point"""
    MaasEngineConsumer.main(args)


main(sys.argv[1:])
