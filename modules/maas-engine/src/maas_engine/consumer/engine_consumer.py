"""Core module containing MAASEngine main class"""

import argparse
import json
import logging
import signal
from typing import Any, Dict, List, Optional

from opensearchpy.connection import Connection as OpenSearchConnection
from amqp import Connection
import opensearchpy.connection.connections as db_connections
from opensearchpy.exceptions import OpenSearchException, ImproperlyConfigured

import kombu

import maas_model

from maas_engine.cli.log import setup_logging
import maas_engine.cli.args as engine_args
import maas_engine.exceptions
from maas_engine.consumer.consumer_mixin import MaasConsumerMixin
from maas_engine.consumer.amqp_settings import AMQPSettings
from maas_engine.engine.base import Engine, EngineSession, EngineReport


class MaasEngineConsumer(MaasConsumerMixin):
    """AMQP consumer and message dispatch based on JSON configuration"""

    def __init__(self, args: argparse.Namespace):
        self.logger = logging.getLogger(self.__class__.__name__)

        # namespace from arg parse
        self.args = args

        self.amqp_settings: AMQPSettings

        self.is_ok = False

        self.producer: kombu.Producer

        self.current_pipeline: List[str] = []

        self.db_connection: OpenSearchConnection | None = None

    @property
    def connection(self):
        """proxy to self.amqp_settings.connection so ConsumerMixin is happy"""
        if self.amqp_settings:
            return self.amqp_settings.connection

    def setup(self):
        """
        Do the things so engine is ready to run:
            - dynamic import of business modules: model and engines
            - connect to amqp
            - setup  database connection

        """

        if not (self.args.config or self.args.config_directory):
            raise ValueError("No configuration")

        if self.args.config:
            Engine.load_config_file(self.args.config)

        if self.args.config_directory:
            Engine.load_config_directory(self.args.config_directory)

        if self.args.force:
            self.logger.info("Data update is forced")

        if self.args.es_reject_errors:
            self.logger.warning(
                "opensearch errors will reject the messages. Use this carefully"
            )

        # setup AMQP
        # TODO add retry policy like in collector
        self.amqp_settings = AMQPSettings(self.args.amqp_url)
        self.amqp_settings.connect()
        self.amqp_settings.build_queues(Engine.CONFIG_DICT, self.args.amqp_max_priority)

        self.producer = kombu.Producer(
            channel=self.amqp_settings.connection, on_return=self.handle_message_return
        )

        # connect signal to exit gracefully
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def get_consumers(self, Consumer, channel):
        """create consumer list, grouped by exchange"""
        if self.amqp_settings:
            return self.amqp_settings.get_consumers(Consumer, channel, self.on_message)

    def on_message(self, body: Dict[str, Any], message: kombu.Message) -> None:
        """
        Handle message by executing an engine pipeline

        Args:
            body (Dict[str, Any]): message content
            message (kombu.Message): kombu Message instance
        """
        exchange_name = message.delivery_info["exchange"]

        routing_key = message.delivery_info["routing_key"]

        if not isinstance(body, dict):
            self.logger.error("MSG body is not a dictionnary: rejecting '%s'", body)
            message.reject()
            return

        # CRIT
        message_id = body.get("message_id", "noid")

        self.logger.info(
            "MSG %s RECEIVED FROM %s/%s ancestors: %s pipeline: %s",
            message_id,
            exchange_name,
            routing_key,
            body.get("ancestor_ids", "N/A"),
            body.get("pipeline", "N/A"),
        )

        if self.should_stop:
            self.logger.info("MaasEngine is exiting: not consuming anymore.")
            return

        # pylint: disable=W0718
        # catching any error is justified by the design of the on_start_message() method
        # that shall absolutely succeed before doing anything, otherwise requeue.
        try:
            self.on_start_message(body, message)
        except Exception as error:
            self.logger.exception(error)
            message.requeue()
            return
        # pylint: enable=W0718

        try:
            # setup db

            # execute pipeline to get reports
            reports = self._execute_engines(routing_key, body)

        except maas_engine.exceptions.HandleMessageException as hme:
            self.logger.warning(
                "MSG %s REQUEUE due to previous error: %s", message_id, hme
            )
            # requeue the whole message on expected error like conflicts
            message.requeue()

        except (OpenSearchException, ImproperlyConfigured) as es_error:
            self.logger.error(
                "MSG %s REQUEUE due to opensearch error: %s with payload %s",
                message_id,
                es_error,
                body,
            )
            # requeue the whole message
            message.requeue()

        except maas_engine.exceptions.CannotProcessMessageException as cpme:
            # deliberately separate from except Exception block
            self.logger.exception(
                "MSG %s NORMAL_REJECTION due to previous error: %s with payload %s",
                message_id,
                cpme,
                body,
            )
            message.reject()

        except Exception as exception:  # pylint: disable=W0703
            self.logger.exception(
                "MSG %s ABNORMAL_REJECTION due to previous error: %s with payload %s",
                message_id,
                exception,
                body,
            )
            message.reject()

        else:
            pipeline = body.get("pipeline", []) + self.current_pipeline
            # send reports before ACK
            if reports:
                # generate the list of indentifiers of ancestor messages
                ancestor_ids = body.get("ancestor_ids", []) + [body["message_id"]]

                self.notify_reports(
                    self.amqp_settings.exchanges["etl-exchange"],
                    reports,
                    message.properties.get(
                        "priority", round(self.args.amqp_max_priority / 2)
                    ),
                    ancestor_ids=ancestor_ids,
                    pipeline=pipeline,
                    force=body.get("force", True),
                )

            self.logger.info(
                "MSG %s ACK %s Completed pipeline: %s",
                message_id,
                routing_key,
                pipeline,
            )

            message.ack()

        finally:
            self.on_end_message(body, message)

    def on_start_message(self, body: Dict[str, Any], message: kombu.Message) -> None:
        """
        Hook for pre-pipeline execution: setup db connection

        Args:
            body (Dict[str, Any]): message body
            message (kombu.Message): message
        """

        self.logger.debug("on_start_message: create connection to opensearch")
        self.db_connection = db_connections.create_connection(
            hosts=[self.args.es_url],
            retry_on_timeout=True,
            max_retries=self.args.es_retries,
            timeout=self.args.es_timeout,
            verify_certs=not self.args.es_ignore_certs_verification,
            ssl_show_warn=not self.args.es_ignore_certs_verification,
        )

    def on_end_message(self, body: Dict[str, Any], message: kombu.Message) -> None:
        """
        Hook for post-pipeline execution: close opensearch connection

        Args:
            body (Dict[str, Any]): message body
            message (kombu.Message): message
        """
        if self.db_connection:
            self.logger.debug("on_end_message: close connection to opensearch")
            self.db_connection.close()
            db_connections.remove_connection("default")
            self.db_connection = None

    def _execute_engines(
        self, routing_key: str, body: Dict[str, Any]
    ) -> list[EngineReport]:
        """Launch the execution of concerned engines

        Args:
            engine_id_list (list[str]): list of engine-id to compute
            data_type (str): the data type at the origin of the computation
            item_ids (list[str]): id list of the data_type items at the origin of
                the computation
        """
        engine_list: List[Engine] = [
            Engine.get(engine_args, self.args)
            for engine_args in self.amqp_settings.event_mapping[routing_key]
        ]

        engine_responses: List[EngineReport] = []

        standalone_responses: List[EngineReport] = []

        self.current_pipeline = []

        # instanciate common session to share data between engines
        session = EngineSession()

        for engine in engine_list:
            # set common session
            engine.session = session

            engine.payload = engine.deserialize_payload(body)

            data_log = ""
            if document_ids := body.get("document_ids"):
                data_log += f" {len(document_ids)}"

            if document_class := body.get("document_class"):
                data_log += f" {document_class}"

            self.logger.info(
                "MSG %s CALL %s%s",
                session.payload.message_id,
                engine.ENGINE_ID,
                data_log,
            )

            # log payload in debug only for performance
            self.logger.debug("Payload: %s", engine.payload)

            # QUESTION may run() call be in a try/except block ?
            # is a partial run of a list of engines dangerous ?
            # allow partial run by configuration
            # better break and reject for safety ?

            responses: List[EngineReport] = [
                report
                for report in engine.run(routing_key, engine.payload)
                if engine.send_reports
            ]

            self.current_pipeline.append(engine.ENGINE_ID)

            # later use engine.reports after v1 ?

            if responses:
                if getattr(engine, "merge_reports", True):
                    engine_responses.extend(responses)
                else:
                    standalone_responses.extend(responses)

        engine_responses = EngineReport.merge_reports(engine_responses)

        return engine_responses + standalone_responses

    # pylint: disable=W0613
    def handle_message_return(self, exception, exchange, routing_key, message):
        # pylint: disable=C0301
        """Callback which is expected to be called on message return if message no routed
        See : https://docs.celeryproject.org/projects/kombu/en/v5.1.0/reference/kombu.html#message-producer
        """
        self.logger.error("***** %s : %s", routing_key, str(exception))

    def notify_reports(
        self,
        exchange: str,
        reports: List[EngineReport],
        priority: int,
        ancestor_ids: Optional[List[str]] = None,
        pipeline: Optional[List[str]] = None,
        force: bool = True,
    ):
        """send messages base on reports to the given exchange

        Args:
            exchange (str): rabbitmq exchange
            reports (list[EngineReport]): merged report
        """

        for report in EngineReport.split_reports(reports):
            self.notify_report(
                exchange,
                report,
                priority,
                ancestor_ids=ancestor_ids,
                pipeline=pipeline,
                force=force,
            )

    def notify_report(
        self,
        exchange,
        report: EngineReport,
        priority: int,
        ancestor_ids: Optional[List[str]] = None,
        pipeline: Optional[List[str]] = None,
        force: bool = True,
    ):
        """
        send a message base on a report to the given exchange

        Args:
            exchange (Exchange): message destination exchange
            report (EngineReport): report to send
        """

        self.logger.info(
            "notify using RK: %s on Exchange : %s with payload: %s / %d ids",
            report.action,
            exchange.name,
            report.document_class,
            len(report.data_ids),
        )

        msg = maas_model.MAASMessage(
            document_class=report.document_class,
            document_ids=report.data_ids,
            document_indices=report.document_indices,
            force=force,
        )

        if ancestor_ids:
            msg.ancestor_ids = ancestor_ids

        if pipeline:
            msg.pipeline = pipeline

        self.producer.publish(
            json.dumps(msg.to_dict()),
            content_type="application/json",
            exchange=exchange.name,
            routing_key=report.action,
            delivery_mode="persistent",
            mandatory=True,
            priority=priority,
            retry=True,
            retry_policy={
                "interval_start": 0,  # First retry immediately,
                "interval_step": 2,  # then increase by 2s for every retry.
                "interval_max": 30,  # but don't exceed 30s between retries.
                "max_retries": self.args.amqp_retries,  # give up after X tries.
            },
        )

    def exit_gracefully(self, signum, frame):
        """
        Handle SIGINT and SIGTERM: try to requeue message

        思へばこの世は常の住み家にあらず

        Args:
            signum ([int]): Signal number
            frame ([frame]): bytecode frame
        """
        self.logger.info(
            "Received signal %d at frame %s: exiting after last run", signum, frame
        )

        self.logger.debug("Set Consumer.should_stop to True")

        self.should_stop = True

    @staticmethod
    def main(args):
        """Main entry point

        Args:
            args (list): command line argument list like sys.argv[:1]
        """
        # parse CLI arguments
        parser = argparse.ArgumentParser(parents=[engine_args.engine_parser()])

        namespace = parser.parse_args(args)

        setup_logging(loglevel=namespace.loglevel)

        # dump some system info
        logging.info("Starting maas-engine %s", maas_engine.__version__)

        logging.info("Using maas-model %s", maas_model.__version__)

        # Add calculated arguments
        namespace.es_url = engine_args.get_es_credentials_url(namespace)

        namespace.amqp_url = engine_args.get_amqp_credentials_url(namespace)

        # Instanciate consumer
        consumer = MaasEngineConsumer(namespace)

        # setup resources
        consumer.setup()

        # run the listening loop
        consumer.run()
