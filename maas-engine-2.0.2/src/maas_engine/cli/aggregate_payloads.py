"""

Utility to aggregate payloads to a new chunk size
"""
import json
import os
import pathlib
import sys
import time
import uuid

from maas_model.message import MAASMessage

import maas_engine.cli.args as engine_args

from maas_engine.engine.base import Engine


def aggregate_payloads_main(args: list[str]):
    """

    Clear all queues with user confirmation
    """
    parser = engine_args.engine_parser()

    parser.add_argument("--chunk-size", type=int, default=512)

    parser.add_argument("input_directory")
    parser.add_argument("output_directory")

    args = parser.parse_args(args)

    input_dir = pathlib.Path(args.input_directory)

    output_dir = pathlib.Path(args.output_directory)

    output_dir.mkdir(parents=True)

    messages = []

    print("Loading messages")

    for payload_path in input_dir.glob("*.json"):
        with open(payload_path, encoding="utf-8") as fp:
            payload_dict = json.load(fp)
            messages.append(Engine.deserialize_payload(payload_dict))
            print(".", end="")
            sys.stdout.flush()

    print("Ok", os.linesep)

    print("Grouping by model class")

    msg_dict = {}

    for msg in messages:
        if msg.document_class not in msg_dict:
            msg_dict[msg.document_class] = []
        msg_dict[msg.document_class].append(msg)

    new_messages = []

    print("Generating messages")

    for document_class, msg_list in msg_dict.items():
        msg_list.sort(key=lambda msg: msg.msg_datetime)

        msg_ids = []

        for msg in msg_list:
            msg_ids.extend(msg.document_ids)

        # remove duplicates
        msg_ids = list(dict.fromkeys(msg_ids))

        chunks = []

        while msg_ids:
            chunks.append(msg_ids[: args.chunk_size])

            del msg_ids[: args.chunk_size]

        new_messages.extend(
            [
                MAASMessage(document_ids=chunk, document_class=document_class)
                for chunk in chunks
            ]
        )

    time_base = f"{int(time.time())}"

    print(f"Writing {len(new_messages)} messages")

    for index, msg in enumerate(new_messages):
        file_path = output_dir / f"{time_base}_{index:06d}.json"
        with file_path.open("w", encoding="utf-8") as fd:
            json.dump(msg.to_dict(), fd)

    print("Done")


def run():
    """entry point"""
    aggregate_payloads_main(sys.argv[1:])


if __name__ == "__main__":
    run()
