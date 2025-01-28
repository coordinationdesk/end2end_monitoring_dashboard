"""AMQP stuff to ventilate MAASMessage"""

import json
import logging

from maas_engine.engine.base import EngineReport
from maas_model import MAASMessage
from kombu import Exchange, Producer, BrokerConnection


class MessageEmitter:
    """Class to handle opensearchpy reports and send it over MQTT system"""

    EXCHANGES_NAME_LIST = ["etl-exchange", "collect-exchange"]

    DEFAULT_CHUNK_SIZE = 1

    DEFAULT_PRIORITY = 1

    def __init__(
        self, url, priority=DEFAULT_PRIORITY, chunk_size=DEFAULT_CHUNK_SIZE
    ) -> None:
        self.url = url

        self.priority = priority

        self.chunk_size = chunk_size

        self.producer = None

        self.connection = None

        self.exchanges = {}

        self.logger = logging.getLogger(self.__class__.__name__)

        # init with amqp args

    def setup(self):
        """Init some connection needed for running"""

        # setup amqp connection
        self.connection = BrokerConnection(self.url)

        # init producer
        self.producer = Producer(
            channel=self.connection, on_return=self.handle_message_return
        )

        self.setup_exchanges()

    # pylint: disable=W0613
    def handle_message_return(self, exception, exchange, routing_key, message):
        # pylint: disable=C0301
        """Callback which is expected to be called on message return if message no routed
        See : https://docs.celeryproject.org/projects/kombu/en/v5.1.0/reference/kombu.html#message-producer
        """
        # TODO better usage of kwargs
        self.logger.error("***** %s : %s", routing_key, str(exception))

    def setup_exchanges(self):
        """Instantiate kombu exchange for needed exchange"""

        for exchange_name in self.EXCHANGES_NAME_LIST:
            exchange = Exchange(exchange_name, type="topic", durable=True)
            self.exchanges[exchange_name] = exchange

    @staticmethod
    def get_routing_key(action):
        """Get the routing key for a given report action

        Note:
            For raw data routing key format is a bit different that action

        Args:
            action (str): the opensearchpy action

        Returns:
            str: the routing key
        """
        if "raw" in action:
            splitted_action = action.split("data.")
            left = splitted_action[0]
            right = splitted_action[1:]
            return left.replace("-", ".") + "data." + "".join(right)
        return action

    def get_exchange(self, routing_key) -> Exchange:
        """From the routing key guess the exchange

        Args:
            routing_key (str): the routing key that we want to know the exchange

        Returns:
            Exchange: the exchange to send a message over the routing key
        """

        if routing_key and "raw" in routing_key:
            return self.exchanges["collect-exchange"]
        return self.exchanges["etl-exchange"]

    def _split_report(self, report: EngineReport):
        """Split a report list into small according the chunk_size provide inside

        Args:
            report (EngineReport): the report to split

        Yields:
            MAASMessage: smaller messages that the provided who can be send to the amqp
        """

        min_offset = max_offset = 0

        report_size = len(report.data_ids)
        while max_offset < report_size:
            max_offset = min(min_offset + self.chunk_size, report_size)

            yield MAASMessage(
                document_class=report.document_class,
                document_ids=report.data_ids[min_offset:max_offset],
                pipeline=["BornFromTheMordor"],
            )

            min_offset = max_offset

    def publish(
        self, report: EngineReport, force_routing_key=None, force_document_class=None
    ):
        """The entry point for engine report

        Args:
            report (EngineReport): a report to be send
        """

        for message in self._split_report(report):
            routing_key = (
                force_routing_key
                if force_routing_key
                else self.get_routing_key(report.action)
            )

            document_class = (
                force_document_class if force_document_class else report.document_class
            )

            target_exchange = self.get_exchange(routing_key)

            self.logger.info(
                "publishing message on rk: %s on Exchange : %s with payload: %s / %d ids",
                routing_key,
                target_exchange.name,
                document_class,
                len(message.document_ids),
            )

            message.document_class = document_class
            message.document_indices = report.document_indices

            self.publish_message(
                message_content_dict=message.to_dict(),
                routing_key=routing_key,
                priority=self.priority,
                retry=True,
                exchange=target_exchange,
            )

    def publish_message(
        self,
        message_content_dict: dict,
        routing_key: str,
        priority: int,
        retry: bool,
        exchange: Exchange = None,
        retry_policy=None,
    ):
        """
        See docstring of :py:meth:`kombu.Producer.publish`
        """

        if not exchange:
            exchange = self.get_exchange(routing_key)

        # Avoid anti-pattern "mutable default value as argument"
        if retry_policy is None:
            retry_policy = {
                "interval_start": 0,  # First retry immediately,
                "interval_step": 2,  # then increase by 2s for every retry.
                "interval_max": 30,  # but don't exceed 30s between retries.
                "max_retries": 10,  # give up after X tries.
            }

        self.producer.publish(
            json.dumps(message_content_dict),
            content_type="application/json",
            exchange=exchange,
            routing_key=routing_key,
            delivery_mode="persistent",
            mandatory=True,
            priority=priority,
            retry=retry,
            retry_policy=retry_policy,
        )
