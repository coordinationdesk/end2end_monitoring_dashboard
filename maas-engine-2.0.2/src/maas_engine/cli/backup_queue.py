"""

Utility to backup all payloads from a queue
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
    """
    Message callback

    Args:
        path (pathlib.Path): target directory
        ack (bool): acknowledge the message
        body (str): payload body
        message (kombu.Message): kombo message
    """
    file_path = path / f"{uuid.uuid4()}.json"

    with file_path.open("w", encoding="utf-8") as fd:
        json.dump(body, fd)

    if ack:
        message.ack()
    else:
        message.requeue()

    print(".", end="")
    sys.stdout.flush()


def backup_queue_main(args: list[str]):
    """

    backup all payloads from a queue
    """
    parser = engine_args.engine_parser()

    parser.add_argument("--ack", action="store_true")

    parser.add_argument(
        "--amqp-timeout", type=int, default=30, help="Drain event timeout in seconds"
    )

    parser.add_argument("exchange", help="Exchange name")

    parser.add_argument("queue", help="Queue name")

    parser.add_argument("routing_key", help="Routing key")

    args = parser.parse_args(args)

    url = engine_args.get_amqp_credentials_url(args)

    dir_path = pathlib.Path(f"{args.queue}_{int(time.time())}")

    dir_path.mkdir(parents=True, exist_ok=True)

    with kombu.Connection(url) as connection:
        exchange = kombu.Exchange(args.exchange, type="topic", durable=True)

        queue = kombu.Queue(
            args.queue,
            exchange,
            routing_key=args.routing_key,
            durable=True,
            exclusive=False,
            max_priority=10,
        )

        with connection.channel() as channel:
            with kombu.Consumer(
                channel,
                queues=queue,
                callbacks=[
                    lambda body, message: process_message(
                        dir_path, args.ack, body, message
                    )
                ],
            ):
                while True:
                    try:
                        connection.drain_events(timeout=args.amqp_timeout)
                    except KeyboardInterrupt as _:
                        # expected case: leave the loop
                        break


def run():
    """entry point"""
    backup_queue_main(sys.argv[1:])


if __name__ == "__main__":
    run()
