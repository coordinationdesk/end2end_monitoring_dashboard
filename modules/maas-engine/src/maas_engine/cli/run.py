"""

A basic entry point for engine cli run
"""
import argparse
import dataclasses
import json
import logging
import sys
from typing import Optional

import opensearchpy.connection.connections as db_connections

import maas_model

import maas_engine
from maas_engine.cli.log import setup_logging
import maas_engine.cli.args as engine_args
from maas_engine.engine.base import Engine


def maas_engine_main(
    args: list[str],
    engine_id: Optional[str] = None,
    parent_parsers: Optional[list[argparse.ArgumentParser]] = None,
):
    """A basic entry point.

    Still in development: only setup database setup, no amqp

    Args:
        args (list): command line argument list like sys.argv[:1]
    """
    if not parent_parsers:
        parent_parsers = [engine_args.engine_parser()]

    # parse CLI arguments
    parser = argparse.ArgumentParser(parents=parent_parsers)

    if not engine_id:
        parser.add_argument(
            "-e", "--engine-id", help="Engine identifier", required=True
        )

    parser.add_argument(
        "-r",
        "--routing-key",
        help="Routing key (only if it has a meaning)",
        required=False,
        default="",
    )

    parser.add_argument(
        "-p", "--payload", help="Json file containing a MAASMessage", required=False
    )

    namespace = parser.parse_args(args)

    if not engine_id:
        engine_id = namespace.engine_id

    if namespace.config:
        Engine.load_config_file(namespace.config)

    if namespace.config_directory:
        Engine.load_config_directory(namespace.config_directory)

    Engine.load_config(namespace.config)

    engine = Engine.get(engine_id, namespace)

    if namespace.payload:
        with open(namespace.payload, encoding="UTF-8") as payload_fd:
            message = engine.deserialize_payload(json.load(payload_fd))
            engine.payload = message
    else:
        message = maas_model.MAASMessage()

    setup_logging(loglevel=namespace.loglevel)

    # dump some system info
    logging.info("Starting maas-engine %s", maas_engine.__version__)

    logging.info("Using maas-model %s", maas_model.__version__)

    # Add calculated arguments
    namespace.es_url = engine_args.get_es_credentials_url(namespace)

    logging.info("Setup connection to Database")
    db_connections.create_connection(
        hosts=[engine_args.get_es_credentials_url(namespace)],
        retry_on_timeout=True,
        max_retries=namespace.es_retries,
        verify_certs=not namespace.es_ignore_certs_verification,
        ssl_show_warn=not namespace.es_ignore_certs_verification,
    )

    # namespace.amqp_url = engine_args.get_amqp_credentials_url(namespace)

    for report in engine.run(namespace.routing_key, message):
        # no notification on bus yet, dump report to stdout
        print(dataclasses.asdict(report))


def run():
    "entry point"
    maas_engine_main(sys.argv[1:])


if __name__ == "__main__":
    run()
