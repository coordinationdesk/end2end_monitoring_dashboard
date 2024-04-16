"""Message bus tools"""
import dataclasses
import json
import logging
from typing import Dict
import socket


from kombu import BrokerConnection, Producer
from kombu.common import maybe_declare

from maas_model import MAASMessage

from maas_collector.queues.queues import PUBLISH_EXCHANGE


class Messenger:
    """
    Messenger encapsulates collector message emitting using groups

    """

    def __init__(
        self,
        url: str,
        v1_compatibility: bool = False,
        priority: int = 0,
        max_retries: int = 0,
        pipeline_name: str = "Collector",
    ):
        self.logger: logging.Logger = logging.getLogger(pipeline_name)

        # rabbitmq url
        self.url: str = url

        self.priority: int = priority

        self.max_retries: int = max_retries

        self.pipeline_name: str = pipeline_name

        # rabbitmq connection
        self._connection: BrokerConnection | None = None

        # message emitter
        self._producer: Producer | None = None

        # V1 compatibility flag
        self.v1_compatibility = v1_compatibility

        # message group configuration
        self.chunk_config: Dict[str, int] = {}

        # grouped messages
        self.message_groups = {}

    @property
    def connection(self) -> BrokerConnection:
        """
        Lazy build broker connection

        Returns:
            BrokerConnection: established connection
        """
        if self._connection is None:
            self._connection = BrokerConnection(
                self.url,
                transport_options={
                    "client_properties": {
                        "connection_name": f"collector@{socket.gethostname()}"
                    }
                },
            )
        return self._connection

    @property
    def producer(self) -> Producer:
        """
        Lazy build producer

        Returns:
            Producer: initialized producer
        """
        if self._producer is None:
            self._producer = self.connection.Producer(
                exchange=PUBLISH_EXCHANGE, on_return=self._on_return
            )
            maybe_declare(PUBLISH_EXCHANGE, self._producer.channel)
        return self._producer

    def setup(self):
        """Connect to the AMQP broker and setup message producer"""
        self.logger.debug("Setup connection to AMQP broker: %s", self.url)

    def load_config_file(self, path: str):
        """Load amqp configuration from file"""
        with open(path, "r", encoding="UTF-8") as config_fd:
            json_config = json.load(config_fd)

            if "amqp" not in json_config:
                # not amqp setting
                return

            for routing_key, routing_info in json_config["amqp"].items():
                if not "chunk_size" in routing_info:
                    continue

                # log overwrite
                if routing_key in self.chunk_config:
                    # log redeclare
                    self.logger.warning(
                        "%s: overwrite chunk size config for %s from %s to %s",
                        path,
                        routing_key,
                        self.chunk_config[routing_key],
                        routing_info["chunk_size"],
                    )

                self.logger.info(
                    "Set chunk configuration for %s: %d",
                    routing_key,
                    routing_info["chunk_size"],
                )

                self.chunk_config[routing_key] = routing_info["chunk_size"]

    def handle_message(self, config, document_id: str, index: str | None = None):
        """handle a document identifier and decide to send it (or not) on the message
        bus following the collector configuration. Accumulate identifiers according to
        the amqp chunk size in the configuration file to send message groups.

        Args:
            config ([FileCollectorConfiguration]): configuration
            document_id ([str]): document identifier
        """
        if not config.routing_key:
            # don't send any message
            return

        document_indices = [index] if index is not None else []

        if not config.routing_key in self.chunk_config:
            # no message grouping: send single document identifier and index
            self.send_to_queue(
                config.routing_key,
                MAASMessage(
                    document_class=config.model_name,
                    document_ids=[document_id],
                    document_indices=document_indices,
                    pipeline=[self.pipeline_name],
                ),
            )
            return

        chunk_size = self.chunk_config[config.routing_key]

        # get the message group for the routing key
        if config.routing_key in self.message_groups:
            group = self.message_groups[config.routing_key]
        else:
            group = self.message_groups[config.routing_key] = {}

        # get the document identifier and index list for the model
        if config.model_name in group:
            info = group[config.model_name]

        else:
            info = group[config.model_name] = {}
            info["document_ids"] = []
            info["document_indices"] = []

        info["document_ids"].append(document_id)

        if index is not None and index not in info["document_indices"]:
            info["document_indices"].append(index)

        # send messages by chunk depending the configuration
        while len(info["document_ids"]) >= chunk_size:
            self.logger.debug(
                "%s buffer has reach %d limit, sending payload",
                config.routing_key,
                chunk_size,
            )

            # send the chunk
            self.send_to_queue(
                config.routing_key,
                MAASMessage(
                    document_class=config.model_name,
                    document_ids=info["document_ids"][:chunk_size],
                    document_indices=info["document_indices"][:chunk_size],
                    pipeline=[self.pipeline_name],
                ),
            )

            # remove the chunk
            del info["document_ids"][:chunk_size]
            del info["document_indices"][:chunk_size]

    def flush_message_groups(self):
        """clear the document identifier cache"""
        for routing_key, group in self.message_groups.items():
            for model_name, info in group.items():
                # filter empty identifier list

                if not info["document_ids"]:
                    continue

                self.send_to_queue(
                    routing_key,
                    MAASMessage(
                        document_class=model_name,
                        document_ids=info["document_ids"],
                        document_indices=info["document_indices"],
                        pipeline=[self.pipeline_name],
                    ),
                )

        self.message_groups.clear()

    def send_to_queue(self, routing_key: str, payload: MAASMessage):
        """send creation / update message to rabbitmq

        Args:
            routing_key (str): routing key on the publishing exchange
            payload (MAASMessage): payload containing document ids and indices
        """
        # Keep only unique index
        payload.document_indices = list(set(payload.document_indices))
        payload.pipeline = [self.pipeline_name]

        if self.v1_compatibility:
            body = payload.document_ids
        else:
            body = dataclasses.asdict(payload)

        self.logger.info(
            "MSG %s PUBLISHING TO %s/%s",
            payload.message_id,
            PUBLISH_EXCHANGE.name,
            routing_key,
        )

        self.logger.debug("Message body: %s", body)

        json_body = json.dumps(body)

        try:
            self.producer.publish(
                json_body,
                content_type="application/json",
                exchange=PUBLISH_EXCHANGE,
                routing_key=routing_key,
                delivery_mode="persistent",
                mandatory=True,
                retry=True,
                priority=self.priority,
                retry_policy={
                    "interval_start": 0,  # First retry immediately,
                    "interval_step": 2,  # then increase by 2s for every retry.
                    "interval_max": 30,  # but don't exceed 30s between retries.
                    "max_retries": self.max_retries,  # give up after X tries.
                },
            )
            self.logger.info(
                "MSG %s PUBLISHED TO %s/%s %d %s",
                payload.message_id,
                PUBLISH_EXCHANGE.name,
                routing_key,
                len(payload.document_ids),
                payload.document_class,
            )
        except Exception as error:
            self.logger.error(
                "MSG %s FAILED TO PUBLISH TO %s/%s %d %s (%s)",
                payload.message_id,
                PUBLISH_EXCHANGE.name,
                routing_key,
                len(payload.document_ids),
                payload.document_class,
                error,
            )
            self.logger.error(
                "MSG %s UNPUBLISHED on %s/%s PAYLOAD %s",
                payload.message_id,
                PUBLISH_EXCHANGE.name,
                routing_key,
                json_body,
            )
            raise error

    def _on_return(self, exception, exchange, routing_key, message):
        """Error callback for message publishing

        see:

        https://docs.celeryproject.org/projects/kombu/en/stable/userguide/producers.html

        for details
        """
        if exception.args[1] == "NO_ROUTE":
            self.logger.warning(
                "AMQP exchange %s has no route for %s", exchange, routing_key
            )
        else:
            self.logger.error(
                "AMQP error on %s:%s : %s", exchange, routing_key, exception
            )
            self.logger.error("Cannot deliver message: %s", message.body)

    def close(self):
        """

        Close resources
        """
        for symbol in ["_producer", "_connection"]:
            value = getattr(self, symbol)
            if value is not None:
                try:
                    self.logger.debug("Closing %s", symbol)
                    value.close()
                # pylint: disable=broad-exception-caught
                # no necessity to raise, only log
                except Exception as error:
                    self.logger.error("Cannot close %s: %s", symbol, error)
                # pylint: enable=broad-exception-caught
                finally:
                    setattr(self, symbol, None)

    def __len__(self):
        return sum(
            [
                len(info["document_ids"])
                for info in [group.values() for group in self.message_groups.values()]
                if info and "document_ids" in info
            ]
        )
