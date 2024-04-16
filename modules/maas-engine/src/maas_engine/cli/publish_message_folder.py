"""

Utility to publish messages from a folder containing payload
"""
import json
import os
import pathlib
import sys
import time
import uuid

import kombu

import maas_engine.cli.args as engine_args


def process_message(path: pathlib.Path, ack: bool, body: str, message: kombu.Message):
    print(".", end="")
    sys.stdout.flush()

    file_path = path / f"{uuid.uuid4()}.json"
    with file_path.open("w", encoding="utf-8") as fd:
        json.dump(body, fd)

    if ack:
        message.ack()
    else:
        message.requeue()


def publish_message_folder_main(args: list[str]):
    """

    backup all payloads from a queue
    """
    parser = engine_args.engine_parser()

    parser.add_argument("--ack", action="store_true")

    parser.add_argument("exchange")

    parser.add_argument("routing_key")

    parser.add_argument("folder")

    args = parser.parse_args(args)

    url = engine_args.get_amqp_credentials_url(args)

    dir_path = pathlib.Path(args.folder)

    with kombu.Connection(url) as connection:
        exchange = kombu.Exchange(args.exchange, type="topic", durable=True)

        producer = kombu.Producer(channel=connection)

        for payload_path in dir_path.glob("*.json"):
            with open(payload_path, encoding="utf-8") as fp:
                producer.publish(
                    fp.read(),
                    content_type="application/json",
                    exchange=exchange.name,
                    routing_key=args.routing_key,
                    delivery_mode="persistent",
                    mandatory=True,
                    priority=5,
                    retry=True,
                    retry_policy={
                        "interval_start": 0,  # First retry immediately,
                        "interval_step": 2,  # then increase by 2s for every retry.
                        "interval_max": 30,  # but don't exceed 30s between retries.
                        "max_retries": args.amqp_retries,  # give up after X tries.
                    },
                )
                print(".", end="")
                sys.stdout.flush()

    print("Done")


def run():
    """entry point"""
    publish_message_folder_main(sys.argv[1:])


if __name__ == "__main__":
    run()
