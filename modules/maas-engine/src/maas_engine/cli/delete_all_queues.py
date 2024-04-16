"""

Utility to clear all queues
"""
import os
import sys

import kombu

import maas_engine.cli.args as engine_args


def delete_all_queues_main(args):
    """

    Clear all queues with user confirmation
    """
    parser = engine_args.engine_parser()

    namespace = parser.parse_args(args)

    url = engine_args.get_amqp_credentials_url(namespace)

    connection = kombu.Connection(url)

    client = connection.get_manager()

    all_queue_info = client.get_queues("/")

    if not all_queue_info:
        print("No queue declared")
        sys.exit()

    non_empty_queues = {
        queue_dict["name"]: queue_dict["messages"]
        for queue_dict in all_queue_info
        if queue_dict["messages"]
    }

    if non_empty_queues:
        print("Warning ! some queues contains messages:", non_empty_queues)
        print("Canceled")
        sys.exit(1)

    confirm = input(f"Are you sure to delete {len(all_queue_info)} queues ? ")
    if not confirm.lower() in ("y", "yes"):
        print("Canceled")
        sys.exit(1)

    for queue_dict in all_queue_info:
        print("Deleting", queue_dict["name"])
        client.delete_queue("/", queue_dict["name"])


def run():
    """entry point"""
    delete_all_queues_main(sys.argv[1:])


if __name__ == "__main__":
    run()
