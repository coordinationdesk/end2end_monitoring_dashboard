"""Developer tool: an engine that consume messages but does nothing"""
from argparse import Namespace
from dataclasses import dataclass
from typing import ClassVar, Iterator

from maas_model import MAASMessage

from maas_engine.engine.base import Engine, EngineReport


@dataclass
class SinkEngine(Engine):
    """

    A dumb engine that does nothing, useful when consuming routing key that has not
    been yet developped so AMQP does not accumulate unrouted messages.
    """

    ENGINE_ID: ClassVar[str] = "SINK"

    def run(self, routing_key: str, payload: MAASMessage) -> Iterator[EngineReport]:
        """Only log the routing key

        Args:
            routing_key (str): routing key
            payload (MAASMEssage): message body

        Returns:
            list[EngineReport]: data reports
        """
        # dumb yield use to flag the method as report generator
        self.logger.info("Ignoring data from %s", routing_key)
        yield from []
