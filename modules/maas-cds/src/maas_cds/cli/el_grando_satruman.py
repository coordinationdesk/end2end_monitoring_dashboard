"""CLI to use query engine or a custom one"""

import argparse
import json
import logging
import sys

from opensearchpy.connection.connections import connections as es_connections

from maas_engine.cli import args as maas_args
from maas_engine.engine.query import QueryEngine
from maas_engine.engine.base import Engine

from maas_model.message import MAASQueryMessage

from maas_cds.lib.decorators import duration_inspector
from maas_cds.lib.message_emitter import MessageEmitter


class Satruman:
    "🧙‍♂️ Always you must meddle, looking for trouble where none exists"

    def __init__(self, args) -> None:
        self.args = args

        self.logger = logging.getLogger(self.__class__.__name__)

        self.es_conn = None

        self.messenger = None

    def setup(self):
        """Setup connectivity for opensearchpy and rabbitmq, load engines configuration"""

        logformat = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
        log_level = (
            self.args.loglevel if self.args.loglevel is not None else logging.WARNING
        )

        logging.basicConfig(
            level=log_level,
            stream=sys.stdout,
            format=logformat,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.logger.info(
            "[SETUP][Logger] - Setup on level %s", logging.getLevelName(log_level)
        )

        self.logger.info("[SETUP][Engine] - Load config %s", self.args.es_url)
        Engine.load_config_file(self.args.config)

        es_url = maas_args.get_es_credentials_url(self.args)

        self.logger.info("[SETUP][opensearchpy] - Setup on %s", self.args.es_url)

        self.es_conn = es_connections.create_connection(
            hosts=[es_url],
            retry_on_timeout=True,
            max_retries=self.args.es_retries,
            timeout=self.args.es_timeout,
            verify_certs=not self.args.es_ignore_certs_verification,
            ssl_show_warn=not self.args.es_ignore_certs_verification,
        )

        self.logger.info("[SETUP][MessageEmitter] - Setup on %s", self.args.amqp_url)

        amqp_url = maas_args.get_amqp_credentials_url(self.args)
        self.messenger = MessageEmitter(
            amqp_url, priority=self.args.amqp_priority, chunk_size=self.args.chunk_size
        )

        self.messenger.logger.setLevel(log_level)
        self.messenger.setup()

        # shut up opensearchpy
        logging.getLogger("opensearchpy").setLevel(logging.WARNING)

    def run_operation(self):
        """Custom engine call"""

        self.logger.debug("[OPERATION] - %s", self.args.operation)
        if Engine.get(self.args.operation.upper()):
            operation_engine = Engine.get(
                {
                    "id": self.args.operation.upper(),
                    "chunk_size": self.args.chunk_size,
                }
            )

            payload = operation_engine.PAYLOAD_MODEL(
                **json.loads(self.args.operation_args)
            )

            operation_engine.payload = payload
            reports = operation_engine.run("magic_routing", payload)

            for report in reports:
                if not self.args.dry_run:
                    self.messenger.publish(report, self.args.routing_key)
                else:
                    self.logger.info("[DRY] - %s", report)

    @duration_inspector
    def run(self):
        """main entry point"""

        if self.args.operation is not None:
            self.run_operation()

        # # elif self.args.specific_id is not None:
        # #     self.logger.info("[SPECIFIC-ID] - %s", self.args.specific_id)
        # #     self.messenger.handle_message(self.config, self.args.specific_id)
        # #     self.messenger.flush_message_groups()

        else:
            engine = QueryEngine(chunk_size=self.args.chunk_size)

            payload = MAASQueryMessage(
                **{
                    "document_class": self.args.document_class,
                    "query_string": self.args.query_string,
                }
            )

            engine.payload = payload
            reports = engine.run("magic_routing", payload)

            for report in reports:
                if self.args.dry_run:
                    self.logger.info("[DRY-RUN] : %s", report)
                else:
                    self.messenger.publish(
                        report,
                        force_routing_key=self.args.routing_key,
                        force_document_class=self.args.output_document_class,
                    )


def satruman_main(argv):
    """satruman entry point with args parsing

    Args:
        argv (list): argument provide to run satruman
    """

    # AMQP / ES access
    parser = argparse.ArgumentParser(
        parents=[maas_args.es_parser(), maas_args.amqp_parser()]
    )

    # AMQP customization
    parser.add_argument(
        "--amqp-priority",
        dest="amqp_priority",
        default=MessageEmitter.DEFAULT_PRIORITY,
        type=int,
    )
    parser.add_argument(
        "--chunk-size",
        dest="chunk_size",
        default=MessageEmitter.DEFAULT_CHUNK_SIZE,
        type=int,
    )

    # Loglevel
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    # Minimum required
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="Configuration path (default: %(default)s)",
        action=maas_args.EnvDefault,
        envvar="MAAS_ENGINE_CONFIG",
        required=True,
        type=argparse.FileType("r"),
    )

    parser.add_argument("--document-class", dest="document_class", default=None)
    parser.add_argument(
        "--output-document-class", dest="output_document_class", default=None
    )

    parser.add_argument("--routing-key", dest="routing_key", default=None)

    # Basic QueryEngine
    parser.add_argument("--query-string", dest="query_string", default="*")

    parser.add_argument("--operation", dest="operation", default=None)
    parser.add_argument("--operation-args", dest="operation_args", default=None)

    # TODO support specific id
    # parser.add_argument("--specific-id", dest="specific_id", default=None)

    # TODO check the implementation maybe add a decorator to handle request and support dry run inside
    # look at the payload_to_tasks decorators
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Don't modify database",
        dest="dry_run",
    )

    args = parser.parse_args(argv)

    if (args.document_class is None and args.routing_key is None) and (
        args.operation is None and args.operation_args is None
    ):
        parser.error(
            "At least one query engine (--document_class and --routing_key) or one operation (--operation and --operation-args)"
        )

    wizard = Satruman(args)
    wizard.setup()
    wizard.run()


def run():
    """main entry point"""
    satruman_main(sys.argv[1:])


if __name__ == "__main__":
    run()
